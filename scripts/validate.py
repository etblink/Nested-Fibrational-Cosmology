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

    # 8. Weil certificates (MIG-026 hardened): (a) reconstruct the EXACT dyadic ball and
    # prove the decimal endpoints enclose mid +/- radius; (b) every pivot under ldl_status
    # PD, and every eigenvalue under an all-positive claim, must have strictly positive
    # lower endpoint AND sign_certified == "positive".
    import os as _os, json as _json
    from fractions import Fraction as _F
    from decimal import Decimal as _D
    def _dec_to_frac(s):
        d = _D(s); sign, digits, exp = d.as_tuple()
        n = int(''.join(map(str, digits))) * (-1 if sign else 1)
        return _F(n) * (_F(10) ** exp if exp >= 0 else _F(1, 10 ** (-exp)))
    def _dy_to_frac(dy):
        man, ex = int(dy["mantissa"]), int(dy["exponent"])
        return _F(man) * (_F(2) ** ex if ex >= 0 else _F(1, 2 ** (-ex)))
    def _check_ball(tag, ball, require_positive):
        errs = []
        try:
            mid, rad = _dy_to_frac(ball["mid_dyadic"]), _dy_to_frac(ball["radius_dyadic"])
        except KeyError:
            return [f"{tag}: exact dyadics missing (pre-MIG-026 certificate)"]
        lo, up = _dec_to_frac(ball["lower_decimal"]), _dec_to_frac(ball["upper_decimal"])
        if not (lo <= mid - rad and mid + rad <= up):
            errs.append(f"{tag}: decimal endpoints do NOT enclose exact dyadic ball")
        if not (lo <= up): errs.append(f"{tag}: lower > upper")
        if require_positive:
            if not (lo > 0): errs.append(f"{tag}: required positive but lower <= 0")
            if ball.get("sign_certified") != "positive":
                errs.append(f"{tag}: required positive but sign_certified != positive")
        return errs
    cert_issues=[]
    if _os.path.exists("metadata/weil_M3_result.json"):
        c=_json.load(open("metadata/weil_M3_result.json"))
        cert_issues += _check_ball("M3", c["M3_ball"], require_positive=True)
    if _os.path.exists("metadata/weil_M4_certificate.json"):
        c=_json.load(open("metadata/weil_M4_certificate.json"))
        pd = c.get("ldl_status") == "PD"
        for i,b in enumerate(c["ldl_pivots"]):
            cert_issues += _check_ball(f"M4 pivot {i}", b, require_positive=pd)
        allpos = c.get("all_eigenvalues_certified_positive", False)
        for i,b in enumerate(c["eigenvalue_enclosures"]):
            cert_issues += _check_ball(f"M4 eig {i}", b, require_positive=allpos)
    if _os.path.exists("metadata/weil_Q12_certificates.json"):
        c=_json.load(open("metadata/weil_Q12_certificates.json"))
        for n,r in c["results"].items():
            pd = r["ldl_status"] == "PD"
            for i,b in enumerate(r["pivots"]):
                cert_issues += _check_ball(f"Q{n} pivot {i}", b, require_positive=pd)
    # rational-height QH certificates (MIG-031): reconstruct the rational set, verify reduction
    # and uniqueness, verify BOTH moment identities exactly, require PD pivots strictly positive.
    from fractions import Fraction as _Frac2
    from math import gcd as _gcd2
    for _fn in sorted(_os.listdir("metadata")) if _os.path.isdir("metadata") else []:
        if not (_fn.startswith("weil_QH") and _fn.endswith("_certificate.json")): continue
        c=_json.load(open(f"metadata/{_fn}"))
        sc=[_Frac2(a,b) for a,b in c["scales"]]
        # reduction + uniqueness
        for a,b in c["scales"]:
            if _gcd2(a,b)!=1: cert_issues.append(f"{_fn}: scale {a}/{b} not reduced")
        if len(set(sc))!=len(sc): cert_issues.append(f"{_fn}: duplicate scales")
        # both moment identities exactly, for every basis vector
        for k,vec in enumerate(c["basis"]):
            if sum(vec)!=0:
                cert_issues.append(f"{_fn}: basis[{k}] sum c != 0")
            if sum(_Frac2(v,1)/s for v,s in zip(vec,sc))!=0:
                cert_issues.append(f"{_fn}: basis[{k}] sum c/q != 0")
        pd = c["ldl_status"]=="PD"
        for i,b in enumerate(c["pivots"]):
            cert_issues += _check_ball(f"{_fn} pivot {i}", b, require_positive=pd)
    if cert_issues: fails.append("Weil certificate failures:\n    "+"\n    ".join(cert_issues))

    # 9. strict UTF-8 over all tracked text files (MIG-026 item 1; MIG-028 git-free).
    # Source of the file list: git ls-files when a git repo is present, else the
    # packaged manifest release/TRACKED_TEXT_MANIFEST.txt. The check is NEVER skipped;
    # if neither source is available that is itself a failure.
    import subprocess as _sp, os as _os2
    tracked=None
    if _os2.path.isdir(".git"):
        try:
            tracked=_sp.check_output(["git","ls-files"], stderr=_sp.DEVNULL).decode().splitlines()
        except Exception:
            tracked=None
    if tracked is None:
        man="release/TRACKED_TEXT_MANIFEST.txt"
        if _os2.path.exists(man):
            tracked=[l.strip() for l in open(man, encoding="utf-8") if l.strip()]
        else:
            fails.append("check 9: no git repo and no release/TRACKED_TEXT_MANIFEST.txt — cannot enumerate tracked text files (UTF-8 check not skipped)")
            tracked=[]
    bad_utf8=[]
    for fn in tracked:
        if fn.endswith((".pdf",".pyc",".png",".zip",".bundle")): continue
        try:
            open(fn,"rb").read().decode("utf-8")
        except UnicodeDecodeError as e:
            bad_utf8.append(f"{fn} @ byte {e.start}")
        except FileNotFoundError:
            pass
    if bad_utf8: fails.append("strict UTF-8 failures: "+", ".join(bad_utf8))

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
