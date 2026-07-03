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
EULER = const_euler()
LOG4PI = (arb(4) * PI).log()

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
def T_certified(q, r, N=64, M=48):
    """Head to N exactly; tail by geometric m-expansion with certified -zeta'/zeta;
    explicit truncation bound (outward) for the m-series remainder. q,r ints (scales)."""
    assert N > Fraction(r, q), "need N > r/q for the geometric expansion"
    pps = prime_powers_upto(N)
    qA, rA = arb(q), arb(r)
    head = arb(0)
    # also precompute partial Dirichlet sums sum_{n<=N} Lambda(n)/n^{m+3/2} for each m
    for n, p in pps:
        lam = arb(p).log()
        head += lam * arb(n).sqrt() / (qA * n + rA) ** 2
    tail = arb(0)
    for m in range(M + 1):
        # S_m = -zeta'/zeta(m+3/2) - sum_{n<=N} Lambda(n)/n^{m+3/2}
        S = neg_zeta_log_deriv(2 * m + 3, 2)
        for n, p in pps:
            S -= arb(p).log() / arb(n) ** (arb(2 * m + 3) / 2)
        term = ((-1) ** m) * arb(m + 1) * (rA / qA) ** m * S / qA ** 2
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
    boundary = (LOG4PI + EULER) / arb(q + r) ** 2
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

# ---------- main ----------
def main():
    scales = [1, 2, 3]
    print(f"K0-W2 engine | Arb precision {BITS} bits | scales {scales}")
    H, V, Mm = M_compressed(scales)
    print("\nUnrestricted entries H(q,r) [certified balls]:")
    for i in range(3):
        for j in range(i, 3):
            approx = -(float(PI) / 2) * (1 / scales[i] + 1 / scales[j])
            print(f"  H({scales[i]},{scales[j]}) = {H[i][j].str(25)}   [boundary part ~ {approx:+.6f}]")
    v = V[0]
    print(f"\nNested basis vector b3 = {v}  (expect [-1, 4, -3])")
    M3 = Mm[0][0]
    print(f"\nM_3 (compressed 1x1) = {M3.str(30)}")
    ok_sign = M3 > 0
    print(f"Rigorous sign determination: M_3 > 0 is {'PROVED (interval strictly positive)' if ok_sign else 'NOT determined at this precision'}")
    norm2 = sum(x * x for x in v)
    print(f"Rayleigh value M_3/|b3|^2 = {(M3 / norm2).str(25)}   (|b3|^2 = {norm2})")
    zs = zero_side_M3(v, scales)
    print(f"\nZero-side cross-check (first 10 zeros, mpmath, NOT certified): {zs}")
    print("   note: zero-side tail beyond zero #10 is O(gamma_11 e^{-pi gamma_11}) ~ 1e-70; agreement is a")
    print("   consistency check of conventions only. It certifies nothing (K0-W2 gate 7).")
    print("\nCLASSIFICATION: restricted finite Weil test only (K0-W1 §7). Not progress toward RH")
    print("absent P0-WEIL-CORE. No zero-location assumption used on the certified track.")
    # machine-readable result
    out = {
        "scales": scales, "basis_b3": v,
        "M3_mid": float(M3.mid()), "M3_rad": float(M3.rad()),
        "M3_sign_certified_positive": bool(ok_sign),
        "zero_side_diagnostic": float(zs),
        "classification": "restricted finite Weil test (K0-W1 §7); no RH-progress claim",
    }
    with open("metadata/weil_M3_result.json", "w") as f:
        json.dump(out, f, indent=2)
    print("\nresult written to metadata/weil_M3_result.json")

if __name__ == "__main__":
    main()
