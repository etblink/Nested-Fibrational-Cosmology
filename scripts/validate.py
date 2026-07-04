#!/usr/bin/env python3
"""
NFC canon validation suite (Phase 5) — the promoted, repeatable version of the
Phase-0 ad-hoc audit. Structural checks only (no compile); the compile gate is a
separate step in Makefile. Exit code 0 = pass, non-zero = fail (for CI / edit gate).

Checks:
  1. Label uniqueness within the corpus label namespace, minus a known-benign allowlist.
  2. Dangling references (ref -> label never defined) MUST be 0.
  3. Proof-citation dependency cycles MUST be 0.
  4. Census stability: re-derive the raw \\status census and compare to a pinned
     expected value (guards against accidental status-tag edits during Phase 7).
  5. cap:* capsule labels MUST be unique corpus-wide (no capsule collisions).
"""
import re,glob,sys,json,collections

CANON=sorted(glob.glob("*.tex"))
label_re=re.compile(r'\\label\{([^}]*)\}')
ref_re=re.compile(r'\\(?:ref|eqref|cref|Cref)\{([^}]*)\}')
status_re=re.compile(r'\\status\{([A-Za-z0-9]+)\}')
STMT=['theorem','proposition','corollary','lemma']

# Known-benign duplicate labels (documented in AUDIT_BASELINE / roster). New dups fail.
BENIGN_DUP={
 "cor:conditional-no-unconditional","def:transport-invariant","sec:arena","sec:descent",
 "sec:frontier","sec:governance","sec:imports","sec:ledger","sec:rh-screening","sec:status",
 "sec:transfer","thm:governing",
}
# Pinned expected raw \status census. Update ONLY via migration.
# MIG-007: R 349->366 (+17) for the 17 Current Status Capsules (Phase 7).
# MIG-008: U 212->211, C 748->749 for prop:scc-status [U]->[C] (C-2 correction, weakening).
EXPECTED_CENSUS={"D":461,"U":211,"C":749,"B":9,"O":5,"R":366}

def brace_body(text,env,start):
    m=re.search(r'\\end\{'+re.escape(env)+r'\}',text[start:])
    return (text[start:start+m.start()],start+m.end()) if m else (text[start:],len(text))

def main():
    fails=[]
    defs=collections.defaultdict(list); refs=collections.defaultdict(list)
    census=collections.Counter(); edges=[]
    for fn in CANON:
        t=open(fn,encoding="utf-8",errors="replace").read()
        for m in label_re.finditer(t): defs[m.group(1)].append(fn)
        for m in ref_re.finditer(t): refs[m.group(1)].append(fn)
        for m in status_re.finditer(t): census[m.group(1)]+=1
        for env in STMT:
            for bm in re.finditer(r'\\begin\{'+env+r'\}',t):
                body,end=brace_body(t,env,bm.end())
                lm=label_re.search(body)
                if not lm: continue
                look=t[end:end+2500]; pm=re.search(r'\\begin\{proof\}',look)
                if pm and pm.start()<400:
                    pb,_=brace_body(t,"proof",end+pm.end())
                    for d in set(ref_re.findall(pb)): edges.append((lm.group(1),d))

    # 1. duplicate labels
    dups={k:v for k,v in defs.items() if len(v)>1 and k not in BENIGN_DUP}
    if dups: fails.append(f"UNEXPECTED duplicate labels: {dups}")
    # 5. capsule uniqueness
    cap_dups={k:v for k,v in defs.items() if k.startswith("cap:") and len(v)>1}
    if cap_dups: fails.append(f"capsule label collision: {cap_dups}")
    # 2. dangling refs
    dangling=sorted(k for k in refs if k not in defs)
    if dangling: fails.append(f"dangling references ({len(dangling)}): {dangling[:20]}")
    # 3. cycles
    import networkx as nx
    G=nx.DiGraph(); G.add_edges_from(edges)
    cyc=list(nx.simple_cycles(G))
    if cyc: fails.append(f"proof-citation cycles ({len(cyc)}): {cyc[:5]}")
    # 4. census stability
    cen=dict(census)
    if cen!=EXPECTED_CENSUS:
        diff={k:(cen.get(k,0),EXPECTED_CENSUS.get(k,0)) for k in set(cen)|set(EXPECTED_CENSUS) if cen.get(k,0)!=EXPECTED_CENSUS.get(k,0)}
        fails.append(f"census drift (got,expected): {diff}  -- if intentional, update EXPECTED_CENSUS via migration")

    # 6. no non-comment content after \end{document}
    tail_offenders={}
    for fn in CANON:
        t=open(fn,encoding="utf-8",errors="replace").read()
        if "\\end{document}" in t:
            tail=t.split("\\end{document}",1)[1]
            live=[l for l in tail.splitlines() if l.strip() and not l.strip().startswith("%")]
            if live: tail_offenders[fn]=live[:3]
    if tail_offenders: fails.append(f"non-comment content after \\end{{document}}: {tail_offenders}")

    # 7. ledger display-status cells must match the declared \status of the referenced label.
    # Declarations are resolved PER FILE (LaTeX \ref resolves within the compiled file;
    # the known benign duplicate labels otherwise cause cross-file false positives).
    ledger_mismatch=[]
    envdecl=re.compile(r'\\begin\{\w+\}\[\\status\{([A-Z])\}\]\\label\{([^}]*)\}')
    rowpat=re.compile(r'\\ref\{([^}]*)\}[^\n]*\n?[^\n&]*&\s*\[([DUCBOR])\]\s*&')
    for fn in CANON:
        t=open(fn,encoding="utf-8",errors="replace").read()
        declared={m.group(2):m.group(1) for m in envdecl.finditer(t)}
        for m in rowpat.finditer(t):
            lbl,cell=m.group(1),m.group(2)
            if lbl in declared and declared[lbl]!=cell:
                ledger_mismatch.append(f"{fn}: row \\ref{{{lbl}}} shows [{cell}] but declaration is [{declared[lbl]}]")
    if ledger_mismatch: fails.append("ledger display-status mismatches:\n    "+"\n    ".join(ledger_mismatch))

    # 8. Weil certificates (MIG-025): decimal endpoints must satisfy 0 < lower <= upper
    # for every ball whose sign is claimed positive; endpoints parsed from the JSON strings.
    import os as _os, json as _json
    from decimal import Decimal as _D
    def _check_ball(tag, ball):
        lo, up = _D(ball["lower_decimal"]), _D(ball["upper_decimal"])
        if not (lo <= up): return f"{tag}: lower > upper"
        if ball.get("sign_certified") == "positive" and not (lo > 0):
            return f"{tag}: claimed positive but lower <= 0"
        return None
    cert_issues=[]
    if _os.path.exists("metadata/weil_M3_result.json"):
        c=_json.load(open("metadata/weil_M3_result.json"))
        e=_check_ball("M3", c["M3_ball"]);  cert_issues += [e] if e else []
        if c["M3_ball"].get("sign_certified") != "positive":
            cert_issues.append("M3: sign not certified positive")
    if _os.path.exists("metadata/weil_M4_certificate.json"):
        c=_json.load(open("metadata/weil_M4_certificate.json"))
        for i,b in enumerate(c["ldl_pivots"]):
            e=_check_ball(f"M4 pivot {i}", b);  cert_issues += [e] if e else []
        for i,b in enumerate(c["eigenvalue_enclosures"]):
            e=_check_ball(f"M4 eig {i}", b);  cert_issues += [e] if e else []
    if _os.path.exists("metadata/weil_Q12_certificates.json"):
        c=_json.load(open("metadata/weil_Q12_certificates.json"))
        for n,r in c["results"].items():
            if r["ldl_status"]=="PD":
                for i,b in enumerate(r["pivots"]):
                    e=_check_ball(f"Q{n} pivot {i}", b);  cert_issues += [e] if e else []
    if cert_issues: fails.append("Weil certificate endpoint failures:\n    "+"\n    ".join(cert_issues))

    report={"labels":sum(len(v) for v in defs.values()),"unique_labels":len(defs),
            "benign_dups_present":sorted(k for k in defs if len(defs[k])>1 and k in BENIGN_DUP),
            "dangling":len(dangling),"cycles":len(cyc),"census":cen,"pass":not fails}
    print(json.dumps(report,indent=2))
    if fails:
        print("\nVALIDATION FAILED:",file=sys.stderr)
        for f in fails: print("  -",f,file=sys.stderr)
        sys.exit(1)
    print("\nVALIDATION PASSED")

if __name__=="__main__": main()
