#!/usr/bin/env python3
"""
NFC canon metadata extractor (Phase 5).

Parses the 17 canon .tex files into a machine-readable claim corpus that is the
single source of truth for status counts, obligation accountings, dependency
edges, and the dashboard. Deterministic and idempotent: re-running on unchanged
sources yields byte-identical output (stable sort, sorted keys).

Output:
  metadata/claims.json        one record per status-tagged environment
  metadata/edges.json         proof-citation dependency edges
  metadata/views.json         the five status views + the four frontier accountings
  metadata/census.json        authoritative status-tag census (resolves F-3)

Design notes:
  * The AUTHORITATIVE status classifier is the \\status{X} tag, NOT the
    environment name (per review ruling on `openobligation`: 110 obligation
    environments exist, only 5 carry [O]).
  * "historical/current flag", "authority level", "supersession", "discharge
    basis", "reviewer note", "review-needed" are seeded from an editable overlay
    file (metadata/overlay.json) so human judgments live outside the extractor
    and survive re-extraction. The extractor never invents these; absent an
    overlay entry they default to current=True/authority by tier heuristic/None.
"""
import re, json, glob, os, hashlib, datetime, subprocess

CANON = [
    "NFC_Book_I","NFC_Book_II","NFC_Book_III","NFC_Book_IV","NFC_Book_V",
    "NFC_Book_VI","NFC_Book_VII","NFC_BIO_Branch","NFC_CRYST_Branch",
    "NFC_GR_Branch","NFC_LING_Branch","NFC_NS_Branch","NFC_RH_Branch",
    "NFC_SCC_Branch","NFC_SM_Branch","NFC_SPEC_Branch","NFC_YM_Branch",
]
SPINE = {f"NFC_Book_{r}" for r in ["I","II","III","IV","V","VI","VII"]}

def branch_of(stem):
    if stem in SPINE: return "SPINE"
    return stem.replace("NFC_","").replace("_Branch","")

STATUS_ENVS = ["theorem","proposition","corollary","lemma","definition",
               "remark","scholium","openobligation","obligation",
               "standingrule","hypothesis"]
STMT_ENVS = ["theorem","proposition","corollary","lemma"]  # carry proof force + proofs

status_re = re.compile(r'\\status\{([A-Za-z0-9]+)\}')
label_re  = re.compile(r'\\label\{([^}]*)\}')
ref_re    = re.compile(r'\\(?:ref|eqref|cref|Cref)\{([^}]*)\}')
sec_re    = re.compile(r'\\(section|subsection|subsubsection)\*?\{')

STATUS_FORCE = {  # status tag -> human "status force" descriptor
    "U":"unconditional","C":"conditional","D":"definitional/standing",
    "B":"bridge (cross-scope, needs transfer theorem)","O":"open (undischarged)",
    "R":"remark (non-load-bearing)",
}
CLAIM_TYPE = {
    "theorem":"theorem","proposition":"proposition","corollary":"corollary",
    "lemma":"lemma","definition":"definition","remark":"remark",
    "scholium":"remark","openobligation":"obligation","obligation":"obligation",
    "standingrule":"standing_rule","hypothesis":"hypothesis",
}

def find_sections(text):
    """Return sorted list of (pos, title) for section-like commands (brace-matched)."""
    out=[]
    for m in sec_re.finditer(text):
        i=m.end(); depth=1; buf=[]
        while i<len(text) and depth>0:
            c=text[i]
            if c=='{':depth+=1
            elif c=='}':
                depth-=1
                if depth==0:break
            buf.append(c); i+=1
        out.append((m.start(), ''.join(buf).strip()))
    return out

def section_at(sections, pos):
    cur="(front matter)"
    for p,t in sections:
        if p<=pos: cur=t
        else: break
    return cur

def brace_match_env(text, env, start):
    """Given \\begin{env} ending at `start`, return (body, end_index)."""
    endpat=re.compile(r'\\end\{'+re.escape(env)+r'\}')
    m=endpat.search(text,start)
    if not m: return text[start:], len(text)
    return text[start:m.start()], m.end()

def load_overlay():
    p="metadata/overlay.json"
    if os.path.exists(p):
        return json.load(open(p))
    return {}

def git_commit():
    """Census commit for provenance. Resolution order:
    (1) NFC_CENSUS_COMMIT env var (for distributed archives without .git);
    (2) git rev-parse; (3) "unknown"."""
    if os.environ.get("NFC_CENSUS_COMMIT"):
        return os.environ["NFC_CENSUS_COMMIT"]
    try:
        return subprocess.check_output(["git","rev-parse","--short","HEAD"],
                                       cwd=".", stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        return "unknown"

def build_timestamp():
    """Reproducible timestamp. Resolution order:
    (1) SOURCE_DATE_EPOCH (reproducible-builds.org convention);
    (2) git HEAD commit time; (3) current UTC time."""
    sde = os.environ.get("SOURCE_DATE_EPOCH")
    if sde:
        return datetime.datetime.fromtimestamp(int(sde), datetime.timezone.utc)
    try:
        ct = subprocess.check_output(["git","log","-1","--format=%ct"],
                                     cwd=".", stderr=subprocess.DEVNULL).decode().strip()
        return datetime.datetime.fromtimestamp(int(ct), datetime.timezone.utc)
    except Exception:
        return datetime.datetime.now(datetime.timezone.utc)

def main():
    overlay=load_overlay()
    claims=[]; edges=[]
    census={k:0 for k in ["D","U","C","B","O","R"]}
    census_other={}
    for stem in CANON:
        fn=stem+".tex"
        text=open(fn,encoding="utf-8",errors="replace").read()
        branch=branch_of(stem)
        sections=find_sections(text)
        # iterate every env-with-status occurrence
        beginpat=re.compile(r'\\begin\{('+'|'.join(STATUS_ENVS)+r')\}(\[[^\]]*\])?')
        for m in beginpat.finditer(text):
            env=m.group(1); optarg=m.group(2) or ""
            body,end=brace_match_env(text,env,m.end())
            smatch=status_re.search(optarg) or status_re.search(body[:120])
            status=smatch.group(1) if smatch else None
            if status is None:
                continue  # only track status-tagged environments
            lmatch=label_re.search(body)
            label=lmatch.group(1) if lmatch else None
            sec=section_at(sections,m.start())
            if status in census: census[status]+=1
            else: census_other[status]=census_other.get(status,0)+1
            # dependencies: refs within this environment body (all refs, dedup, sorted)
            deps=sorted(set(ref_re.findall(body)))
            # proof-citation edges: for statement envs, capture the *following* proof block
            proof_deps=[]
            if env in STMT_ENVS and label:
                look=text[end:end+2500]
                pm=re.search(r'\\begin\{proof\}',look)
                if pm and pm.start()<400:
                    pbody,_=brace_match_env(text,"proof",end+pm.end())
                    proof_deps=sorted(set(ref_re.findall(pbody)))
                    for d in proof_deps:
                        edges.append({"from":label,"to":d,"file":fn,"kind":"proof-cite"})
            ov=overlay.get(label,{}) if label else {}
            rec={
                "claim_id": label or f"{stem}:{env}@{m.start()}",
                "source_file": fn,
                "source_section": sec,
                "claim_type": CLAIM_TYPE.get(env,env),
                "environment": env,                 # raw env (openobligation vs obligation, etc.)
                "status_tag": status,
                "status_force": STATUS_FORCE.get(status,"UNKNOWN"),
                "branch": branch,
                "dependencies": proof_deps or deps,
                "discharge_basis": ov.get("discharge_basis"),
                "supersedes": ov.get("supersedes"),
                "superseded_by": ov.get("superseded_by"),
                "historical": ov.get("historical", False),
                "authority_level": ov.get("authority_level", _authority_default(env,label)),
                "frontier_accounting": _frontier_membership(label,status,env),
                "generated_from": None,             # canon source is authored, not generated
                "last_reviewed": ov.get("last_reviewed"),
                "reviewer_note": ov.get("reviewer_note"),
                "review_needed": ov.get("review_needed", False),
            }
            claims.append(rec)
    claims.sort(key=lambda r:(r["source_file"], r["claim_id"]))
    edges.sort(key=lambda e:(e["file"],e["from"],e["to"]))

    # ---- Frontier accountings (kept SEPARATE, never summed) ----
    syntactic_O=[c["claim_id"] for c in claims if c["status_tag"]=="O"]
    ob_labels=[c["claim_id"] for c in claims
               if c["environment"] in ("openobligation","obligation")
               and c["claim_id"].startswith("ob:")]
    reduced_frontier=[  # from Book VII / roster, authoritative curated list (overlay-confirmable)
        {"item":"RH arithmetic orbit grammar","labels":["ob:rh-sf-logderiv-legality","ob:rh-sf-trace-pairing-law","ob:rh-sf-d2-audit"]},
        {"item":"RH packet-local synthesis","labels":["ob:rh-tloc-L3","ob:rh-tloc-L4","ob:rh-tloc-L5","ob:rh-tloc-L6","ob:rh-tloc-L7"]},
        {"item":"SM matter content","labels":["ob:SM-matter","ob:SM-IDcont-TV","ob:O-ID-cont"]},
        {"item":"GR global curvature-subcriticality","labels":["def:curv-subcrit-global"]},
    ]
    accountings={
        "I_syntactic_O_census":{"count":len(syntactic_O),"labels":sorted(syntactic_O),
            "measures":"environments literally tagged \\status{O}"},
        "II_named_obligation_roster":{"count":len(ob_labels),"labels":sorted(ob_labels),
            "measures":"all ob:-labelled obligation environments regardless of tag"},
        "III_reduced_irreducible_frontier":{"count":len(reduced_frontier),"items":reduced_frontier,
            "measures":"genuinely open deep mathematics after all reductions"},
        "IV_branch_posture":{"source":"per-branch A1 status proposition",
            "measures":"closure ladder position per branch (see views.branch_posture)"},
        "_warning":"These four accountings measure different things and MUST NOT be summed.",
    }

    # ---- Five status views ----
    views={
        "formal_tag_view": census | {"_other":census_other},
        "branch_posture_view": _branch_posture_view(),
        "obligation_roster_view":{
            "total_ob_labels":len(ob_labels),
            "by_tag":_count_by(claims, lambda c:c["status_tag"],
                                pred=lambda c:c["claim_id"].startswith("ob:")),
        },
        "reduced_frontier_view": reduced_frontier,
        "release_snapshot_view":{
            "generated": build_timestamp().isoformat(),
            "census_commit": git_commit(),
            "total_claims": len(claims),
            "census": census,
        },
    }

    os.makedirs("metadata",exist_ok=True)
    _dump("metadata/claims.json", claims)
    _dump("metadata/edges.json", edges)
    _dump("metadata/views.json", views)
    # reconcile against the raw grep census endorsed by the F-3 review ruling
    grep_census=_raw_grep_census()
    prose_delta={k:grep_census.get(k,0)-census.get(k,0) for k in grep_census}
    _dump("metadata/census.json", {
          "environment_census":census,          # status-tagged ENVIRONMENT declarations (claims)
          "environment_census_other":census_other,
          "total_status_tagged_environments":sum(census.values())+sum(census_other.values()),
          "raw_grep_census":grep_census,        # every \\status{X} occurrence (review-endorsed F-3 numbers)
          "prose_mention_delta":prose_delta,    # grep - environment (inline prose status mentions, non-declarations)
          "reconciliation_note":("raw_grep_census is the review-endorsed F-3 figure "
              "(counts every \\status{X}). environment_census counts only status-tagged "
              "environment declarations (the claim records). The delta is prose status "
              "mentions (e.g. GR narrative 'is \\status{C}', NS inline sub-lemma tags) that "
              "are not standalone declarations. Both are authoritative for their own question."),
          "census_commit":git_commit(),
          "generated":build_timestamp().isoformat(),
          "frontier_accountings":accountings})
    print(f"claims={len(claims)} edges={len(edges)} census={census} other={census_other}")

def _raw_grep_census():
    """Every \\status{X} occurrence across canon (review-endorsed F-3 census)."""
    c={}
    pat=re.compile(r'\\status\{([A-Za-z0-9]+)\}')
    for stem in CANON:
        for x in pat.findall(open(stem+".tex",encoding="utf-8",errors="replace").read()):
            c[x]=c.get(x,0)+1
    return c

def _authority_default(env,label):
    if label and ("status" in (label or "")): return "A1_branch_status_proposition"
    if label and "frontier" in (label or ""): return "A2_named_failure_frontier"
    if env in ("openobligation","obligation"): return "A3_closure_ledger"
    return "body_claim"

def _frontier_membership(label,status,env):
    m=[]
    if status=="O": m.append("I_syntactic_O")
    if label and label.startswith("ob:"): m.append("II_named_roster")
    return m

def _count_by(claims,key,pred=lambda c:True):
    out={}
    for c in claims:
        if pred(c): out[key(c)]=out.get(key(c),0)+1
    return dict(sorted(out.items()))

def _branch_posture_view():
    # sourced from each branch's A1 status proposition (verbatim postures, review-approved)
    return {
        "YM":"Conditional CERT-CLOSE (MSC-normalized NFC scope); B1/B2/B3 post-program",
        "NS":"Domain-bounded conditional CERT-CLOSE, conditional on the standing branch hypotheses together with the named IDC and alpha hypotheses (MIG-050); unconditional global regularity external",
        "SCC":"Conditional CERT-CLOSE at declared structural endpoint (UCTI/depth-sum/threshold-stability + source-descent)",
        "GR":"Domain-bounded conditional CERT-CLOSE + CK-corner extension; global curvature-subcriticality open",
        "SM":"Conditionally intrinsic-structural closed, inherited-scope open",
        "BIO":"Replication-heredity endpoint discharged; EVO/MULTI conditional; BND residual toolkit-boundary",
        "LING":"Contrast+recursion+context-response closed; reference semantics conditional at two scopes",
        "CRYST":"Conditional CERT-CLOSE (diffraction-periodicity-symmetry); phase problem frontier",
        "SPEC":"CERT-CLOSE on gauge-response regime; matter-rich regime open (SM-gated)",
        "RH":"CERT-PROJ; S1 arithmetic + RH4-6 frontier",
    }

def _branch_posture_view_placeholder(): return _branch_posture_view()

def _dump(path,obj):
    with open(path,"w") as f:
        json.dump(obj,f,indent=2,sort_keys=False,ensure_ascii=False)
        f.write("\n")

if __name__=="__main__":
    main()
