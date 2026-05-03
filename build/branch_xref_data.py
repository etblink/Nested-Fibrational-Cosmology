"""
build/branch_xref_data.py — v35 Canonical cross-reference data for all remaining branches.

Provides BRANCH_XREF_DATA: a dict mapping branch name -> {machine_id -> xref_dict}.
Also provides BRANCH_CERT_CONFIGS with certificate metadata per branch.

Imported by both add_xrefs.py and multi_branch_certificate.py.
"""

# ─────────────────────────────────────────────────────────────────────────
# Canonical cross-reference data per branch
# ─────────────────────────────────────────────────────────────────────────

BRANCH_XREF_DATA = {

    "NS": {
        "thm:NS.stage0": {
            "canonical_theorem": "NS.Stage-0",
            "canonical_section": "NS §Lawful Descent",
            "canonical_label": "NS Stage-0 Thermodynamic Floor Density [U]",
            "cross_check": "Unconditional; no Phase-A or K_0 hypothesis needed",
        },
        "thm:NS.stage1": {
            "canonical_theorem": "NS.Stage-1",
            "canonical_section": "NS §Source-Descended Obstruction",
            "canonical_label": "NS Stage-1 Boundary Flux Stabilization [U]",
            "cross_check": "Unconditional; follows from Stage-0",
        },
        "thm:NS.stage2a": {
            "canonical_theorem": "NS.Stage-2a",
            "canonical_section": "NS §Source-Descended Obstruction",
            "canonical_label": "NS Stage-2a Discrete Balance Identity [U]",
            "cross_check": "Unconditional; canonical decomposition of obstruction quantity",
        },
        "thm:NS.stage2b": {
            "canonical_theorem": "NS.Stage-2b",
            "canonical_section": "NS §Source-Descended Obstruction",
            "canonical_label": "NS Stage-2b Nonlinear Term Identification [C]",
            "cross_check": "Conditional on PASS screening from Book II",
        },
        "thm:NS.leray": {
            "canonical_theorem": "NS.Leray",
            "canonical_section": "NS §Lawful Descent",
            "canonical_label": "NS Leray Weak Existence [U]",
            "cross_check": "Unconditional; canonical base for all NS closure arguments",
        },
        "thm:NS.window-uniformity": {
            "canonical_theorem": "NS.WindowUnif",
            "canonical_section": "NS §Active Continuation Criterion",
            "canonical_label": "NS Window Uniformity + Q2a Resolution [C]",
            "cross_check": "Conditional Phase-A/K_0=7; Q2a resolved; eventual periodicity",
        },
        "thm:NS.6.1": {
            "canonical_theorem": "NS.6.1",
            "canonical_section": "NS §Active Missing Bridge",
            "canonical_label": "NS.6.1 Active Missing Bridge Theorem [C]",
            "cross_check": "Conditional; partial discharge of ob:NS.bridge-stage2",
        },
        "thm:NS.Ren5": {
            "canonical_theorem": "NS.Ren.5",
            "canonical_section": "NS §Boundary Chain",
            "canonical_label": "Late Alignment-to-Dissipation Lemma Ren.5 [C]",
            "cross_check": "Conditional; discharges proof-program frontier via sub-lemma chain",
        },
        "thm:NS.SB2-discharged": {
            "canonical_theorem": "NS.SB2-dis",
            "canonical_section": "NS §Boundary Chain",
            "canonical_label": "SB2 Conditionally Discharged via SCT.6b [C]",
            "cross_check": "Full discharge of ob:NS.SB2 at Phase-A/K_0=7/PASS/SCT.6b scope",
        },
        "thm:NS.7.1": {
            "canonical_theorem": "NS.7.1",
            "canonical_section": "NS §Endpoint Bridge",
            "canonical_label": "NS.7.1 Continuation-Criterion-to-Endpoint [C]",
            "cross_check": "Domain-bounded CERT-CLOSE on declared interval; Stage-3 Clay remains external",
        },
        "cor:NS.domain-bounded-cert-close": {
            "canonical_theorem": "NS.DomBdd",
            "canonical_section": "NS §Domain-Bounded CERT-CLOSE",
            "canonical_label": "NS Domain-Bounded CERT-CLOSE Corollary [C]",
            "cross_check": "Corollary of NS.6.1+NS.7.1; domain-bounded scope only",
        },
        "prop:NS.status": {
            "canonical_theorem": "prop:NS-status",
            "canonical_section": "NS §Branch Status",
            "canonical_label": "NS Branch Status (Updated) [C] — domain-bounded conditional CERT-CLOSE",
            "cross_check": "Corrects stale frontier-blocked preamble; v31 governance finding",
        },
        "ob:NS.SB2": {
            "canonical_theorem": "ob:NS.SB2",
            "canonical_section": "NS §Obligations",
            "canonical_label": "Positive Reserve on the Safe Tail — CONDITIONALLY DISCHARGED [C]",
            "cross_check": "Discharged by thm:NS.SB2-discharged via SCT.6b",
        },
        "ob:NS.bridge-stage2": {
            "canonical_theorem": "ob:NS.bridge2",
            "canonical_section": "NS §Bridge Stack",
            "canonical_label": "NS Bridge Stack Stage 2 Obligation [O] — partial discharge",
            "cross_check": "Partially discharged by thm:NS.6.1; stage boundary progress recorded",
        },
        "front:NS.main": {
            "canonical_theorem": "front:NS.main",
            "canonical_section": "NS §Stage-3 Frontier",
            "canonical_label": "NS Stage-3 Global Frontier — Clay Millennium Prize [O]",
            "cross_check": "ACTIVE EXTERNAL FRONTIER; unconditional global regularity outside NFC toolkit",
        },
        "status:NS": {
            "canonical_theorem": "status:NS",
            "canonical_section": "NS §Branch Status",
            "canonical_label": "NS Branch Status — domain-bounded-cert-close",
            "cross_check": "Stale preamble corrected in v31; governed by prop:NS.status",
        },
    },

    "SM": {
        "ob:SM.harmonization": {
            "canonical_theorem": "O-SM.Harm",
            "canonical_section": "SM §Open Obligations",
            "canonical_label": "O-SM.Harmonization — Harmonization Functor [C]",
            "cross_check": "Partially discharged by KPO chain; matter extension pending",
        },
        "ob:SM.matter": {
            "canonical_theorem": "O-SM.Matter",
            "canonical_section": "SM §Open Obligations",
            "canonical_label": "O-SM.Matter — Matter Content [C]",
            "cross_check": "Candidate assignment at structural level; scoped discharge",
        },
        "ob:SM.higgs": {
            "canonical_theorem": "O-SM.Higgs",
            "canonical_section": "SM §Open Obligations",
            "canonical_label": "O-SM.Higgs — Higgs/EWSB Screening [C]",
            "cross_check": "B0 screening scoped discharge; full higgs mechanism pending",
        },
        "ob:SM.coupling-transfer": {
            "canonical_theorem": "O-SM.CoupTr",
            "canonical_section": "SM §Open Obligations",
            "canonical_label": "O-SM.CouplingTransfer — Structural Seed [C]",
            "cross_check": "Structural-seed scope only; numerical coupling derivation pending",
        },
        "thm:SM.gauge-chain": {
            "canonical_theorem": "thm:SM-gauge-chain",
            "canonical_section": "SM §Gauge Algebra and Uniqueness",
            "canonical_label": "SM Gauge Algebra + Uniqueness Chain [C]",
            "cross_check": "su(3)+su(2)+u(1) identified from collar-local Lie theory; inherits YM [C]",
        },
        "thm:SM.three-gen": {
            "canonical_theorem": "thm:SM-three-gen",
            "canonical_section": "SM §Three-Generation Structure",
            "canonical_label": "Three-Generation Structure [U]",
            "cross_check": "UNCONDITIONAL; multiplicity-3 eigenblock count from NFC-3Gen structure",
        },
        "thm:SM.harmonization-partial": {
            "canonical_theorem": "thm:SM-harm-partial",
            "canonical_section": "SM §Harmonization Functor",
            "canonical_label": "Conditional Partial Harmonization Functor (KPO-1 to KPO-4) [C]",
            "cross_check": "PARTIAL discharge of O-SM.Harmonization; matter sector excluded",
        },
        "thm:SM.coupling-transfer-full": {
            "canonical_theorem": "thm:SM-coupling-transfer",
            "canonical_section": "SM §Coupling Transfer",
            "canonical_label": "Structural Coupling Transfer Theorem [C]",
            "cross_check": "SCOPED discharge; structural seed only, not full coupling derivation",
        },
        "thm:SM.higgs-source-descended": {
            "canonical_theorem": "thm:SM-higgs-src",
            "canonical_section": "SM §Matter Content",
            "canonical_label": "B0 Screening Projection Source-Descendedness [C]",
            "cross_check": "SCOPED discharge of O-SM.Higgs; B0=ker(d_Sv) uniquely determined",
        },
        "thm:SM.18.1": {
            "canonical_theorem": "thm:SM-18-1",
            "canonical_section": "SM §Intrinsic Closure",
            "canonical_label": "Conditional SM Intrinsic Closure (legacy alias) [C]",
            "cross_check": "Legacy machine ID; superseded by prop:SM.intrinsic-closure in v30",
        },
        "prop:SM.intrinsic-closure": {
            "canonical_theorem": "prop:SM-intrinsic",
            "canonical_section": "SM §Intrinsic Closure",
            "canonical_label": "Conditional SM Intrinsic Structural Closure [C]",
            "cross_check": "Four SM internal obligations conditionally discharged; inherits YM+GR scope limits",
        },
        "prop:SM.status-reconciliation": {
            "canonical_theorem": "prop:SM-status-rec",
            "canonical_section": "SM §Status Reconciliation",
            "canonical_label": "SM Status Reconciliation — corrected from CERT-PROJ [C]",
            "cross_check": "Corrected posture: conditionally intrinsic-structural closed, inherited-scope open",
        },
        "ob:SM.O-IDcont": {
            "canonical_theorem": "ob:O-IDcont",
            "canonical_section": "SM §Open Obligations",
            "canonical_label": "O-IDcont Continuum/Operator Identification Force Upgrade [O]",
            "cross_check": "ACTIVE FRONTIER; blocks promotion from conditional to unconditional closure",
        },
        "status:SM": {
            "canonical_theorem": "status:SM",
            "canonical_section": "SM §Branch Status",
            "canonical_label": "SM Branch Status — intrinsic-structural-close",
            "cross_check": "Status(SM) <= Status(YM) AND Status(GR) AND Status(SM_intrinsic)",
        },
    },

    "RH": {
        "thm:RH.1": {
            "canonical_theorem": "thm:RH1",
            "canonical_section": "RH §Six-Step Ladder",
            "canonical_label": "RH1 — Canonical Object Xi [C]",
            "cross_check": "Branch target established: RH = reality condition on zeros of Xi",
        },
        "thm:RH.2": {
            "canonical_theorem": "thm:RH2",
            "canonical_section": "RH §Six-Step Ladder",
            "canonical_label": "RH2 — Spine Reduction [C]",
            "cross_check": "Prime/explicit-formula/zero data all descend from Xi",
        },
        "thm:RH.3": {
            "canonical_theorem": "thm:RH3",
            "canonical_section": "RH §Six-Step Ladder",
            "canonical_label": "RH3 — Admissible Probe Space H_RH [C]",
            "cross_check": "SCC-admissible probe space; RH iff K(t,u) positive-definite",
        },
        "ob:RH.4": {
            "canonical_theorem": "ob:RH4",
            "canonical_section": "RH §Six-Step Ladder",
            "canonical_label": "RH4 — Operator Realization (scaling-flow candidate) [C]",
            "cross_check": "Option (ii) conditionally realized; full operator realization pending",
        },
        "ob:RH.5": {
            "canonical_theorem": "ob:RH5",
            "canonical_section": "RH §Six-Step Ladder",
            "canonical_label": "RH5 — Selection Exclusion (SCC support-rigidity) [C]",
            "cross_check": "Conditionally hardened; SCC support-rigidity provides structural exclusion",
        },
        "ob:RH.6": {
            "canonical_theorem": "ob:RH6",
            "canonical_section": "RH §Six-Step Ladder",
            "canonical_label": "RH6 — Critical-Line Localization [C]",
            "cross_check": "Conditionally hardened; requires full RH4 at canonical force to complete",
        },
        "ob:RH.S1-TRACE": {
            "canonical_theorem": "S1-TRACE",
            "canonical_section": "RH §S1 Formal Packet",
            "canonical_label": "S1-TRACE — Trace Formula Pairing CONDITIONALLY DISCHARGED [C]",
            "cross_check": "Scaling-flow candidate conditionally realizes RH-N2 trace formula",
        },
        "ob:RH.S1-DESCENT": {
            "canonical_theorem": "S1-DESCENT",
            "canonical_section": "RH §S1 Formal Packet",
            "canonical_label": "S1-DESCENT — Arithmetic Descent Without Hidden Import CONDITIONALLY DISCHARGED [C]",
            "cross_check": "Transport-localization chain L1-L7; RH defect ledger",
        },
        "ob:RH.S1-COMP": {
            "canonical_theorem": "S1-COMP",
            "canonical_section": "RH §S1 Formal Packet",
            "canonical_label": "S1-COMP — SCC-Minimal Faithful Package DISCHARGED via SCC-MCS [C]",
            "cross_check": "Discharged by thm:SCC.MCS; SCC-MCS provides minimal faithful carrier",
        },
        "ob:RH.S1-ARC": {
            "canonical_theorem": "S1-ARC",
            "canonical_section": "RH §S1 Formal Packet — IRREDUCIBLE",
            "canonical_label": "S1-ARC — Q[psi]>=0 from arithmetic structure of Xi [O] IRREDUCIBLE",
            "cross_check": "THIS IS THE MATHEMATICAL CONTENT OF RH ITSELF. NOT discharged. Not claimed proved.",
        },
        "thm:RH.S1.formal": {
            "canonical_theorem": "ob:rh-s1-formal",
            "canonical_section": "RH §S1 Formal Packet",
            "canonical_label": "S1 Formal Witness Assembly — reduces to S1-ARC [O]",
            "cross_check": "Containing frontier; S1-TRACE/DESCENT/COMP conditionally discharged; S1-ARC remains",
        },
        "status:RH": {
            "canonical_theorem": "prop:RH-status",
            "canonical_section": "RH §Branch Status",
            "canonical_label": "RH Branch Status — CERT-PROJ",
            "cross_check": "Architecture constituted; S1-ARC is the irreducible arithmetic frontier",
        },
    },

    "BIO": {
        "ob:BIO.REP": {"canonical_theorem": "ob:BIO.REP", "canonical_section": "BIO §Obligations", "canonical_label": "Replication Certification [C]", "cross_check": "Discharged by thm:BIO.REP"},
        "ob:BIO.MET": {"canonical_theorem": "ob:BIO.MET", "canonical_section": "BIO §Obligations", "canonical_label": "Metabolic Bookkeeping [C]", "cross_check": "Discharged by thm:BIO.MET"},
        "ob:BIO.FID": {"canonical_theorem": "ob:BIO.FID", "canonical_section": "BIO §Obligations", "canonical_label": "Replication Fidelity Margin [C]", "cross_check": "Discharged by thm:BIO.FID; positive gap on C_Bio^nd"},
        "ob:BIO.NC":  {"canonical_theorem": "ob:BIO.NC",  "canonical_section": "BIO §Obligations", "canonical_label": "No-Hidden Hereditary Channel [C]", "cross_check": "Discharged by thm:BIO.NC"},
        "ob:BIO.HER": {"canonical_theorem": "ob:BIO.HER", "canonical_section": "BIO §Obligations", "canonical_label": "Hereditary Descent Transport [C]", "cross_check": "Discharged by thm:BIO.HER"},
        "ob:BIO.BND": {"canonical_theorem": "ob:BIO.BND", "canonical_section": "BIO §Obligations", "canonical_label": "Boundary Self-Organization (Nondegenerate Regime) [C]", "cross_check": "SCOPED discharge; nondegenerate regime only; BND-open remains"},
        "thm:BIO.REP": {"canonical_theorem": "thm:BIO.REP", "canonical_section": "BIO §Replication", "canonical_label": "Replication Kernel Certification [C]", "cross_check": "Source-descended from SCC.MCS; no biological primitives"},
        "thm:BIO.MET": {"canonical_theorem": "thm:BIO.MET", "canonical_section": "BIO §Metabolic", "canonical_label": "Metabolic Ledger Theorem [C]", "cross_check": "Additivity from carrier-transport algebra"},
        "thm:BIO.FID": {"canonical_theorem": "thm:BIO.FID", "canonical_section": "BIO §Fidelity", "canonical_label": "Replication Fidelity Margin Theorem [C]", "cross_check": "delta_fid > 0 from nondegeneracy of C_Bio^nd"},
        "thm:BIO.NC":  {"canonical_theorem": "thm:BIO.NC",  "canonical_section": "BIO §No-Hidden-Channel", "canonical_label": "No-Hidden Hereditary Channel Theorem [C]", "cross_check": "No undeclared hereditary pathways; Book V no-hidden-supplementation"},
        "thm:BIO.HER": {"canonical_theorem": "thm:BIO.HER", "canonical_section": "BIO §Hereditary", "canonical_label": "Hereditary Descent Transport Theorem [C]", "cross_check": "Book V branch-legitimacy satisfied on C_Bio^nd"},
        "thm:BIO.BND": {"canonical_theorem": "thm:BIO.BND", "canonical_section": "BIO §Boundary", "canonical_label": "Boundary Self-Organization (Nondegenerate Regime) [C]", "cross_check": "Book II capacity law; scoped to nondegenerate regime"},
        "thm:BIO.END": {"canonical_theorem": "thm:BIO.END", "canonical_section": "BIO §Endpoint", "canonical_label": "BIO Endpoint on C_Bio^nd [C]", "cross_check": "Conditional endpoint; REP through HER discharged; EVO/MULTI downstream"},
        "thm:BIO.MULTI.twocell": {"canonical_theorem": "thm:BIO.MULTI2", "canonical_section": "BIO §Assembly", "canonical_label": "Minimal Two-Unit Assembly A2 [C]", "cross_check": "BIO analogue of SPEC caesium calibration; not full multicellular biology"},
        "ob:BIO.BND-open": {"canonical_theorem": "ob:BIO.BND-open", "canonical_section": "BIO §Frontier", "canonical_label": "Boundary Self-Organization (Full Replicator Class) [O] ACTIVE FRONTIER", "cross_check": "Force question; BND for full class requires new ingredient or Book VI bridge"},
        "status:BIO": {"canonical_theorem": "status:BIO", "canonical_section": "BIO §Branch Status", "canonical_label": "BIO Branch Status — conditional-cert-close on C_Bio^nd", "cross_check": "No-smuggling maintained; EVO/MULTI not claimed"},
    },

    "LING": {
        "thm:LING.END": {"canonical_theorem": "thm:LING.END", "canonical_section": "LING §Endpoint", "canonical_label": "LING Endpoint — Contrast/Recursion/Context-Response [C]", "cross_check": "Conditional closure on declared contrast/recursion/context-response structure"},
        "ob:LING.REF-INVIS-RECOV": {"canonical_theorem": "ob:LING.REF", "canonical_section": "LING §Frontier", "canonical_label": "Reference Invisibility/Recovery Frontier [O] ACTIVE FRONTIER", "cross_check": "Reference recovery is live structural frontier; contrast closure does not solve it"},
        "status:LING": {"canonical_theorem": "status:LING", "canonical_section": "LING §Branch Status", "canonical_label": "LING Branch Status — conditional-cert-close", "cross_check": "Closed on contrast/recursion/context-response; REF-INVIS-RECOV preserved"},
    },

    "CRYST": {
        "thm:CRYST.END": {"canonical_theorem": "thm:CRYST.END", "canonical_section": "CRYST §Endpoint", "canonical_label": "CRYST Endpoint — Diffraction/Periodicity/Symmetry [C]", "cross_check": "Eight of nine obligations discharged; phase problem the principal frontier"},
        "ob:CRYST.phase-problem": {"canonical_theorem": "ob:CRYST.PHASE", "canonical_section": "CRYST §Frontier", "canonical_label": "Crystallographic Phase Problem [O] ACTIVE FRONTIER", "cross_check": "Generic non-centrosymmetric phase recovery; structurally parallel to RH S1-ARC"},
        "status:CRYST": {"canonical_theorem": "status:CRYST", "canonical_section": "CRYST §Branch Status", "canonical_label": "CRYST Branch Status — conditional-cert-close on diffraction-periodicity-symmetry domain", "cross_check": "Phase problem preserved; DOM-epsilon and EWALD-epsilon convergence conditions noted"},
    },

    "SCC": {
        "ob:SCC.MCS":  {"canonical_theorem": "ob:SCC.MCS",  "canonical_section": "SCC §Obligations", "canonical_label": "SCC Minimal Carrier Structure Obligation [C]", "cross_check": "Discharged by thm:SCC.MCS"},
        "ob:SCC.UC":   {"canonical_theorem": "ob:SCC.UC",   "canonical_section": "SCC §Obligations", "canonical_label": "SCC Universality Condition Obligation [C]", "cross_check": "Discharged by thm:SCC.UC"},
        "ob:SCC.TSI":  {"canonical_theorem": "ob:SCC.TSI",  "canonical_section": "SCC §Obligations", "canonical_label": "SCC Total Structural Integration Obligation [C]", "cross_check": "Discharged by thm:SCC.TSI"},
        "thm:SCC.MCS": {"canonical_theorem": "thm:SCC.MCS", "canonical_section": "SCC §MCS", "canonical_label": "SCC Minimal Carrier Structure Theorem [C]", "cross_check": "Structural counterfactual capacity at minimal faithful carrier level; feeds RH.S1-COMP"},
        "thm:SCC.UC":  {"canonical_theorem": "thm:SCC.UC",  "canonical_section": "SCC §UC", "canonical_label": "SCC Universality Condition Theorem [C]", "cross_check": "Universal role-carrier universality; feeds downstream branches"},
        "thm:SCC.TSI": {"canonical_theorem": "thm:SCC.TSI", "canonical_section": "SCC §TSI", "canonical_label": "SCC Total Structural Integration Theorem [C]", "cross_check": "MCS+UC+TSI packet gives conditional CERT-CLOSE; no phenomenological overclaim"},
        "status:SCC":  {"canonical_theorem": "status:SCC",  "canonical_section": "SCC §Branch Status", "canonical_label": "SCC Branch Status — conditional-cert-close (MCS+UC+TSI)", "cross_check": "No active SCC-local frontier; feeds RH/BIO/YM structurally"},
    },

    "SPEC": {
        "thm:SPEC.10.1": {"canonical_theorem": "thm:SPEC.10.1", "canonical_section": "SPEC §Endpoint", "canonical_label": "SPEC Gauge-Response Spectroscopy Endpoint [U]", "cross_check": "CERT-CLOSE on gauge-response regime; matter-rich spectroscopy gated on SM.matter"},
        "status:SPEC":   {"canonical_theorem": "status:SPEC",   "canonical_section": "SPEC §Branch Status", "canonical_label": "SPEC Branch Status — cert-close on gauge-response spectroscopy", "cross_check": "Cleanest closure result; no active SPEC-local frontier in declared scope"},
    },
}

# ─────────────────────────────────────────────────────────────────────────
# Certificate configuration per branch
# ─────────────────────────────────────────────────────────────────────────

BRANCH_CERT_CONFIGS = {
    "NS": {
        "posture": "domain-bounded-cert-close",
        "active_frontier": "front:NS.main",
        "frontier_label": "Stage-3 Global Unconditional Regularity (Clay Prize)",
        "key_narrative": (
            "NS reaches domain-bounded conditional CERT-CLOSE via the "
            "NS.6.1+NS.7.1 chain under Phase-A/K_0=7/PASS/LS-2. "
            "Stage-3 global unconditional regularity (Clay Millennium Prize) "
            "is the external frontier. ob:NS.SB2 conditionally discharged via SCT.6b. "
            "Stale preamble (frontier-blocked) corrected in v31."
        ),
        "cert_order": [
            "thm:NS.stage0", "thm:NS.stage1", "thm:NS.stage2a", "thm:NS.stage2b",
            "thm:NS.leray", "thm:NS.window-uniformity", "thm:NS.6.1",
            "thm:NS.Ren5", "thm:NS.SB2-discharged", "ob:NS.SB2",
            "thm:NS.7.1", "cor:NS.domain-bounded-cert-close",
            "prop:NS.status", "ob:NS.bridge-stage2", "front:NS.main", "status:NS",
        ],
        "special_note": "Stale-posture correction: preamble says frontier-blocked; actual posture is domain-bounded-cert-close.",
    },
    "SM": {
        "posture": "intrinsic-structural-close",
        "active_frontier": "ob:SM.O-IDcont",
        "frontier_label": "O-IDcont Continuum/Operator Identification Force Upgrade",
        "key_narrative": (
            "SM has conditional intrinsic structural closure: four internal obligations "
            "(Harmonization, Matter, Higgs, CouplingTransfer) conditionally discharged. "
            "Status(SM) <= Status(YM) AND Status(GR). O-IDcont blocks unconditional closure. "
            "Corrected from CERT-PROJ by prop:SM.status-reconciliation."
        ),
        "cert_order": [
            "ob:SM.harmonization", "ob:SM.matter", "ob:SM.higgs", "ob:SM.coupling-transfer",
            "thm:SM.gauge-chain", "thm:SM.three-gen",
            "thm:SM.harmonization-partial", "thm:SM.coupling-transfer-full",
            "thm:SM.higgs-source-descended", "thm:SM.18.1",
            "prop:SM.intrinsic-closure", "prop:SM.status-reconciliation",
            "ob:SM.O-IDcont", "status:SM",
        ],
        "special_note": "First pilot to exercise intrinsic-structural-close posture. thm:SM.three-gen is [U] (unconditional).",
    },
    "RH": {
        "posture": "cert-proj",
        "active_frontier": "ob:RH.S1-ARC",
        "frontier_label": "S1-ARC: Q[psi]>=0 from arithmetic structure of Xi — IRREDUCIBLE",
        "key_narrative": (
            "RH architecture constituted through RH1-RH3. S1-TRACE/DESCENT/COMP "
            "conditionally discharged. S1-ARC is the irreducible arithmetic frontier: "
            "this is the mathematical content of RH itself. "
            "THIS CERTIFICATE DOES NOT PROVE THE RIEMANN HYPOTHESIS."
        ),
        "cert_order": [
            "thm:RH.1", "thm:RH.2", "thm:RH.3",
            "ob:RH.4", "ob:RH.5", "ob:RH.6",
            "ob:RH.S1-TRACE", "ob:RH.S1-DESCENT", "ob:RH.S1-COMP",
            "ob:RH.S1-ARC", "thm:RH.S1.formal", "status:RH",
        ],
        "special_note": "CRITICAL: S1-ARC is [O]. This certificate explicitly records that RH is not proved.",
    },
    "BIO": {
        "posture": "conditional-cert-close",
        "active_frontier": "ob:BIO.BND-open",
        "frontier_label": "Boundary Self-Organization for Full Replicator Class",
        "key_narrative": (
            "BIO reaches its endpoint on the nondegenerate certified biological class C_Bio^nd. "
            "REP through HER obligations conditionally discharged. "
            "BND scoped to nondegenerate regime; BND-open remains for full class. "
            "No-smuggling boundary maintained throughout."
        ),
        "cert_order": [
            "ob:BIO.REP", "thm:BIO.REP", "ob:BIO.MET", "thm:BIO.MET",
            "ob:BIO.FID", "thm:BIO.FID", "ob:BIO.NC", "thm:BIO.NC",
            "ob:BIO.HER", "thm:BIO.HER", "ob:BIO.BND", "thm:BIO.BND",
            "thm:BIO.END", "thm:BIO.MULTI.twocell",
            "ob:BIO.BND-open", "status:BIO",
        ],
        "special_note": "No biological primitives (genes, cells, fitness, membrane biophysics) imported.",
    },
    "LING": {
        "posture": "conditional-cert-close",
        "active_frontier": "ob:LING.REF-INVIS-RECOV",
        "frontier_label": "Reference Invisibility/Recovery Frontier",
        "key_narrative": (
            "LING closes on contrast, recursion, and context-response structure. "
            "Reference invisibility/recovery is the live structural frontier."
        ),
        "cert_order": ["thm:LING.END", "ob:LING.REF-INVIS-RECOV", "status:LING"],
        "special_note": None,
    },
    "CRYST": {
        "posture": "conditional-cert-close",
        "active_frontier": "ob:CRYST.phase-problem",
        "frontier_label": "Crystallographic Phase Problem",
        "key_narrative": (
            "CRYST closes on diffraction-periodicity-symmetry domain. "
            "Eight of nine obligations discharged. Phase problem is the principal frontier, "
            "structurally parallel to RH S1-ARC."
        ),
        "cert_order": ["thm:CRYST.END", "ob:CRYST.phase-problem", "status:CRYST"],
        "special_note": None,
    },
    "SCC": {
        "posture": "conditional-cert-close",
        "active_frontier": None,
        "frontier_label": "No active SCC-local frontier",
        "key_narrative": (
            "SCC MCS+UC+TSI packet gives conditional CERT-CLOSE on structural "
            "counterfactual capacity. No active SCC-local frontier. "
            "SCC feeds RH/BIO/YM structurally (MCS discharged RH.S1-COMP)."
        ),
        "cert_order": [
            "ob:SCC.MCS", "thm:SCC.MCS",
            "ob:SCC.UC", "thm:SCC.UC",
            "ob:SCC.TSI", "thm:SCC.TSI",
            "status:SCC",
        ],
        "special_note": "No phenomenological or consciousness overclaim.",
    },
    "SPEC": {
        "posture": "cert-close",
        "active_frontier": None,
        "frontier_label": "No active SPEC-local frontier (gauge-response scope)",
        "key_narrative": (
            "SPEC is the cleanest closure result: CERT-CLOSE on gauge-response "
            "spectroscopy regime. Matter-rich spectroscopy gated on SM.matter. "
            "thm:SPEC.10.1 is [U] — unconditional at declared scope."
        ),
        "cert_order": ["thm:SPEC.10.1", "status:SPEC"],
        "special_note": None,
    },
}
