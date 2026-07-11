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
EXPECTED_CENSUS={"D":461,"U":211,"C":749,"B":9,"O":6,"R":366}

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
        # MIG-037 (item 1): a negative radius defeats the perturbation-bound semantics
        # (||R||_inf row sums would be invalid). Reject before any enclosure/row-sum use.
        if rad < 0:
            errs.append(f"{tag}: radius_dyadic is negative")
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

    # ---- MIG-035: independent interval arithmetic (Fraction-based; no flint dependency,
    # so the git-free release environment can run it) for the H=4/H=5 matrix + eigenvalue
    # certificate checks. Each interval is an exact [lo, hi] pair of Fractions. ----
    class _Iv:
        __slots__=("lo","hi")
        def __init__(s,lo,hi): s.lo,s.hi=lo,hi
        def __add__(s,o): return _Iv(s.lo+o.lo, s.hi+o.hi)
        def __sub__(s,o): return _Iv(s.lo-o.hi, s.hi-o.lo)
        def __mul__(s,o):
            ps=(s.lo*o.lo, s.lo*o.hi, s.hi*o.lo, s.hi*o.hi); return _Iv(min(ps),max(ps))
        def __truediv__(s,o):
            if o.lo<=0<=o.hi: raise ZeroDivisionError("interval divisor contains 0")
            r=_Iv(_F(1)/o.hi, _F(1)/o.lo); return s*r
        def pos(s): return s.lo>0
        def contains(s,x): return s.lo<=x<=s.hi
        def overlaps(s,o): return s.lo<=o.hi and o.lo<=s.hi
    def _ball_iv(b):
        return _Iv(_dec_to_frac(b["lower_decimal"]), _dec_to_frac(b["upper_decimal"]))
    def _dy_rad(b):
        r = _dy_to_frac(b["radius_dyadic"])
        if r < 0:
            raise ValueError("negative radius_dyadic in matrix entry")
        return r

    def _mig035_checks(_fn, c):
        errs=[]
        if "compressed_matrix_balls" not in c:
            return errs  # not a MIG-035 full-matrix certificate (e.g. QH2/QH3); other checks cover it
        m=c.get("dim")
        B=c["compressed_matrix_balls"]
        # (i) dimension = |Q_H|-2 and full m*m serialized
        want={f"{a}_{b}" for a in range(m) for b in range(m)}
        if set(B.keys())!=want:
            errs.append(f"{_fn}: compressed_matrix_balls keys != full {m}x{m} grid"); return errs
        # every entry ball must enclose its own exact dyadic (catches a narrowed entry ball)
        for key,b in B.items():
            errs += _check_ball(f"{_fn} M[{key}]", b, require_positive=False)
        # (ii) Hermitian-compatibility: M_jk == M_kj (equal dyadic mid & rad; real => conj trivial)
        for a in range(m):
            for b in range(a+1,m):
                jk,kj=B[f"{a}_{b}"],B[f"{b}_{a}"]
                if (jk["mid_dyadic"],jk["radius_dyadic"])!=(kj["mid_dyadic"],kj["radius_dyadic"]):
                    errs.append(f"{_fn}: non-Hermitian pair M[{a}_{b}] != M[{b}_{a}]")
        if errs: return errs
        # (iii) primary matrix identified; the engine's interval LDL is the PD certificate.
        # Independent ties below (trace, det, positivity) bind pivots<->eigenvalues<->matrix
        # without re-deriving the ~1e-64 pivots (beyond a 40-digit serialization's reach).
        if c.get("primary_matrix")!="compressed":
            errs.append(f"{_fn}: primary_matrix not identified as 'compressed'")
        claimed_pd = c.get("ldl_status")=="PD"
        if claimed_pd and not all(_ball_iv(b).pos() for b in c["pivots"]):
            errs.append(f"{_fn}: claims LDL PD but a serialized pivot lower endpoint is not > 0")
        # (iv) MIG-036 PRIMARY binding: exact rational residual certificate ties the
        # serialized eigenvalue enclosures to the eigenvalues of the serialized midpoint A_0.
        # Reconstruct A_0 (exact dyadic midpoints) and ||R||_inf from the serialized matrix.
        A0=[[_dy_to_frac(B[f"{i}_{j}"]["mid_dyadic"]) for j in range(m)] for i in range(m)]
        # MIG-037 (item 1): reject negative matrix radii cleanly (no traceback) before the
        # row-sum; a negative radius would corrupt ||R||_inf and the perturbation bound.
        try:
            Rinf_recomputed=max(sum(_dy_rad(B[f"{a}_{b}"]) for b in range(m)) for a in range(m))
        except ValueError as ex:
            errs.append(f"{_fn}: {ex}"); return errs
        if Rinf_recomputed < 0:
            errs.append(f"{_fn}: recomputed ||R||_inf is negative"); return errs
        ec=c.get("eigenvalue_certificate")
        E=c.get("eigenvalue_enclosures",[])
        if not ec or "eigenpairs" not in ec:
            errs.append(f"{_fn}: missing eigenvalue_certificate.eigenpairs (MIG-036 residual proof required)"); return errs
        pairs=ec["eigenpairs"]
        if len(pairs)!=m or len(E)!=m:
            errs.append(f"{_fn}: eigenpairs/enclosures count != dim {m}"); return errs
        # recorded ||R||_inf must be a valid (>=) upper bound
        Rinf_claimed=_dec_to_frac(ec["R_inf_upper"]["upper_decimal"])
        if Rinf_claimed < Rinf_recomputed:
            errs.append(f"{_fn}: recorded ||R||_inf < recomputed (invalid Weyl bound)"); return errs
        thetas=[]; intervals=[]
        for idx,pr in enumerate(pairs):
            # MIG-037 (item 2): witness vector must be exactly dim dyadic coordinates
            # (a surplus/short coordinate makes v not an element of the m-dim matrix space).
            vlist=pr.get("v")
            if not isinstance(vlist,list) or len(vlist)!=m:
                errs.append(f"{_fn}: eig {idx} witness vector has {len(vlist) if isinstance(vlist,list) else 'non-list'} coords != dim {m}"); return errs
            v=[_dy_to_frac(d) for d in vlist]
            rho=_dy_to_frac(pr["rho"])
            if rho<0: errs.append(f"{_fn}: eig {idx} rho negative"); return errs
            if all(x==0 for x in v):
                errs.append(f"{_fn}: eig {idx} residual vector is zero"); return errs
            s=sum(x*x for x in v)
            Av=[sum(A0[i][j]*v[j] for j in range(m)) for i in range(m)]
            p=sum(v[i]*Av[i] for i in range(m))
            w=[s*Av[i]-p*v[i] for i in range(m)]
            w2=sum(x*x for x in w)
            # Hermitian residual bound: ||w||^2 <= rho^2 s^3  <=>  ||A0 v - theta v|| <= rho ||v||
            if w2 > rho*rho*s**3:
                errs.append(f"{_fn}: eig {idx} residual bound violated (||r|| > rho): counterfeit"); return errs
            theta=_F(p,s)
            lo_t,hi_t=theta-rho,theta+rho
            # MIG-037 (item 3): residual interval must be well-formed
            if lo_t>hi_t:
                errs.append(f"{_fn}: eig {idx} residual interval lower > upper"); return errs
            thetas.append(theta); intervals.append((lo_t, hi_t, rho))
        # disjoint and strictly ordered (exact rational) -> n intervals exhaust the n-point spectrum
        for i in range(1,m):
            if not (intervals[i][0] > intervals[i-1][1]):
                errs.append(f"{_fn}: midpoint eigenvalue intervals not disjoint/ordered at {i} (spectrum not exhausted)"); return errs
        # widen by ||R||_inf (Weyl) and bind to the serialized enclosures; positivity = PRIMARY PD proof
        allpos=c.get("all_eigenvalues_certified_positive",False)
        for i,(lo_t,hi_t,rho) in enumerate(intervals):
            wlo=lo_t-Rinf_recomputed; whi=hi_t+Rinf_recomputed
            if wlo>whi:  # MIG-037 (item 3): widened interval must be well-formed
                errs.append(f"{_fn}: eig {i} widened interval lower > upper"); return errs
            ser_lo=_dec_to_frac(E[i]["lower_decimal"]); ser_hi=_dec_to_frac(E[i]["upper_decimal"])
            if ser_lo>ser_hi:
                errs.append(f"{_fn}: eig {i} serialized enclosure lower > upper"); return errs
            if ser_lo>wlo or ser_hi<whi:
                errs.append(f"{_fn}: serialized eig enclosure {i} does not outward-contain the residual-certified widened interval")
            if allpos and (wlo<=0 or ser_lo<=0):
                errs.append(f"{_fn}: eig {i} lower endpoint <= 0 under all-positive claim (PD fails)")
        # inertia agreement (LDL pivots are a redundant cross-check per MIG-036)
        pos_piv=sum(1 for b in c["pivots"] if _ball_iv(b).pos())
        inertia=c.get("inertia",{})
        if not (pos_piv==m and inertia.get("agree") is True
                and inertia.get("ldl_positive_pivots")==m and inertia.get("eig_positive")==m):
            errs.append(f"{_fn}: LDL/eigenvalue inertia disagreement (piv+={pos_piv}, dim={m}, inertia={inertia})")
        # (v) SECONDARY sanity only (necessary, not sufficient; the residual cert above is the binding):
        # trace overlap and det-product overlap, using the residual-derived intervals.
        Ivs=[_Iv(_dec_to_frac(E[i]["lower_decimal"]), _dec_to_frac(E[i]["upper_decimal"])) for i in range(m)]
        tr=_Iv(_F(0),_F(0))
        for i in range(m): tr=tr+_ball_iv(B[f"{i}_{i}"])
        se=_Iv(_F(0),_F(0))
        for iv in Ivs: se=se+iv
        if not tr.overlaps(se):
            errs.append(f"{_fn}: [sanity] trace enclosure disjoint from sum(eigenvalues)")
        # --- MIG-044 item E: residual-provenance validation (only for certificates that
        # carry the new fields; pre-MIG-044 certificates, e.g. H<=7, are unaffected). ---
        if "midpoint_matrix_sha256" in ec:
            import hashlib as _hashlib
            CANON_V = "MIG044-canon-v1"
            def _cdy(d): return f"{int(d['mantissa'])}:{int(d['exponent'])}"
            # E.4: recompute the canonical midpoint-matrix hash from the SERIALIZED matrix
            mid_parts = [_cdy(B[f"{i}_{j}"]["mid_dyadic"]) for i in range(m) for j in range(m)]
            recomputed_mid_hash = _hashlib.sha256((CANON_V + "|MID|" + ";".join(mid_parts)).encode("ascii")).hexdigest()
            if recomputed_mid_hash != ec["midpoint_matrix_sha256"]:
                errs.append(f"{_fn}: recomputed midpoint_matrix_sha256 does not match serialized matrix (counterfeit)")
            # E.5: recompute the canonical ordered-witness hash from the SERIALIZED witnesses
            wit_rows = [",".join(_cdy(d) for d in pr["v"]) for pr in pairs]
            recomputed_wit_hash = _hashlib.sha256((CANON_V + "|WIT|" + "|".join(wit_rows)).encode("ascii")).hexdigest()
            if recomputed_wit_hash != ec["ordered_witness_sha256"]:
                errs.append(f"{_fn}: recomputed ordered_witness_sha256 does not match serialized witnesses (counterfeit)")
            # E.3: certificate generator hash equals the actual generator file (if accessible)
            try:
                actual_gen_hash = _hashlib.sha256(open("scripts/weil_engine.py", "rb").read()).hexdigest()
                if c.get("provenance", {}).get("generator_script_sha256") != actual_gen_hash:
                    errs.append(f"{_fn}: certificate generator_script_sha256 does not match scripts/weil_engine.py")
            except FileNotFoundError:
                pass
            # E.7: multiplier belongs to the declared multiplier ladder
            mult = ec.get("eigenvector_multiplier")
            if mult not in (3, 6, 12, 20):
                errs.append(f"{_fn}: eigenvector_multiplier {mult} not in declared ladder (3,6,12,20)")
            # E.8: working precision == profile bits * multiplier
            wprec = ec.get("eigenvector_working_precision_bits")
            pbits = c.get("profile", {}).get("bits")
            if wprec != (pbits * mult if isinstance(mult, int) and isinstance(pbits, int) else None):
                errs.append(f"{_fn}: eigenvector_working_precision_bits {wprec} != profile bits {pbits} * multiplier {mult}")
            # E.9: selected B belongs to the deterministic resolution ladder and satisfies B <= working precision
            Bsel = ec.get("residual_resolution_bits")
            ladder_vals = {320, 640, 1280, 2560, 5120, 10240, 20480}
            if not (isinstance(Bsel, int) and isinstance(wprec, int) and Bsel <= wprec and (Bsel in ladder_vals or Bsel == wprec)):
                errs.append(f"{_fn}: residual_resolution_bits {Bsel} not on the deterministic ladder or exceeds working precision {wprec}")
        return errs

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
    # rational-height QH certificates (MIG-031; MIG-032 hardened): reconstruct the EXPECTED
    # ordered Q_H from H and require equality; check dim, basis rank, full two-moment nullspace
    # spanning, ratio/profile agreement, and filename<->H<->scales consistency.
    from fractions import Fraction as _Frac2
    from math import gcd as _gcd2
    def _q_height(H):
        S={_Frac2(m,n) for m in range(1,H+1) for n in range(1,H+1) if _gcd2(m,n)==1}
        anchors=[_Frac2(1),_Frac2(2)]
        rest=sorted((s for s in S if s not in anchors), key=lambda s:(max(abs(s.numerator),s.denominator),s))
        return [a for a in anchors if a in S]+rest
    def _rank_mod_p(rows, ncols, p=2147483647):
        # exact rank over F_p of an integer matrix given as list of row lists
        M=[[x % p for x in row] for row in rows]; rank=0; r=0
        for c in range(ncols):
            piv=None
            for i in range(r,len(M)):
                if M[i][c]%p!=0: piv=i; break
            if piv is None: continue
            M[r],M[piv]=M[piv],M[r]
            inv=pow(M[r][c],p-2,p)
            M[r]=[(x*inv)%p for x in M[r]]
            for i in range(len(M)):
                if i!=r and M[i][c]%p!=0:
                    f=M[i][c]; M[i]=[(a-f*b)%p for a,b in zip(M[i],M[r])]
            r+=1; rank+=1
            if r==len(M): break
        return rank
    for _fn in sorted(_os.listdir("metadata")) if _os.path.isdir("metadata") else []:
        if not (_fn.startswith("weil_QH") and _fn.endswith("_certificate.json")): continue
        c=_json.load(open(f"metadata/{_fn}"))
        H=c.get("H")
        # filename height <-> JSON H
        import re as _re
        mfn=_re.search(r"weil_QH(\d+)_certificate", _fn)
        if mfn and int(mfn.group(1))!=H:
            cert_issues.append(f"{_fn}: filename height {mfn.group(1)} != JSON H {H}")
        sc=[_Frac2(a,b) for a,b in c["scales"]]
        # reduction + uniqueness
        for a,b in c["scales"]:
            if _gcd2(a,b)!=1: cert_issues.append(f"{_fn}: scale {a}/{b} not reduced")
        if len(set(sc))!=len(sc): cert_issues.append(f"{_fn}: duplicate scales")
        # EXPECTED ordered Q_H equality (defeats counterfeit substitution)
        if H is not None:
            exp=_q_height(H)
            if sc!=exp:
                cert_issues.append(f"{_fn}: scales != deterministic Q_height({H}) (order/content mismatch)")
        # dim = |Q_H| - 2
        if c.get("dim")!=len(sc)-2:
            cert_issues.append(f"{_fn}: dim {c.get('dim')} != |Q_H|-2 = {len(sc)-2}")
        # basis: exactly dim vectors, correct length, both moments exact, full rank = dim,
        # and spans the entire two-moment nullspace (nullspace dim = len(sc)-2)
        B=c["basis"]
        if len(B)!=c.get("dim"):
            cert_issues.append(f"{_fn}: basis has {len(B)} vectors, dim={c.get('dim')}")
        for k,vec in enumerate(B):
            if len(vec)!=len(sc):
                cert_issues.append(f"{_fn}: basis[{k}] length {len(vec)} != #scales {len(sc)}")
                continue
            if sum(vec)!=0:
                cert_issues.append(f"{_fn}: basis[{k}] sum c != 0")
            if sum(_Frac2(v,1)/s for v,s in zip(vec,sc))!=0:
                cert_issues.append(f"{_fn}: basis[{k}] sum c/q != 0")
        if B and all(len(v)==len(sc) for v in B):
            rk=_rank_mod_p(B, len(sc))
            if rk!=len(B):
                cert_issues.append(f"{_fn}: basis rank {rk} != #vectors {len(B)} (dependent)")
            if rk!=len(sc)-2:
                cert_issues.append(f"{_fn}: basis rank {rk} != nullspace dim {len(sc)-2} (does not span two-moment nullspace)")
        # recorded ratio agreement (max/min of scales)
        if "max_min_ratio" in c:
            rr=_Frac2(*c["max_min_ratio"]); exp_r=max(sc)/min(sc)
            if rr!=exp_r: cert_issues.append(f"{_fn}: recorded ratio {rr} != max/min {exp_r}")
        # MIG-033: dynamic precision guard. profile.max_scale_ratio feeds the elevated
        # S_m-table precision, so it MUST equal the engine's exact rule
        #   max_scale_ratio = max(2, ceil(max Q_H / min Q_H) + 1)   (= H^2 + 1 for Q_H),
        # and the profile MUST agree with provenance on bits/N/M. Previously only
        # max_min_ratio was checked; a tampered profile.max_scale_ratio passed.
        from math import ceil as _ceil2
        prof = c.get("profile"); prov = c.get("provenance")
        if not isinstance(prof, dict):
            cert_issues.append(f"{_fn}: profile block missing")
        elif not isinstance(prov, dict):
            cert_issues.append(f"{_fn}: provenance block missing")
        else:
            exp_msr = max(2, _ceil2(max(sc)/min(sc)) + 1)
            if prof.get("max_scale_ratio") != exp_msr:
                cert_issues.append(f"{_fn}: profile.max_scale_ratio {prof.get('max_scale_ratio')} != ceil(max/min)+1 = {exp_msr}")
            if H is not None and exp_msr != H*H + 1:
                cert_issues.append(f"{_fn}: ceil(max/min)+1 = {exp_msr} != H^2+1 = {H*H+1} (Q_H ratio invariant broken)")
            for pk, vk in (("bits","precision_bits"), ("N","prime_head_N"), ("M","prime_tail_M")):
                if prof.get(pk) != prov.get(vk):
                    cert_issues.append(f"{_fn}: profile.{pk} {prof.get(pk)} != provenance.{vk} {prov.get(vk)}")
        # PD pivots strictly positive
        pd=c["ldl_status"]=="PD"
        for i,b in enumerate(c["pivots"]):
            cert_issues += _check_ball(f"{_fn} pivot {i}", b, require_positive=pd)
        # MIG-035: full compressed matrix, eigenvalue enclosures, nesting, inertia, Weyl
        cert_issues += _mig035_checks(_fn, c)
        # MIG-035: nesting proof (Q_{H-1} ordered prefix of Q_H) when present
        nst=c.get("nesting")
        if isinstance(nst,dict) and nst.get("previous_H") is not None and not nst.get("prefix_verified"):
            cert_issues.append(f"{_fn}: nesting.prefix_verified is not True")
    if cert_issues: fails.append("Weil certificate failures:\n    "+"\n    ".join(cert_issues))

    # 7b. MIG-044: residual-resolution diagnostic artifact validation (weil_QH*_residual_diagnostic.json).
    # A diagnostic file is supplemental evidence, never itself a positivity certificate; it is
    # validated for (i) internal self-consistency (self-hash) and (ii) binding to the delivered
    # generator and to the certificate it supports (load-bearing candidate's matrix/witness hashes).
    diag_issues=[]
    import hashlib as _hashlib2, os as _os3, re as _re4
    for _dfn in (sorted(_os3.listdir("metadata")) if _os3.path.isdir("metadata") else []):
        if not (_dfn.startswith("weil_QH") and _dfn.endswith("_residual_diagnostic.json")): continue
        d=_json.load(open(f"metadata/{_dfn}"))
        # E.1: diagnostic self-hash recomputable after excluding only the self-hash field
        claimed=d.get("diagnostic_sha256")
        recomputed=_hashlib2.sha256(
            _json.dumps({k:v for k,v in d.items() if k!="diagnostic_sha256"}, sort_keys=True).encode()
        ).hexdigest()
        if claimed!=recomputed:
            diag_issues.append(f"{_dfn}: diagnostic_sha256 does not match recomputation from its own contents")
        # E.2: diagnostic generator hash equals the actual generator file
        try:
            actual_gen=_hashlib2.sha256(open("scripts/weil_engine.py","rb").read()).hexdigest()
            if d.get("generator_sha256")!=actual_gen:
                diag_issues.append(f"{_dfn}: generator_sha256 does not match scripts/weil_engine.py")
        except FileNotFoundError:
            pass
        # E.6: the load-bearing candidate's matrix/witness hashes equal the certificate's
        lb=d.get("load_bearing_candidate")
        if isinstance(lb, dict):
            hnum=_re4.search(r"weil_QH(\d+)_residual_diagnostic", _dfn)
            if hnum:
                _certpath=f"metadata/weil_QH{hnum.group(1)}_certificate.json"
                if _os3.path.exists(_certpath):
                    _cert=_json.load(open(_certpath))
                    _cec=_cert.get("eigenvalue_certificate",{})
                    if lb.get("midpoint_matrix_sha256")!=_cec.get("midpoint_matrix_sha256"):
                        diag_issues.append(f"{_dfn}: load_bearing_candidate midpoint hash does not match {_certpath}")
                    if lb.get("ordered_witness_sha256")!=_cec.get("ordered_witness_sha256"):
                        diag_issues.append(f"{_dfn}: load_bearing_candidate witness hash does not match {_certpath}")
                    if not (lb.get("midpoint_hash_matches_certificate") and lb.get("witness_hash_matches_certificate")
                            and lb.get("generator_hash_matches_certificate")):
                        diag_issues.append(f"{_dfn}: load_bearing_candidate self-reports a binding mismatch")
    if diag_issues: fails.append("Residual-diagnostic failures:\n    "+"\n    ".join(diag_issues))

    # 8b. MIG-033: displayed-interval enclosure. Two guarantees:
    #   (i)  the canonical directed-rounded display (floor lower / ceiling upper,
    #        24 significant digits) of EVERY certified ball encloses its exact
    #        dyadic ball — re-proved here independently of weil_engine.py;
    #   (ii) every interval printed in prose reports ([<sci>, <sci>] in tracked
    #        .md files outside migrations/) encloses the certified ball it
    #        displays; intervals matching no certified ball are rejected, so
    #        prose intervals can only come from certificates.
    # MIG-032's round-to-nearest display violated (i)/(ii) on every QH pivot.
    from decimal import Decimal as _Dec3, Context as _Ctx3, ROUND_FLOOR as _RF3, ROUND_CEILING as _RC3
    disp_issues=[]
    def _ball_exact(b):
        if "mid_dyadic" in b and "radius_dyadic" in b:
            mid=_dy_to_frac(b["mid_dyadic"]); rad=_dy_to_frac(b["radius_dyadic"])
            return mid-rad, mid+rad
        return _dec_to_frac(b["lower_decimal"]), _dec_to_frac(b["upper_decimal"])
    def _walk_balls(obj, tag):
        if isinstance(obj, dict):
            if "lower_decimal" in obj and "upper_decimal" in obj:
                yield tag, obj
            for k,v in obj.items(): yield from _walk_balls(v, f"{tag}.{k}")
        elif isinstance(obj, list):
            for i,v in enumerate(obj): yield from _walk_balls(v, f"{tag}[{i}]")
    _balls=[]
    if _os.path.isdir("metadata"):
        for _fn in sorted(_os.listdir("metadata")):
            if _fn.startswith("weil_") and _fn.endswith(".json"):
                try: _c=_json.load(open(f"metadata/{_fn}"))
                except Exception as e:
                    disp_issues.append(f"{_fn}: unreadable ({e})"); continue
                _balls += list(_walk_balls(_c, _fn))
    for _tag,_b in _balls:
        try: _L,_U=_ball_exact(_b)
        except Exception as e:
            disp_issues.append(f"{_tag}: cannot reconstruct exact ball ({e})"); continue
        _sig=24
        _dlo=_Ctx3(prec=_sig, rounding=_RF3).plus(_Dec3(_b["lower_decimal"]))
        _dup=_Ctx3(prec=_sig, rounding=_RC3).plus(_Dec3(_b["upper_decimal"]))
        if not (_dec_to_frac(f"{_dlo:.{_sig-1}e}") <= _L and _dec_to_frac(f"{_dup:.{_sig-1}e}") >= _U):
            disp_issues.append(f"{_tag}: canonical directed display fails to enclose exact ball")
    # tracked text enumeration (shared by checks 8b and 9; MIG-028 rule: git ls-files
    # when a repo is present, else the packaged manifest; NEVER silently skipped).
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
            fails.append("checks 8b/9: no git repo and no release/TRACKED_TEXT_MANIFEST.txt — cannot enumerate tracked text files (checks not skipped)")
            tracked=[]

    # 8b (continued): prose interval scan. Every [<sci>, <sci>] in tracked .md
    # reports must enclose the certified ball it displays. Matching rule: a ball
    # is DISPLAYED by an interval if the ball's exact midpoint lies inside it;
    # the interval passes iff at least one certified ball is FULLY enclosed by it.
    # An interval that matches no ball at all is rejected (prose intervals may
    # only be generated from certificates). migrations/ is excluded: the
    # migration log is an immutable historical record and may quote defective
    # pre-repair displays verbatim.
    import re as _re3
    _ivpat=_re3.compile(r"\[\s*(-?\d+(?:\.\d+)?[eE][+-]?\d+)\s*,\s*(-?\d+(?:\.\d+)?[eE][+-]?\d+)\s*\]")
    _exact_cache=[]
    for _tag,_b in _balls:
        try: _exact_cache.append((_tag, *_ball_exact(_b)))
        except Exception: pass
    for _fn in tracked:
        if not _fn.endswith(".md") or _fn.startswith("migrations/"): continue
        try: _txt=open(_fn, encoding="utf-8").read()
        except Exception: continue
        for _m in _ivpat.finditer(_txt):
            _a,_bb=_dec_to_frac(_m.group(1)), _dec_to_frac(_m.group(2))
            _line=_txt[:_m.start()].count("\n")+1
            _mid_matched=[t for t,_L,_U in _exact_cache if _a <= (_L+_U)/2 <= _bb]
            _enclosed=[t for t,_L,_U in _exact_cache if _a <= _L and _U <= _bb]
            if _enclosed: continue
            if _mid_matched:
                disp_issues.append(f"{_fn}:{_line}: displayed interval {_m.group(0)} does NOT enclose certified ball(s) {', '.join(_mid_matched[:3])}")
            else:
                disp_issues.append(f"{_fn}:{_line}: displayed interval {_m.group(0)} matches no certified ball (prose intervals must be generated from certificates)")
    if disp_issues: fails.append("Displayed-interval failures:\n    "+"\n    ".join(disp_issues))

    # 9. strict UTF-8 over all tracked text files (MIG-026 item 1; MIG-028 git-free).
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
