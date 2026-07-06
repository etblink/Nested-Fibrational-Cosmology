#!/usr/bin/env python3
"""
K0-W2: Certified Weil Matrix Entry Engine (scaffold; MIG-024).

Computes unrestricted Weil matrix entries
    H(q,r) = B_hat_W(U_q f0, U_r f0) = -E(f_{q,r}),   f0(x)=sqrt(x)e^{-x},
for rational scales, using the reviewer-verified closed forms:
    f_{q,r}(x) = sqrt(q r x)/(q x + r)^2                       (cross-correlation)
    E(f) = prime sum + (log 4pi + gamma) f(1) + archimedean J  (Weil explicit-formula functional)

CERTIFIED MODE (flint/Arb ball arithmetic):
  * prime head: exact sum over prime powers n <= N of Lambda(n) sqrt(n)/(qn+r)^2
  * prime tail: geometric m-expansion with certified -zeta'/zeta(m+3/2) from arb_series,
    plus an explicit outward truncation bound added to the ball radius
  * archimedean term: substitution u = 1/t maps [1,inf) -> [0,1]; the removable
    singularity at u=1 is cancelled EXACTLY by rational polynomial division (sympy,
    integer coefficients) before evaluation; then Arb certified integration (acb_calc)
  * boundary term: (log 4pi + euler_gamma)/(q+r)^2 in balls

All numerical results are RESTRICTED FINITE WEIL TESTS (K0-W1 Section 7).
They are not, and must never be described as, progress toward RH absent P0-WEIL-CORE.

DIAGNOSTIC MODE additionally cross-checks (never certifies) against the symmetric
zero-side formula using mpmath's high-precision zeta zeros.
"""
import sys, json
from fractions import Fraction

import flint
from flint import arb, acb, arb_series
import sympy as sp

BITS = 350
flint.ctx.prec = BITS

# ---------- constants (certified balls) ----------
def const_pi():
    return arb.pi()

def const_euler():
    # gamma = -psi(1) = -(d/ds log Gamma)(1): series coeff 1 of lgamma at 1
    try:
        return arb.const_euler()
    except AttributeError:
        s = arb_series([arb(1), arb(1)], prec=2).lgamma()
        return -s[1]

PI = const_pi()
# MIG-040: the module-level EULER/LOG4PI below are evaluated at import-time precision and
# are RETAINED ONLY for provenance/diagnostic reference. The certified matrix-building path
# MUST NOT use them for the boundary constant (they froze a ~2e-106 radius floor that no
# profile could contract, blocking H=7). Use boundary_constant() instead, which evaluates
# (log(4*pi) + EulerGamma) at the ACTIVE flint.ctx.prec and caches by exact precision.
EULER = const_euler()
LOG4PI = (arb(4) * PI).log()

_boundary_const_cache = {}
def boundary_constant():
    """MIG-040: C_boundary = log(4*pi) + EulerGamma, evaluated at the CURRENTLY active
    flint.ctx.prec and cached keyed by that exact precision. A ball created at one
    precision is never returned for another. No fallback to the frozen 350-bit constants.
    Formula unchanged: this is exactly log(4*pi) + gamma; only its evaluation precision moves."""
    prec = flint.ctx.prec
    cached = _boundary_const_cache.get(prec)
    if cached is not None:
        return cached
    val = (arb(4) * arb.pi()).log() + const_euler()   # both at the active precision
    _boundary_const_cache[prec] = val
    return val

# ---------- prime powers and Lambda ----------
def prime_powers_upto(N):
    """[(n, p)] for n = p^k <= N; Lambda(n) = log p."""
    out = []
    for p in sp.primerange(2, N + 1):
        pk = p
        while pk <= N:
            out.append((pk, p))
            pk *= p
    return sorted(out)

def neg_zeta_log_deriv(sigma_num, sigma_den):
    """Certified ball for -zeta'/zeta(sigma) at rational sigma>1 via arb_series."""
    sigma = arb(sigma_num) / arb(sigma_den)
    ser = arb_series([sigma, arb(1)], prec=2).zeta()
    z, zp = ser[0], ser[1]
    return -(zp / z)

# ---------- prime side: T(q,r) = sum_{n>=2} Lambda(n) sqrt(n)/(qn+r)^2 ----------
_S_cache = {}
MAX_SCALE_RATIO = 12  # largest r/q among used scale pairs; controls the S-table precision boost

def S_values(N, M):
    """Entry-independent certified S_m = -zeta'/zeta(m+3/2) - sum_{n<=N} Lambda(n) n^{-m-3/2}.

    PRECISION NOTE (MIG-025 radius-floor fix): S_m is a difference of O(2^-m)-scale
    quantities and so carries an ABSOLUTE ball-radius floor ~2^-prec. Downstream it is
    multiplied by (r/q)^m (up to 12^m), which amplifies that floor catastrophically for
    large m. Therefore the S-table is computed once at an ELEVATED internal precision
    prec_S = base + ceil(M*log2(MAX_SCALE_RATIO)) + 64, then the context is restored.
    Term arithmetic downstream stays at base precision (term midpoints are small)."""
    base = flint.ctx.prec
    import math
    prec_S = base + int(M * math.log2(MAX_SCALE_RATIO)) + 64
    key = (N, M, base)
    if key in _S_cache:
        return _S_cache[key]
    flint.ctx.prec = prec_S
    try:
        pps = prime_powers_upto(N)
        logs = {n: arb(p).log() for n, p in pps}
        out = []
        for m in range(M + 1):
            S = neg_zeta_log_deriv(2 * m + 3, 2)
            e = arb(2 * m + 3) / 2
            for n, p in pps:
                S -= logs[n] / arb(n) ** e
            out.append(S)
    finally:
        flint.ctx.prec = base
    _S_cache[key] = out
    return out

def T_certified(q, r, N=64, M=48):
    """Head to N exactly; tail by geometric m-expansion with certified -zeta'/zeta;
    explicit truncation bound (outward) for the m-series remainder. q,r ints (scales)."""
    assert N > Fraction(r, q), "need N > r/q for the geometric expansion"
    pps = prime_powers_upto(N)
    qA, rA = arb(q), arb(r)
    head = arb(0)
    for n, p in pps:
        lam = arb(p).log()
        head += lam * arb(n).sqrt() / (qA * n + rA) ** 2
    Svals = S_values(N, M)
    tail = arb(0)
    for m in range(M + 1):
        term = ((-1) ** m) * arb(m + 1) * (rA / qA) ** m * Svals[m] / qA ** 2
        tail += term
    # truncation bound: |term_m| <= (1/q^2)(m+1)(r/(qN))^m N^{-1/2}[logN/(m+1/2)+1/(m+1/2)^2]
    # for m > M:  sum <= C * rho^{M+1} ((M+2) - (M+1) rho)/(1-rho)^2,  rho = r/(qN),
    # with C = N^{-1/2} (log N + 4) / q^2  (crude, valid since m+1/2 >= 1/2 -> bracket <= 2logN+4 <= ... use logN+4 for m>=1; safe: 2(logN+2))
    rho = arb(r) / (arb(q) * N)
    C = (arb(2) * (arb(N).log() + 2)) / (arb(N).sqrt() * qA ** 2)
    bound = C * rho ** (M + 1) * ((M + 2) - (M + 1) * rho) / (1 - rho) ** 2
    tail = tail.union(tail + bound).union(tail - bound)  # widen ball outward by the bound
    return head + tail

# ---------- archimedean side: J(q,r), certified ----------
_Jcache = {}
def J_integrand_coeffs(q, r):
    """Exact integer numerator/denominator coefficient lists of the u-substituted,
    singularity-cancelled integrand G(u), u in [0,1]. Verified by sympy cancel."""
    key = (q, r)
    if key in _Jcache:
        return _Jcache[key]
    u = sp.symbols('u')
    Q, R = sp.Integer(q), sp.Integer(r)
    G = (2 * u ** 2 / (1 - u ** 4)) * (1 / (Q + R * u ** 2) ** 2 + 1 / (Q * u ** 2 + R) ** 2) \
        - 4 * u / ((Q + R) ** 2 * (1 - u ** 4))
    Gc = sp.cancel(sp.together(G))
    num, den = sp.fraction(Gc)
    num, den = sp.Poly(sp.expand(num), u), sp.Poly(sp.expand(den), u)
    # sanity: denominator must not vanish on [0,1] except nowhere (u=1 root removed)
    assert den.eval(1) != 0, "singularity at u=1 not cancelled"
    nc = [int(c) for c in num.all_coeffs()]
    dc = [int(c) for c in den.all_coeffs()]
    _Jcache[key] = (nc, dc)
    return nc, dc

def _horner(coeffs, x):
    acc = acb(0)
    for c in coeffs:
        acc = acc * x + c
    return acc

def J_certified(q, r):
    nc, dc = J_integrand_coeffs(q, r)
    def f(u, analytic=False):
        return _horner(nc, u) / _horner(dc, u)
    return acb.integral(f, 0, 1).real

# ---------- full entry ----------
def H_entry_certified(q, r, N=64, M=48):
    boundary = boundary_constant() / arb(q + r) ** 2
    prime = T_certified(q, r, N, M) + T_certified(r, q, N, M)
    arch = J_certified(q, r)
    return -(arb(q) * arb(r)).sqrt() * (prime + boundary + arch)

# ---------- nested basis and compressed matrices ----------
def nested_basis(scales):
    """b_k (k=3..N) supported on coords 1,2,k: exact integers if scales are ints."""
    q = scales
    N = len(q)
    cols = []
    for k in range(2, N):
        b = [0] * N
        b[0] = q[0] * (q[1] - q[k])
        b[1] = q[1] * (q[k] - q[0])
        b[k] = q[k] * (q[0] - q[1])
        assert sum(b) == 0 and sum(Fraction(bj, qj) for bj, qj in zip(b, q)) == 0
        cols.append(b)
    return cols  # list of columns

def M_compressed(scales, N=64, M=48):
    n = len(scales)
    H = [[None] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            H[i][j] = H_entry_certified(scales[i], scales[j], N, M)
            H[j][i] = H[i][j]
    V = nested_basis(scales)
    m = len(V)
    Mm = [[arb(0)] * m for _ in range(m)]
    for a in range(m):
        for b in range(m):
            s = arb(0)
            for i in range(n):
                if V[a][i] == 0: continue
                for j in range(n):
                    if V[b][j] == 0: continue
                    s += arb(V[a][i]) * arb(V[b][j]) * H[i][j]
            Mm[a][b] = s
    return H, V, Mm

# ---------- zero-side cross-check (DIAGNOSTIC ONLY; never certifies) ----------
def zero_side_M3(coeffs, scales, K=10, dps=60):
    import mpmath as mp
    mp.mp.dps = dps
    total = mp.mpf(0)
    for k in range(1, K + 1):
        g = mp.im(mp.zetazero(k))
        phi = sum(c * mp.power(s, mp.mpf(-0.5)) * mp.e ** (-1j * g * mp.log(s))
                  for c, s in zip(coeffs, scales))
        w = mp.pi * g / mp.sinh(mp.pi * g)
        total += 2 * w * abs(phi) ** 2   # zeros come in pairs rho, conj(rho)
    return total

# ---------- MIG-025: rigorous certificates, Q4 Schur, Q12 LDL ----------
import hashlib, subprocess, platform
from decimal import Decimal, getcontext, ROUND_FLOOR, ROUND_CEILING

def _arb_exact_fraction(x):
    """Exact Fraction for an arb with ZERO radius (mid() or rad() results)."""
    man, exp = x.man_exp()
    man, exp = int(man), int(exp)
    return Fraction(man) * (Fraction(2) ** exp if exp >= 0 else Fraction(1, 2 ** (-exp)))

def _frac_to_decimal(fr, digits, rounding):
    getcontext().prec = digits + 10
    getcontext().rounding = rounding
    d = Decimal(fr.numerator) / Decimal(fr.denominator)
    return format(d.normalize(), 'e')

def ball_certificate(x, digits=50):
    """Exact dyadic ball -> outward decimal certificate. lower rounded FLOOR, upper CEILING,
    radius CEILING, mid FLOOR (mid is informational; endpoints are the certificate)."""
    mid = _arb_exact_fraction(x.mid())
    rad = _arb_exact_fraction(x.rad())
    lo, up = mid - rad, mid + rad
    mman, mexp = x.mid().man_exp(); rman, rexp = x.rad().man_exp()
    return {
        "mid_dyadic": {"mantissa": str(int(mman)), "exponent": int(mexp)},
        "radius_dyadic": {"mantissa": str(int(rman)), "exponent": int(rexp)},
        "mid_decimal": _frac_to_decimal(mid, digits, ROUND_FLOOR),
        "radius_decimal": _frac_to_decimal(rad, digits, ROUND_CEILING),
        "lower_decimal": _frac_to_decimal(lo, digits, ROUND_FLOOR),
        "upper_decimal": _frac_to_decimal(up, digits, ROUND_CEILING),
        "sign_certified": ("positive" if lo > 0 else ("negative" if up < 0 else "indeterminate")),
    }

def provenance(bits, N, M):
    """MIG-026: generation_start_commit is the commit checked out when generation began
    (NOT a pointer to the generator source, which is identified only by
    generator_script_sha256). The commit CONTAINING these certificates is recorded
    post-commit in the external release manifest (certificate_container_commit)."""
    try:
        commit = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"],
                                         stderr=subprocess.DEVNULL).decode().strip()
    except Exception:
        commit = "unknown"
    src = open(__file__, "rb").read()
    return {
        "precision_bits": bits, "prime_head_N": N, "prime_tail_M": M,
        "python": platform.python_version(),
        "python_flint": getattr(flint, "__version__", "unknown"),
        "boundary_constant_mode": "active-profile (MIG-040): log(4*pi)+EulerGamma evaluated at active flint.ctx.prec, cached by exact precision; not import-time",
        "flint_arb_note": "FLINT/Arb library versions not exposed by python-flint 0.8; bundled with wheel",
        "generator_script_sha256": hashlib.sha256(src).hexdigest(),
        "generation_start_commit": commit,
        "prime_tail_bound": "sum_{m>M} <= C rho^{M+1}((M+2)-(M+1)rho)/(1-rho)^2, rho=r/(qN), C=2(logN+2)/(sqrt(N) q^2), added outward",
        "archimedean": "u=1/t substitution to [0,1]; removable u=1 singularity cancelled by exact rational polynomial division; Arb acb_calc certified integration",
        "classification": "restricted finite Weil test (K0-W1 sec.7); no RH-progress claim; no zero-location input on certified track",
    }

def H_matrix(scales, N=64, M=48):
    n = len(scales)
    H = [[None] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            H[i][j] = H_entry_certified(scales[i], scales[j], N, M)
            H[j][i] = H[i][j]
    return H

def compress(H, V):
    m = len(V); n = len(V[0])
    out = [[arb(0)] * m for _ in range(m)]
    for a in range(m):
        for b in range(m):
            s = arb(0)
            for i in range(n):
                if V[a][i] == 0: continue
                for j in range(n):
                    if V[b][j] == 0: continue
                    s += arb(V[a][i]) * arb(V[b][j]) * H[i][j]
            out[a][b] = s
    return out

def ldl_pivots(Mm):
    """Interval LDL^T pivots. Returns (pivots, status): status 'PD' if all pivots
    rigorously > 0, 'INDETERMINATE' if any pivot ball straddles 0, 'NOT_PD' if any < 0."""
    n = len(Mm)
    A = [[Mm[i][j] for j in range(n)] for i in range(n)]
    pivots = []
    for k in range(n):
        p = A[k][k]
        pivots.append(p)
        if not (p > 0):
            return pivots, ("NOT_PD" if (p < 0) else "INDETERMINATE")
        for i in range(k + 1, n):
            lik = A[i][k] / p
            for j in range(k + 1, i + 1):
                A[i][j] = A[i][j] - lik * A[k][j]
                A[j][i] = A[i][j]
    return pivots, "PD"

def eig2_enclosure(a, b, d):
    """Rigorous eigenvalue enclosures for [[a,b],[b,d]] in ball arithmetic."""
    tr2 = (a + d) / 2
    disc = (((a - d) / 2) ** 2 + b ** 2).sqrt()
    return tr2 - disc, tr2 + disc

def zero_side_matrix(V, scales, K=12, dps=60):
    """Diagnostic zero-side compressed matrix using positive ordinates only:
    (M)_{ab} = sum_{gamma>0} w(gamma) * 2*Re(a_a conj(a_b)), w = pi g/sinh(pi g)."""
    import mpmath as mp
    mp.mp.dps = dps
    m = len(V)
    out = [[mp.mpf(0)] * m for _ in range(m)]
    for k in range(1, K + 1):
        g = mp.im(mp.zetazero(k))
        w = mp.pi * g / mp.sinh(mp.pi * g)
        amps = [sum(V[a][i] * mp.power(s, mp.mpf(-0.5)) * mp.e ** (-1j * g * mp.log(s))
                    for i, s in enumerate(scales)) for a in range(m)]
        for a in range(m):
            for b in range(m):
                out[a][b] += w * 2 * mp.re(amps[a] * mp.conj(amps[b]))
    return out

def run_m3():
    scales = [1, 2, 3]
    H = H_matrix(scales)
    V = nested_basis(scales)
    Mm = compress(H, V)
    M3 = Mm[0][0]
    cert = {
        "M3_ball": ball_certificate(M3),
        "diagnostic_float": float(M3.mid()),
        "scales": scales, "basis": V,
        "provenance": provenance(BITS, 64, 48),
    }
    json.dump(cert, open("metadata/weil_M3_result.json", "w"), indent=2)
    print("M3 =", M3.str(30), "->", cert["M3_ball"]["sign_certified"])
    print("cert endpoints:", cert["M3_ball"]["lower_decimal"], "..", cert["M3_ball"]["upper_decimal"])

def run_q4():
    scales = [1, 2, 3, 4]
    H = H_matrix(scales)
    V = nested_basis(scales)          # b3=(-1,4,-3,0), b4=(-2,6,0,-4)
    print("basis:", V)
    Mm = compress(H, V)
    for row in Mm:
        print("  [", ", ".join(x.str(20) for x in row), "]")
    pivots, status = ldl_pivots(Mm)
    schur = pivots[1] if len(pivots) > 1 else None
    lo_eig, hi_eig = eig2_enclosure(Mm[0][0], Mm[0][1], Mm[1][1])
    print("LDL pivots:", [p.str(20) for p in pivots], "->", status)
    print("Schur complement (alpha - u^2/M3):", schur.str(25))
    print("eigenvalue enclosures:", lo_eig.str(25), "|", hi_eig.str(25))
    both_pos = (lo_eig > 0)
    cert = {
        "scales": scales, "basis": V,
        "M4_entries_balls": {f"{a}{b}": ball_certificate(Mm[a][b]) for a in range(2) for b in range(2)},
        "ldl_pivots": [ball_certificate(p) for p in pivots],
        "ldl_status": status,
        "schur_complement": ball_certificate(schur),
        "eigenvalue_enclosures": [ball_certificate(lo_eig), ball_certificate(hi_eig)],
        "all_eigenvalues_certified_positive": bool(both_pos),
        "provenance": provenance(BITS, 64, 48),
    }
    json.dump(cert, open("metadata/weil_M4_certificate.json", "w"), indent=2)
    zs = zero_side_matrix(V, scales)
    print("zero-side diagnostic matrix (12 zeros, 2Re convention, NOT certified):")
    for row in zs: print("  [", ", ".join(mp_str(x) for x in row), "]")

def mp_str(x):
    return f"{float(x):.14e}"

PROFILES = [(350, 64, 48), (450, 192, 112), (600, 384, 160)]

def run_q12():
    scales = list(range(1, 13))
    results = {}
    pending = set(range(3, 13))
    used_profile = {}
    for (bits, N, M) in PROFILES:
        if not pending:
            break
        flint.ctx.prec = bits
        print(f"profile bits={bits} N={N} M={M}: computing 78 certified entries...")
        H = H_matrix(scales, N, M)
        for n in sorted(pending):
            sub = scales[:n]
            V = nested_basis(sub)
            Hs = [[H[i][j] for j in range(n)] for i in range(n)]
            Mm = compress(Hs, V)
            pivots, status = ldl_pivots(Mm)
            results[n] = {"scales": sub, "dim": len(V), "ldl_status": status,
                          "profile": {"bits": bits, "N": N, "M": M},
                          "pivots": [ball_certificate(p, digits=40) for p in pivots]}
            print(f"  Q_{n}: dim {len(V)}  LDL {status}  pivots: " + ", ".join(p.str(12) for p in pivots))
            if status == "PD":
                used_profile[n] = (bits, N, M)
        pending = {n for n in pending if results[n]["ldl_status"] != "PD"}
        if pending:
            print(f"  escalating for Q_{sorted(pending)} (pivot interval touched zero)")
    out = {"family": "M_N = V_N^T H V_N, nested exact basis, scales 1..N",
           "escalation_profiles": PROFILES,
           "precision_note": "precision_bits, N, M are strictly per-result (results[n].profile); no global values apply (MIG-026 item 4)",
           "results": results, "provenance": {k: v for k, v in provenance("per-result", "per-result", "per-result").items()
                                              if k not in ("precision_bits", "prime_head_N", "prime_tail_M")},
           "eigenvalue_sign_statement": "for each N with ldl_status=PD, all eigenvalues of M_N are rigorously positive (Sylvester via certified LDL pivots)"}
    json.dump(out, open("metadata/weil_Q12_certificates.json", "w"), indent=2)
    if pending:
        print(f"UNRESOLVED at max profile: Q_{sorted(pending)} — reported as indeterminate, per gate policy")
    print("written metadata/weil_Q12_certificates.json")

# ---------- MIG-029: rational-height exhaustion Q_H (exact RH-equivalent directed system) ----------
def rational_height_scales(H):
    """Q_H = {m/n : 1<=m,n<=H, gcd(m,n)=1}, sorted. Union over H exhausts Q_+."""
    from math import gcd
    from fractions import Fraction
    S = sorted({Fraction(m, n) for m in range(1, H + 1) for n in range(1, H + 1) if gcd(m, n) == 1})
    return S

def run_qheight(H=4, N=64, M=48):
    """Certified compressed Weil matrix M_H over rational-height scales Q_H.
    Scales are rationals; H_entry_certified handles integer scales, so we clear denominators:
    U_q with q=m/n scales f0(qx); entries depend on q,r rationally via the closed forms, which
    extend verbatim to rational q,r (f_{q,r}(x)=sqrt(qrx)/(qx+r)^2). We evaluate with q,r as arb."""
    from fractions import Fraction
    scales = rational_height_scales(H)
    print(f"Q_{H}: {len(scales)} rational scales: {[str(s) for s in scales]}")
    # NOTE: this is a scaffold stub demonstrating the directed system; full certified rational-entry
    # evaluation reuses H_entry_certified with arb(q_num)/arb(q_den). Recorded for MIG-029; the
    # certified integer slices Q_3..Q_12 remain the validated first slices.
    return scales


# ================= MIG-031: certified rational-height evaluator =================
# Reuses the verified integer machinery's mathematics (closed forms f_{q,r}=sqrt(qrx)/(qx+r)^2,
# prime series, archimedean J) but with EXACT rational scales q,r in Q_+, per the 8 requirements.
from fractions import Fraction as _Frac
from math import gcd as _gcd, log2 as _log2

def _arb_from_fraction(fr):
    """Exact arb for a Fraction: arb(numerator)/arb(denominator). No float path (req 1)."""
    return arb(int(fr.numerator)) / arb(int(fr.denominator))

def reduced_height(fr):
    """h(m/n) = max(m,n) for reduced m/n (req 5)."""
    return max(abs(fr.numerator), fr.denominator)

def Q_height(H):
    """Q_H = {m/n : 1<=m,n<=H, gcd=1}, ordered by PERSISTENT rule: anchors 1,2 first,
    then by (reduced_height, value) so V_H embeds canonically into V_{H+1} (req 5)."""
    from math import gcd
    S = {_Frac(m, n) for m in range(1, H + 1) for n in range(1, H + 1) if gcd(m, n) == 1}
    anchors = [_Frac(1), _Frac(2)]
    rest = sorted((s for s in S if s not in anchors), key=lambda s: (reduced_height(s), s))
    return [a for a in anchors if a in S] + rest

def T_certified_rational(q, r, N=64, M=48):
    """Prime series T(q,r)=sum Lambda(n)sqrt(n)/(qn+r)^2 for rational q,r (arb-exact)."""
    qA, rA = _arb_from_fraction(q), _arb_from_fraction(r)
    ratio = _Frac(r, 1) / _Frac(q, 1)  # r/q as Fraction
    assert N > ratio, f"need N > r/q = {float(ratio)} for geometric tail"
    pps = prime_powers_upto(N)
    head = arb(0)
    for n, p in pps:
        head += arb(p).log() * arb(n).sqrt() / (qA * n + rA) ** 2
    Svals = S_values(N, M)
    tail = arb(0)
    rq = rA / qA
    for m in range(M + 1):
        tail += ((-1) ** m) * arb(m + 1) * rq ** m * Svals[m] / qA ** 2
    # outward truncation bound (same closed form, ratio rho=r/(qN))
    rho = rA / (qA * N)
    C = (arb(2) * (arb(N).log() + 2)) / (arb(N).sqrt() * qA ** 2)
    bound = C * rho ** (M + 1) * ((M + 2) - (M + 1) * rho) / (1 - rho) ** 2
    return (head + tail).union(head + tail + bound).union(head + tail - bound)

def J_integrand_coeffs_rational(q, r):
    """Exact rational archimedean integrand: clear denominators over Q[u], cancel the
    removable u=1 singularity over Q[u], return normalized integer coeff arrays (req 3)."""
    u = sp.symbols('u')
    Q = sp.Rational(q.numerator, q.denominator)
    R = sp.Rational(r.numerator, r.denominator)
    G = (2 * u ** 2 / (1 - u ** 4)) * (1 / (Q + R * u ** 2) ** 2 + 1 / (Q * u ** 2 + R) ** 2)         - 4 * u / ((Q + R) ** 2 * (1 - u ** 4))
    Gc = sp.cancel(sp.together(G))
    num, den = sp.fraction(Gc)
    num, den = sp.Poly(sp.expand(num), u), sp.Poly(sp.expand(den), u)
    assert den.eval(1) != 0, "u=1 singularity not cancelled"
    # Clear denominators of BOTH polys by a single common factor L (lcm over all coeff
    # denominators of num AND den), then divide BOTH by a single common integer gcd, so the
    # rational function num/den is preserved exactly (fixing the independent-gcd bug).
    all_cs = [sp.Rational(c) for c in num.all_coeffs()] + [sp.Rational(c) for c in den.all_coeffs()]
    L = 1
    for c in all_cs:
        L = sp.lcm(L, sp.denom(c))
    ncI = [int(sp.Rational(c) * L) for c in num.all_coeffs()]
    dcI = [int(sp.Rational(c) * L) for c in den.all_coeffs()]
    g = 0
    for c in ncI + dcI:
        g = _gcd(g, abs(c))
    g = g or 1
    nc = [c // g for c in ncI]
    dc = [c // g for c in dcI]
    return nc, dc

def J_certified_rational(q, r):
    nc, dc = J_integrand_coeffs_rational(q, r)
    def f(u, analytic=False):
        return _horner(nc, u) / _horner(dc, u)
    return acb.integral(f, 0, 1).real

def H_entry_rational(q, r, N=64, M=48):
    """Ambient Weil entry B_hat_W(U_q f0, U_r f0) for rational q,r."""
    qr = _arb_from_fraction(q) * _arb_from_fraction(r)
    boundary = boundary_constant() / (_arb_from_fraction(q) + _arb_from_fraction(r)) ** 2
    prime = T_certified_rational(q, r, N, M) + T_certified_rational(r, q, N, M)
    arch = J_certified_rational(q, r)
    return -qr.sqrt() * (prime + boundary + arch)

def primitive_nullspace_basis(scales):
    """Integer nullspace basis of the 2xN moment matrix A=[[1..1],[1/q..]], anchors q1,q2 fixed.
    b_k supported on (0,1,k): clear denominators, divide by gcd, serialize exact ints (req 4)."""
    n = len(scales)
    q1, q2 = scales[0], scales[1]
    cols = []
    for k in range(2, n):
        qk = scales[k]
        # b1*1+b2*1+bk*1=0 ; b1/q1+b2/q2+bk/qk=0. Solve over Q, clear denominators.
        # Use the same closed form as integer case but with Fractions:
        b1 = q1 * (q2 - qk)
        b2 = q2 * (qk - q1)
        bk = qk * (q1 - q2)
        vec = [_Frac(0)] * n
        vec[0], vec[1], vec[k] = b1, b2, bk
        # clear denominators to integers, divide by gcd
        from sympy import lcm
        L = 1
        for v in (b1, b2, bk): L = sp.lcm(L, v.denominator)
        ivec = [int(v * L) for v in vec]
        g = 0
        for v in ivec: g = _gcd(g, abs(v))
        g = g or 1
        ivec = [v // g for v in ivec]
        assert sum(ivec) == 0 and sum(_Frac(v, 1) / s for v, s in zip(ivec, scales)) == 0
        cols.append(ivec)
    return cols

def dynamic_max_ratio(scales):
    """max/min of the scale set = H^2 for Q_H (req 2); controls S-table precision."""
    fr = [_Frac(s) for s in scales]
    return max(fr) / min(fr)

def run_rational_height(H, base_bits=350, N=64, M=48):
    global MAX_SCALE_RATIO
    scales = Q_height(H)
    ratio = dynamic_max_ratio(scales)
    MAX_SCALE_RATIO = max(2, int(ratio) + 1)  # req 2: derive from actual scale set, not hard-coded 12
    _S_cache.clear()
    flint.ctx.prec = base_bits
    print(f"Q_{H}: {len(scales)} scales {[f'{s.numerator}/{s.denominator}' for s in scales]}")
    print(f"  max/min ratio = {ratio} (= H^2 = {H*H}); MAX_SCALE_RATIO -> {MAX_SCALE_RATIO}")
    n = len(scales)
    Hm = [[None]*n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            Hm[i][j] = H_entry_rational(scales[i], scales[j], N, M)
            Hm[j][i] = Hm[i][j]
    V = primitive_nullspace_basis(scales)
    print(f"  primitive basis vectors: {V}")
    m = len(V)
    Mm = [[arb(0)]*m for _ in range(m)]
    for c in range(m):
        for d in range(m):
            s = arb(0)
            for i in range(n):
                if V[c][i]==0: continue
                for j in range(n):
                    if V[d][j]==0: continue
                    s += arb(V[c][i])*arb(V[d][j])*Hm[i][j]
            Mm[c][d] = s
    pivots, status = ldl_pivots(Mm)
    print(f"  M_{H}: dim {m}  LDL {status}")
    for p in pivots: print("    pivot", p.str(18))
    cert = {
        "H": H,
        "scales": [[s.numerator, s.denominator] for s in scales],
        "ordering_rule": "anchors [1,2] then (reduced_height h(m/n)=max(m,n), value); persistent nesting",
        "max_min_ratio": [ratio.numerator, ratio.denominator],
        "basis": V,
        "dim": m,
        "profile": {"bits": base_bits, "N": N, "M": M, "max_scale_ratio": MAX_SCALE_RATIO},
        "ldl_status": status,
        "pivots": [ball_certificate(p, digits=40) for p in pivots],
        "provenance": provenance(base_bits, N, M),
    }
    json.dump(cert, open(f"metadata/weil_QH{H}_certificate.json","w"), indent=2)
    print(f"  written metadata/weil_QH{H}_certificate.json")
    return Mm, pivots, status


# ================= MIG-035: H=4/H=5 certified rational-height matrices =================
def _basis_moment_checks(basis, scales):
    """Verify Sum_j c_j = 0 and Sum_j c_j/q_j = 0 EXACTLY (rationals) for every basis
    vector (req 3). Returns per-vector dict; raises on any failure."""
    out = []
    for idx, c in enumerate(basis):
        s0 = sum(c)  # integers
        s1 = sum(_Frac(cj) / _Frac(scales[j]) for j, cj in enumerate(c))  # exact rational
        if s0 != 0 or s1 != 0:
            raise ValueError(f"basis vector {idx} fails moment equations: sum={s0}, sum c/q={s1}")
        out.append({"index": idx, "sum_c": int(s0), "sum_c_over_q": [s1.numerator, s1.denominator]})
    return out

def _nesting_certificate(H):
    """Verify Q_{H-1} is the exact ordered prefix of Q_H, so V_{H-1} embeds canonically
    into V_H by zero-padding (req 1: verify nesting against the previous height)."""
    cur = Q_height(H)
    if H <= 1:
        return {"previous_H": None, "prefix_verified": True, "note": "base height; no predecessor"}
    prev = Q_height(H - 1)
    is_prefix = cur[:len(prev)] == prev
    if not is_prefix:
        raise ValueError(f"nesting broken: Q_{H-1} is not the ordered prefix of Q_{H}")
    return {
        "previous_H": H - 1,
        "previous_len": len(prev),
        "current_len": len(cur),
        "prefix_verified": True,
        "embedding": "V_{H-1} embeds into V_H by zero-padding new coordinates (persistent (reduced_height,value) order)",
    }

def _rad_frac(x):
    """Exact Fraction radius of an arb ball (outward)."""
    return _arb_exact_fraction(x.rad())

# MIG-036 (item 5): the former _weyl_eig_enclosures used float ordering
# (key=lambda t: float(t[0].mid())), unsafe for increasingly clustered H>=6 spectra.
# It is removed; eigenvalues are now bound by the exact-rational residual certificate
# (_residual_eig_certificate), which orders by exact rational comparison of p_i/s_i.

RH_PROFILES = [(350, 64, 48), (500, 192, 112), (700, 384, 160), (900, 512, 224),
               # MIG-039 restricted profile-extension: appended ONLY after all four existing
               # profiles returned LDL INDETERMINATE for H=7, with the failure diagnosed as
               # solely numerical certification strength (all computed pivot midpoints
               # positive; pivot 31 mid=5.48e-88 with radius 6.71e-87 straddling zero).
               # Same formulas, matrix construction, Arb semantics, residual theorem,
               # dyadic serialization, and validator format; strictly monotone increases.
               (1200, 768, 320), (1600, 1024, 448)]

def _dyadic(x):
    """Serialize an arb (or its exact midpoint) as an exact dyadic {mantissa, exponent}."""
    src = x.mid() if hasattr(x, "mid") else x
    man, exp = src.man_exp()
    return {"mantissa": str(int(man)), "exponent": int(exp)}

def _dyf(d):
    """Dyadic dict -> exact Fraction."""
    from fractions import Fraction as Fr
    m = int(d["mantissa"]); e = int(d["exponent"])
    return Fr(m) * (Fr(2) ** e if e >= 0 else Fr(1, 2 ** (-e)))

def _adaptive_rho(w2, s, B):
    """MIG-043: rigorous exact dyadic upper bound rho = ceil(2^B * sqrt(w2/s^3)) / 2^B,
    computed with integer/rational arithmetic only (no float). Postcondition rho^2 s^3 >= w2.
    A zero exact residual (w2 == 0) receives rho = 0."""
    from fractions import Fraction as Fr
    from math import isqrt
    if w2 == 0:
        return Fr(0)
    # eta^2 = w2 / s^3 = a/b ; rho = r/2^B with r = ceil(2^B * sqrt(a/b))
    a = Fr(w2, s ** 3)
    num = a.numerator * (1 << (2 * B))   # a * 2^{2B}
    den = a.denominator
    r = isqrt(num // den)
    while r * r * den < num:              # ensure (r/2^B)^2 >= a  i.e.  r^2 den >= num
        r += 1
    rho = Fr(r, 1 << B)
    assert rho * rho * s ** 3 >= w2
    return rho

def _candidate_quantities(Mm, base_prec, mult):
    """MIG-043 Phase A: reproduce the residual method's candidate vectors at one
    (profile, multiplier) and return exact per-candidate quantities. Does NOT change the
    matrix, solver, profile, formula, enclosure, basis, or LDL."""
    from fractions import Fraction as Fr
    m = len(Mm)
    A0 = [[_arb_exact_fraction(Mm[i][j].mid()) for j in range(m)] for i in range(m)]
    Rinf_frac = max(sum(_arb_exact_fraction(Mm[i][j].rad()) for j in range(m)) for i in range(m))
    P = flint.acb_mat([[acb(Mm[i][j].mid()) for j in range(m)] for i in range(m)])
    saved = flint.ctx.prec
    try:
        flint.ctx.prec = base_prec * mult
        vals, vecs = P.eig(right=True)
        cand = []
        for col in range(m):
            v = [_arb_exact_fraction(vecs[i, col].real.mid()) for i in range(m)]
            if all(x == 0 for x in v):
                return None, Rinf_frac
            s = sum(x * x for x in v)
            Av = [sum(A0[i][j] * v[j] for j in range(m)) for i in range(m)]
            p = sum(v[i] * Av[i] for i in range(m))
            w = [s * Av[i] - p * v[i] for i in range(m)]
            w2 = sum(x * x for x in w)
            cand.append({"theta": Fr(p, s), "w2": w2, "s": s})
        cand.sort(key=lambda c: c["theta"])
        return cand, Rinf_frac
    finally:
        flint.ctx.prec = saved

def _classify_candidate(cand, Rinf_frac, W):
    """MIG-043 Phase A: 320-bit floor audit + B-ladder separation + Weyl, then classify."""
    from fractions import Fraction as Fr
    m = len(cand)
    thetas = [c["theta"] for c in cand]
    gaps = [thetas[i + 1] - thetas[i] for i in range(m - 1)]
    min_gap = min(gaps); min_idx = gaps.index(min_gap)
    # 320-bit floor audit
    floor = Fr(1, 1 << 319)
    rho320 = [_adaptive_rho(c["w2"], c["s"], 320) for c in cand]
    at_floor = sum(1 for r in rho320 for _ in [0] if r == floor)
    disj320 = all(thetas[i + 1] - rho320[i + 1] > thetas[i] + rho320[i] for i in range(m - 1))
    # B-ladder (<= W, plus W), dedup
    ladder = sorted({b for b in (320, 640, 1280, 2560, 5120, 10240, 20480) if b <= W} | {W})
    ladder_results = {}
    first_sep_B = None
    sep_rhos = None
    for B in ladder:
        rhos = [_adaptive_rho(c["w2"], c["s"], B) for c in cand]
        disj = all(thetas[i + 1] - rhos[i + 1] > thetas[i] + rhos[i] for i in range(m - 1))
        ladder_results[B] = disj
        if disj and first_sep_B is None:
            first_sep_B = B; sep_rhos = rhos
    # Weyl check at the first separating B
    weyl_all_pos = None
    if first_sep_B is not None:
        weyl_all_pos = all((thetas[i] - sep_rhos[i] - Rinf_frac) > 0 for i in range(m))
    # classification
    if first_sep_B is None:
        cls = "VECTOR-RESIDUAL-LIMITED"
    elif not weyl_all_pos:
        cls = "NONPOSITIVE-AFTER-WEYL"
    elif disj320:
        cls = "FULLY-SEPARABLE"
    else:
        cls = "QUANTIZATION-LIMITED"
    return {
        "dim": m,
        "min_center_gap": [min_gap.numerator, min_gap.denominator],
        "min_gap_indices": [min_idx, min_idx + 1],
        "min_gap_float": float(min_gap),
        "floor_2^-319_float": float(floor),
        "candidates_at_floor_320": at_floor,
        "min_gap_over_floor_float": float(min_gap / floor),
        "disjoint_at_320": disj320,
        "ladder_tested": ladder,
        "ladder_disjoint": {str(B): ladder_results[B] for B in ladder},
        "first_separating_B": first_sep_B,
        "weyl_all_positive_at_first_sep": weyl_all_pos,
        "classification": cls,
        "failing_pairs_at_320": [
            [i, i + 1,
             [gaps[i].numerator, gaps[i].denominator],
             float(gaps[i] - (rho320[i] + rho320[i + 1]))]
            for i in range(m - 1)
            if not (thetas[i + 1] - rho320[i + 1] > thetas[i] + rho320[i])
        ],
    }

def _residual_eig_certificate(Mm, base_prec):
    """MIG-036: bind the midpoint spectrum to A_0 with an EXACT RATIONAL residual
    certificate the validator can recompute without flint.

    For each eigenvector v_i (dyadic), with s = v^T v, p = v^T A_0 v, w = s*A_0 v - p*v
    (all exact dyadic), the Hermitian residual theorem gives an eigenvalue of A_0 in
    [theta - rho, theta + rho] with theta = p/s and any rho satisfying ||w||_2^2 <= rho^2 s^3
    (equivalently ||A_0 v - theta v||_2 <= rho ||v||_2). We serialize v and a dyadic rho;
    the n intervals are proved pairwise disjoint and ordered, so they exhaust the n-point
    midpoint spectrum. Widening each by the recomputed ||R||_inf encloses the true spectrum.
    Ordering uses EXACT rational comparison of p_i/s_i (no float)."""
    from fractions import Fraction as Fr
    from math import isqrt
    m = len(Mm)
    A0 = [[_arb_exact_fraction(Mm[i][j].mid()) for j in range(m)] for i in range(m)]
    Rinf_frac = max(sum(_arb_exact_fraction(Mm[i][j].rad()) for j in range(m)) for i in range(m))
    Rinf = arb(_frac_to_decimal(Rinf_frac, 80, ROUND_CEILING))
    P = flint.acb_mat([[acb(Mm[i][j].mid()) for j in range(m)] for i in range(m)])
    saved = flint.ctx.prec
    result = None
    resolution_bits = None
    try:
        for mult in (3, 6, 12, 20):
            flint.ctx.prec = base_prec * mult
            W_prec = base_prec * mult
            vals, vecs = P.eig(right=True)
            cand = []
            good = True
            for col in range(m):
                v = [_arb_exact_fraction(vecs[i, col].real.mid()) for i in range(m)]
                if all(x == 0 for x in v):
                    good = False; break
                s = sum(x * x for x in v)
                Av = [sum(A0[i][j] * v[j] for j in range(m)) for i in range(m)]
                p = sum(v[i] * Av[i] for i in range(m))
                w = [s * Av[i] - p * v[i] for i in range(m)]
                w2 = sum(x * x for x in w)
                cand.append({"theta": Fr(p, s), "w2": w2, "s": s, "v": v})
            if not good:
                continue
            cand.sort(key=lambda c: c["theta"])  # exact rational sort
            # MIG-043: ADAPTIVE dyadic residual resolution. The former fixed SCALE = 1<<320
            # imposed a rho floor of 2^-319 (~9.36e-97) regardless of eigenvector precision,
            # which prevented separation whenever the center gap fell below that floor
            # (the H=8 min gap is ~2.2e-103). We now select the SMALLEST bit resolution B on
            # the deterministic ladder {320,640,...,20480,W} (<= W = working precision) at which
            # every rho_i = ceil(2^B * sqrt(w2_i/s_i^3)) / 2^B (integer sqrt; rho^2 s^3 >= w2)
            # yields pairwise-disjoint ordered intervals. Same theorem, same formula, same
            # postcondition; only the grid fineness adapts.
            ladder = sorted({b for b in (320, 640, 1280, 2560, 5120, 10240, 20480) if b <= W_prec} | {W_prec})
            chosen = None
            for B in ladder:
                SCALE = 1 << B
                rhos = []
                for c in cand:
                    rho2 = Fr(c["w2"], c["s"] ** 3)
                    rs = isqrt((rho2.numerator * SCALE * SCALE) // rho2.denominator) + 2
                    rho = Fr(rs, SCALE)
                    if rho * rho * c["s"] ** 3 < c["w2"]:
                        rho = rho * 2  # safety (never triggers)
                    rhos.append(rho)
                if all(cand[i]["theta"] - rhos[i] > cand[i - 1]["theta"] + rhos[i - 1] for i in range(1, m)):
                    chosen = (B, rhos); break
            if chosen is None:
                continue  # residual isolation genuinely failed at this multiplier; escalate
            B_used, rhos = chosen
            for c, r in zip(cand, rhos):
                c["rho"] = r
            resolution_bits = B_used
            result = cand; break
    finally:
        flint.ctx.prec = saved
    if result is None:
        raise RuntimeError("residual eig certificate: could not obtain disjoint ordered midpoint intervals")
    # widened enclosures (exact) and serialization
    eigpairs = []
    enclosures = []
    all_pos = True
    for c in result:
        lo = c["theta"] - c["rho"] - Rinf_frac
        hi = c["theta"] + c["rho"] + Rinf_frac
        if lo <= 0:
            all_pos = False
        enclosures.append({
            "lower_decimal": _frac_to_decimal(lo, 45, ROUND_FLOOR),
            "upper_decimal": _frac_to_decimal(hi, 45, ROUND_CEILING),
        })
        # rho serialized as dyadic upper bound (adaptive B-ladder resolution, MIG-043)
        eigpairs.append({
            "v": [_dyadic_from_fraction(x) for x in c["v"]],
            "rho": _dyadic_from_fraction(c["rho"]),
        })
    return eigpairs, enclosures, Rinf, Rinf_frac, all_pos, resolution_bits

def _dyadic_from_fraction(fr):
    """Serialize an exact dyadic Fraction (denominator a power of 2) as {mantissa, exponent}.
    For a general Fraction, represents it exactly if dyadic; else raises."""
    num, den = fr.numerator, fr.denominator
    if den & (den - 1) != 0:
        raise ValueError("non-dyadic fraction cannot be serialized exactly")
    e = -(den.bit_length() - 1)
    return {"mantissa": str(num), "exponent": e}


def _build_compressed(H, scales, V, base_bits, N, M):
    """Build the compressed real-symmetric interval matrix M_H at one precision profile."""
    global MAX_SCALE_RATIO
    ratio = dynamic_max_ratio(scales)
    MAX_SCALE_RATIO = max(2, int(ratio) + 1)
    _S_cache.clear()
    flint.ctx.prec = base_bits
    _bc = boundary_constant()  # MIG-040: built once at this profile's precision, reused for all entries
    n = len(scales)
    Hm = [[None] * n for _ in range(n)]
    for i in range(n):
        for j in range(i, n):
            Hm[i][j] = H_entry_rational(scales[i], scales[j], N, M)
            Hm[j][i] = Hm[i][j]
    m = len(V)
    Mm = [[arb(0)] * m for _ in range(m)]
    for a in range(m):
        for b in range(a, m):
            s = arb(0)
            for i in range(n):
                if V[a][i] == 0: continue
                for j in range(n):
                    if V[b][j] == 0: continue
                    s += arb(V[a][i]) * arb(V[b][j]) * Hm[i][j]
            Mm[a][b] = s
            Mm[b][a] = s
    return Mm

def run_rational_height_certified(H, profiles=None):
    """MIG-035 richer certificate for H (>=4): full compressed matrix as dyadic entry
    balls, exact basis with moment checks, interval-LDL PD certification, and rigorous
    eigenvalue enclosures, plus nesting proof and LDL/eigenvalue inertia agreement.
    Escalates precision profiles until PD certifies (like run_q12).
    Does NOT touch the existing QH2/QH3 certificates (different generator, only run for H)."""
    scales = Q_height(H)
    ratio = dynamic_max_ratio(scales)
    n = len(scales)
    nesting = _nesting_certificate(H)
    V = primitive_nullspace_basis(scales)
    moment_checks = _basis_moment_checks(V, scales)
    m = len(V)
    print(f"Q_{H}: {n} scales; dim {m}; max/min ratio {ratio}; nesting OK")

    profiles = profiles or RH_PROFILES
    # MIG-042: exact maximum ordered scale ratio for the applicability predicate.
    # For the symmetric entry construction H_entry_rational evaluates both T(q,r) and
    # T(r,q), so the relevant threshold is max_{q,r} r/q = max(Q_H)/min(Q_H), computed
    # exactly as a Fraction (never float, never hardcoded H**2 or a height-specific value).
    _sfr = [_Frac(s) for s in scales]
    max_ratio = max(_sfr) / min(_sfr)
    profile_dispositions = []
    Mm = pivots = eigpairs = eig_encl_ser = None; Rinf = Rinf_frac = None; resolution_bits = None; status = "INDETERMINATE"; base_bits = N = M = None
    for (bb, NN, MM) in profiles:
        # MIG-042 structural-applicability guard: the prime-tail geometric expansion
        # requires N > r/q for every ordered pair, i.e. N > max_ratio (strict). A profile
        # failing this is STRUCTURALLY INAPPLICABLE (outside the convergence domain) and is
        # recorded and skipped BEFORE any matrix construction. This is distinct from LDL
        # indeterminacy / residual-isolation / nonpositive-endpoint / profile exhaustion.
        if not (_Frac(NN) > max_ratio):
            profile_dispositions.append({
                "bits": bb, "N": NN, "M": MM,
                "max_ratio": [max_ratio.numerator, max_ratio.denominator],
                "comparison": f"N={NN} <= max_ratio={max_ratio} (float {float(max_ratio):.6g})",
                "outcome": "STRUCTURALLY INAPPLICABLE",
                "reason": "prime-tail geometric convergence precondition N > r/q not met; matrix not constructed",
            })
            print(f"  profile bits={bb} N={NN} M={MM}: STRUCTURALLY INAPPLICABLE (N={NN} <= max_ratio {max_ratio}); skip")
            continue
        base_bits, N, M = bb, NN, MM
        Mm = _build_compressed(H, scales, V, bb, NN, MM)
        pivots, status = ldl_pivots(Mm)
        if status != "PD":
            profile_dispositions.append({"bits": bb, "N": NN, "M": MM, "outcome": f"LDL {status}"})
            print(f"  profile bits={bb} N={NN} M={MM}: LDL {status} -> escalate")
            continue
        try:
            eigpairs, eig_encl_ser, Rinf, Rinf_frac, all_pos, resolution_bits = _residual_eig_certificate(Mm, bb)
        except RuntimeError as ex:
            profile_dispositions.append({"bits": bb, "N": NN, "M": MM, "outcome": "LDL PD; RESIDUAL-ISOLATION-FAILURE",
                                         "detail": str(ex)})
            print(f"  profile bits={bb} N={NN} M={MM}: LDL PD but residual eig certificate failed ({ex}) -> escalate")
            status = "INDETERMINATE"
            continue
        if not all_pos:
            profile_dispositions.append({"bits": bb, "N": NN, "M": MM, "outcome": "LDL PD; NONPOSITIVE-AFTER-WEYL"})
            print(f"  profile bits={bb} N={NN} M={MM}: LDL PD but a widened eigenvalue interval not strictly positive -> escalate")
            status = "INDETERMINATE"
            continue
        print(f"  profile bits={bb} N={NN} M={MM}: LDL PD and eigenvalues residual-certified "
              f"(disjoint at adaptive resolution B={resolution_bits}, all positive)")
        profile_dispositions.append({"bits": bb, "N": NN, "M": MM, "outcome": "CERTIFIED",
                                     "residual_resolution_bits": resolution_bits})
        break
    if status != "PD" or eigpairs is None:
        raise ValueError(f"H={H}: not fully certified at max profile (LDL {status})")
    for p in pivots:
        assert p > 0, "pivot lower endpoint not strictly positive"

    # MIG-036: eigenvalue enclosures are the residual-certified widened intervals
    assert len(eig_encl_ser) == len(pivots), "eigenvalue count != dim"
    m = len(pivots)
    eig_positive = m  # all_pos verified above
    Rinf_cert = ball_certificate(Rinf, digits=40)
    print(f"  eigenvalues: {m} residual-certified enclosures, all positive; "
          f"lambda_min lower {eig_encl_ser[0]['lower_decimal']}.., lambda_max upper ..{eig_encl_ser[-1]['upper_decimal']}")

    # serialize the FULL compressed matrix (both triangles) so Hermitian pairing
    # M_jk = conj(M_kj) is independently checkable and tamperable in adversarial tests
    cmb = {}
    for a in range(m):
        for b in range(m):
            cmb[f"{a}_{b}"] = ball_certificate(Mm[a][b], digits=40)

    cert = {
        "H": H,
        "scales": [[s.numerator, s.denominator] for s in scales],
        "ordering_rule": "anchors [1,2] then (reduced_height h(m/n)=max(m,n), value); persistent nesting",
        "nesting": nesting,
        "max_min_ratio": [ratio.numerator, ratio.denominator],
        "basis": V,
        "basis_moment_checks": moment_checks,
        "dim": m,
        "matrix_dim_rule": "|Q_H| - 2",
        "primary_matrix": "compressed",
        "hermitian": True,
        "compressed_matrix_balls": cmb,
        "profile": {"bits": base_bits, "N": N, "M": M, "max_scale_ratio": MAX_SCALE_RATIO},
        "profile_history": profile_dispositions,
        "max_ratio_exact": [max_ratio.numerator, max_ratio.denominator],
        "ldl_status": status,
        "pivots": [ball_certificate(p, digits=40) for p in pivots],
        "pivots_role": ("redundant generator-produced cross-check; the PRIMARY positive-definiteness "
                        "proof is the matrix-bound eigenvalue residual certificate below (MIG-036)"),
        "eigenvalue_method": ("MIG-036 exact rational residual certificate binding lambda(A_0): for each "
                              "eigenvector v (dyadic), the validator recomputes theta = v^T A_0 v / v^T v "
                              "and w = (v^T v) A_0 v - (v^T A_0 v) v in exact rational arithmetic and "
                              "verifies ||w||_2^2 <= rho^2 (v^T v)^3, so the Hermitian residual theorem "
                              "places an eigenvalue of A_0 in [theta-rho, theta+rho]; the n intervals are "
                              "proved pairwise disjoint and ordered (exact rational comparison), hence "
                              "exhaust the n-point spectrum; each is widened outward by the recomputed "
                              "||R||_inf (Weyl) to enclose the true spectrum. This binds the spectrum to "
                              "the serialized matrix and is the primary PD proof."),
        "eigenvalue_certificate": {
            "primary_pd_proof": True,
            "residual_theorem": "Hermitian residual: exists eigenvalue in [theta-rho, theta+rho] when ||A0 v - theta v||_2 <= rho ||v||_2",
            "residual_resolution_bits": resolution_bits,
            "residual_resolution_note": ("MIG-043 adaptive dyadic resolution: rho_i = ceil(2^B sqrt(w2_i/s_i^3))/2^B "
                                         "at the smallest ladder B in {320,640,...,W} giving pairwise-disjoint "
                                         "ordered intervals (replaces the fixed 2^-320 grid; same theorem/formula)."),
            "eigenpairs": eigpairs,
            "R_inf_upper": Rinf_cert,
        },
        "weyl": {
            "R_inf_upper": Rinf_cert,
            "bound": "||A-A_0||_2 <= ||R||_inf (max abs row sum of entry-ball radii; Hermitian)",
        },
        "eigenvalue_enclosures": eig_encl_ser,
        "all_eigenvalues_certified_positive": True,
        "inertia": {"ldl_positive_pivots": m, "eig_positive": eig_positive, "dim": m, "agree": True},
        "classification": ("H=%d rigorously positive restricted rational-height Weil test if certified: "
                           "a finite consistency result inside an exact infinite reformulation, "
                           "NOT a theorem-step toward RH." % H),
        "provenance": provenance(base_bits, N, M),
    }
    path = f"metadata/weil_QH{H}_certificate.json"
    json.dump(cert, open(path, "w"), indent=2)
    print(f"  written {path}")
    return Mm, pivots, eig_encl_ser, status


def _display_ball_refs(ball):
    """Exact Fraction reference endpoints for enclosure checks: the dyadic ball
    [mid-rad, mid+rad] when serialized dyadics are present (strongest), else the
    outward decimal endpoints (themselves proven to enclose the dyadic ball by
    validate.py check 8)."""
    from fractions import Fraction
    from decimal import Decimal
    if "mid_dyadic" in ball and "radius_dyadic" in ball:
        mid = Fraction(int(ball["mid_dyadic"]["mantissa"])) * Fraction(2) ** int(ball["mid_dyadic"]["exponent"])
        rad = Fraction(int(ball["radius_dyadic"]["mantissa"])) * Fraction(2) ** int(ball["radius_dyadic"]["exponent"])
        return mid - rad, mid + rad
    return (Fraction(Decimal(ball["lower_decimal"])), Fraction(Decimal(ball["upper_decimal"])))

def display_interval_from_cert(ball, sig=24):
    """MIG-033: generate prose interval text from certified outward endpoints with
    DIRECTED rounding — lower endpoint ROUND_FLOOR, upper endpoint ROUND_CEILING,
    at `sig` significant digits — then PROVE enclosure of the exact dyadic ball
    before returning. Never returns a non-enclosing string (raises ValueError).

    MIG-032's version formatted with round-to-nearest ({:.24e}), which rounded the
    H=2 lower endpoint UP by ~9.02e-42 past the certified lower endpoint, so the
    displayed interval failed to enclose the certificate. Round-to-nearest is
    never directionally safe; only floor/ceiling formatting is."""
    from decimal import Decimal, Context, ROUND_FLOOR, ROUND_CEILING
    from fractions import Fraction
    lo = Decimal(ball["lower_decimal"]); up = Decimal(ball["upper_decimal"])
    dlo = Context(prec=sig, rounding=ROUND_FLOOR).plus(lo)
    dup = Context(prec=sig, rounding=ROUND_CEILING).plus(up)
    # format at exactly `sig` significant digits; the Decimal already has <= sig
    # digits, so this formatting is exact (no further rounding occurs)
    slo, sup = f"{dlo:.{sig-1}e}", f"{dup:.{sig-1}e}"
    # mandatory enclosure self-check against the exact dyadic ball
    L, U = _display_ball_refs(ball)
    if not (Fraction(Decimal(slo)) <= L and Fraction(Decimal(sup)) >= U):
        raise ValueError(f"display_interval_from_cert: [{slo}, {sup}] does not enclose "
                         f"the certified ball — refusing to emit a non-enclosing display")
    return f"[{slo}, {sup}]"

def display_interval_exact(ball):
    """MIG-033 alternative: verbatim certified outward endpoints, no shortening.
    Trivially enclosing (endpoints are the certificate's own outward decimals)."""
    return f"[{ball['lower_decimal']}, {ball['upper_decimal']}]"


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "m3"
    {"m3": run_m3, "q4": run_q4, "q12": run_q12, "qheight": lambda: run_qheight(int(sys.argv[2]) if len(sys.argv)>2 else 4),
     "qh": lambda: run_rational_height(int(sys.argv[2]) if len(sys.argv)>2 else 2)}[cmd]()

if __name__ == "__main__":
    main()
