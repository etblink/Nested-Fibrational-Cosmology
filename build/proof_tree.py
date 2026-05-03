"""
build/proof_tree.py — v33 Proof Tree Engine

Generates structured, human-readable "proof trees" for each branch pilot,
showing the full dependency chain from posture to leaf claims.

This is the primary L3 hardening deliverable: it makes governance outputs
auditable rather than just present. A domain expert should be able to read
the proof tree for GR or YM and verify that the inferred posture follows
from the stated dependencies.

Output:
  output/reports/proof_trees.json
  output/tables/proof_trees.md
  output/tables/proof_trees_summary.md
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

import yaml

ROOT = Path(__file__).resolve().parents[1]
REPORTS = ROOT / "output" / "reports"
TABLES = ROOT / "output" / "tables"

REPORTS.mkdir(parents=True, exist_ok=True)
TABLES.mkdir(parents=True, exist_ok=True)

# Branch posture inference rules — parallel to validate.py posture_rules
# Each entry: (status_id, basis_ids, posture, narrative)
POSTURE_INFERENCE_RULES: List[Tuple[str, List[str], str, str]] = [
    (
        "status:GR",
        ["thm:GR.domain", "ob:GR.global-subcriticality"],
        "domain-bounded-cert-close",
        "GR closure chain reaches the declared domain endpoint; global curvature-subcriticality remains the only surviving frontier.",
    ),
    (
        "status:YM",
        ["thm:YM.7", "thm:YM.B1.bridge", "thm:YM.B2.bridge", "thm:YM.B3.bridge", "ob:YM.B3.A2"],
        "conditional-cert-close",
        "YM bridge stack establishes conditional closure at MSC-normalized scope; B3-A2 is the surviving residual obligation.",
    ),
    (
        "status:NS",
        ["thm:NS.7.1", "thm:NS.6.1", "front:NS.main"],
        "domain-bounded-cert-close",
        "NS.6.1+NS.7.1 chain gives domain-bounded conditional CERT-CLOSE; Stage-3 global unconditional regularity (Clay) is the external frontier.",
    ),
    (
        "status:SM",
        ["thm:SM.18.1", "ob:SM.O-IDcont"],
        "intrinsic-structural-close",
        "SM internal obligations conditionally discharged; O-IDcont force upgrade blocks unconditional closure; inherited YM/GR scope limits apply.",
    ),
    (
        "status:SPEC",
        ["thm:SPEC.10.1"],
        "cert-close",
        "SPEC gauge-response spectroscopy endpoint achieved unconditionally at declared scope; no active SPEC-local frontier.",
    ),
    (
        "status:SCC",
        ["thm:SCC.MCS", "thm:SCC.UC", "thm:SCC.TSI"],
        "conditional-cert-close",
        "SCC MCS+UC+TSI packet conditionally establishes structural counterfactual capacity; no active SCC-local frontier.",
    ),
    (
        "status:BIO",
        ["thm:BIO.END", "ob:BIO.BND-open"],
        "conditional-cert-close",
        "BIO endpoint reached on nondegenerate C_Bio^nd; BND for full replicator class remains the active structural frontier.",
    ),
    (
        "status:LING",
        ["thm:LING.END", "ob:LING.REF-INVIS-RECOV"],
        "conditional-cert-close",
        "LING contrast/recursion/context-response structure conditionally closed; reference invisibility/recovery is the active frontier.",
    ),
    (
        "status:CRYST",
        ["thm:CRYST.END", "ob:CRYST.phase-problem"],
        "conditional-cert-close",
        "CRYST diffraction-periodicity-symmetry endpoint conditionally achieved; phase problem remains the active frontier.",
    ),
    (
        "status:RH",
        ["thm:RH.3", "ob:RH.S1-ARC"],
        "cert-proj",
        "RH architecture constituted through RH1-RH3; S1-TRACE/DESCENT/COMP conditionally discharged; S1-ARC is the irreducible arithmetic frontier.",
    ),
]

# Discharge mode labels for display
DISCHARGE_MODE_LABELS = {
    "full": "full discharge ✓",
    "partial": "partial discharge (progress recorded; obligation remains open)",
    "scoped": "scoped discharge (closed on sub-regime only)",
    "superseding": "superseding discharge (obligation reformulated)",
}

# Status display labels
STATUS_LABELS = {
    "U": "[U] unconditional",
    "C": "[C] conditional",
    "O": "[O] open",
    "D": "[D] definition",
    "B": "[B] bridge",
    "R": "[R] remark",
    "domain-bounded-cert-close": "domain-bounded CERT-CLOSE",
    "conditional-cert-close": "conditional CERT-CLOSE",
    "intrinsic-structural-close": "intrinsic-structural-close",
    "cert-close": "CERT-CLOSE",
    "cert-proj": "CERT-PROJ",
    "frontier-blocked": "frontier-blocked",
}


def load_all_claims() -> Dict[str, Dict[str, Any]]:
    """Load all claim records from all branches."""
    claims: Dict[str, Dict[str, Any]] = {}
    for branch_dir in (ROOT / "claims" / "branches").iterdir():
        if branch_dir.is_dir():
            for path in branch_dir.glob("*.yaml"):
                data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
                cid = data.get("id")
                if cid:
                    claims[cid] = data
    # Also spine claims
    for spine_dir in (ROOT / "claims" / "spine").iterdir() if (ROOT / "claims" / "spine").exists() else []:
        if spine_dir.is_dir():
            for path in spine_dir.glob("*.yaml"):
                data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
                cid = data.get("id")
                if cid:
                    claims[cid] = data
    return claims


def load_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def get_deps(claim: Dict[str, Any]) -> List[str]:
    deps_raw = claim.get("dependencies", {}) or {}
    if isinstance(deps_raw, dict):
        return deps_raw.get("requires", []) or []
    return list(deps_raw) if deps_raw else []


def get_discharges(claim: Dict[str, Any]) -> List[Dict[str, Any]]:
    return claim.get("discharges", []) or []


def get_status(cid: str, claims: Dict, computed: Dict) -> str:
    eff = computed.get(cid, {}).get("effective_status")
    if eff:
        return eff
    claim = claims.get(cid, {})
    return claim.get("declared_status", "?")


def build_proof_tree(
    root_id: str,
    claims: Dict[str, Dict[str, Any]],
    computed: Dict[str, Any],
    max_depth: int = 4,
    visited: Optional[Set[str]] = None,
    depth: int = 0,
) -> Dict[str, Any]:
    """Build a recursive proof tree node."""
    if visited is None:
        visited = set()

    claim = claims.get(root_id, {})
    status = get_status(root_id, claims, computed)
    kind = claim.get("kind", "unknown")
    title = claim.get("title", root_id)

    node: Dict[str, Any] = {
        "id": root_id,
        "kind": kind,
        "title": title,
        "status": status,
        "status_label": STATUS_LABELS.get(status, status),
        "children": [],
        "discharge_targets": [],
        "scope_regime": (claim.get("scope", {}) or {}).get("regime", ""),
        "scope_cert": (claim.get("scope", {}) or {}).get("certificate_scope", ""),
        "promotion_ceiling": (claim.get("scope", {}) or {}).get("promotion_ceiling", ""),
        "is_frontier": kind == "frontier" or status == "O",
        "is_leaf": False,
        "truncated": False,
    }

    # Record discharge targets for this claim
    for d in get_discharges(claim):
        target = d.get("target", "")
        mode = d.get("kind", "")
        if target:
            node["discharge_targets"].append({
                "target": target,
                "mode": mode,
                "mode_label": DISCHARGE_MODE_LABELS.get(mode, mode),
                "basis": d.get("basis", []),
                "scope_relation": d.get("scope_relation", ""),
            })

    if depth >= max_depth or root_id in visited:
        node["truncated"] = root_id in visited and depth > 0
        node["is_leaf"] = True
        return node

    visited_copy = visited | {root_id}
    deps = get_deps(claim)

    if not deps:
        node["is_leaf"] = True
    else:
        for dep_id in deps[:6]:  # cap children
            child = build_proof_tree(dep_id, claims, computed, max_depth, visited_copy, depth + 1)
            node["children"].append(child)

    return node


def format_tree_md(
    node: Dict[str, Any],
    indent: int = 0,
    is_last: bool = True,
    prefix: str = "",
) -> List[str]:
    """Render a proof tree node as Markdown lines."""
    pad = "  " * indent
    status_str = node.get("status_label", node.get("status", "?"))
    kind_str = node.get("kind", "")
    title_str = node.get("title", node["id"])[:70]

    # Status badge
    s = node.get("status", "")
    if s == "O":
        badge = "🔴"
    elif s == "C":
        badge = "🟡"
    elif s == "U":
        badge = "🟢"
    elif s in ("domain-bounded-cert-close", "conditional-cert-close",
                "cert-close", "intrinsic-structural-close"):
        badge = "✅"
    elif s == "cert-proj":
        badge = "🔵"
    else:
        badge = "⚪"

    line = f"{pad}- {badge} `{node['id']}` **{status_str}** _{kind_str}_"
    if title_str and title_str != node["id"]:
        line += f"  \n{pad}  ↳ _{title_str}_"

    scope_bits = []
    if node.get("scope_regime"):
        scope_bits.append(f"regime=`{node['scope_regime']}`")
    if node.get("scope_cert"):
        scope_bits.append(f"cert=`{node['scope_cert']}`")
    if node.get("promotion_ceiling"):
        scope_bits.append(f"ceiling=`{node['promotion_ceiling']}`")
    if scope_bits:
        line += f"  \n{pad}  📐 {', '.join(scope_bits)}"

    lines = [line]

    # Discharge targets
    for dt in node.get("discharge_targets", []):
        lines.append(
            f"{pad}  ⚡ discharges `{dt['target']}` "
            f"via **{dt['mode_label']}**"
        )

    if node.get("truncated"):
        lines.append(f"{pad}  _(cycle detected — not expanded)_")
    elif node.get("is_leaf") and not node.get("children"):
        if not node.get("discharge_targets"):
            lines.append(f"{pad}  _(leaf — no dependencies)_")

    for i, child in enumerate(node.get("children", [])):
        child_lines = format_tree_md(
            child, indent + 1, i == len(node["children"]) - 1, prefix
        )
        lines.extend(child_lines)

    return lines


def generate_branch_tree(
    branch: str,
    status_id: str,
    basis_ids: List[str],
    posture: str,
    narrative: str,
    claims: Dict[str, Dict[str, Any]],
    computed: Dict[str, Any],
) -> Dict[str, Any]:
    """Generate the full proof tree for one branch posture."""
    posture_status = STATUS_LABELS.get(posture, posture)

    # Identify active frontiers
    frontiers = []
    for cid in basis_ids:
        s = get_status(cid, claims, computed)
        claim = claims.get(cid, {})
        if s == "O" or claim.get("kind") == "frontier":
            frontiers.append({"id": cid, "title": claim.get("title", cid)})

    # Build trees for each basis item
    basis_trees = []
    for bid in basis_ids:
        tree = build_proof_tree(bid, claims, computed, max_depth=4, visited={status_id})
        basis_trees.append(tree)

    return {
        "branch": branch,
        "status_id": status_id,
        "posture": posture,
        "posture_label": posture_status,
        "narrative": narrative,
        "basis_ids": basis_ids,
        "active_frontiers": frontiers,
        "basis_trees": basis_trees,
    }


def render_branch_md(branch_tree: Dict[str, Any]) -> List[str]:
    branch = branch_tree["branch"]
    posture = branch_tree["posture_label"]
    narrative = branch_tree["narrative"]
    frontiers = branch_tree["active_frontiers"]

    lines = [
        f"## {branch}",
        "",
        f"**Posture:** `{branch_tree['posture']}`  {posture}",
        "",
        f"**Narrative:** {narrative}",
        "",
    ]

    if frontiers:
        lines.append("**Active frontiers:**")
        for f in frontiers:
            lines.append(f"- 🔴 `{f['id']}` — {f['title']}")
        lines.append("")

    lines += [
        "**Proof tree** (basis items → dependencies, max depth 4):",
        "",
    ]

    for tree in branch_tree["basis_trees"]:
        tree_lines = format_tree_md(tree, indent=0)
        lines.extend(tree_lines)
        lines.append("")

    return lines


def render_summary_md(all_trees: List[Dict[str, Any]]) -> List[str]:
    lines = [
        "# v33 Branch Posture Proof Tree Summary",
        "",
        "| Branch | Posture | Active frontiers | Basis depth |",
        "|--------|---------|-----------------|-------------|",
    ]
    for bt in all_trees:
        frontier_strs = ", ".join(
            f"`{f['id']}`" for f in bt["active_frontiers"]
        ) or "none"
        max_depth = max(
            (bt.get("max_depth_reached", 0),),
        )
        lines.append(
            f"| {bt['branch']} | `{bt['posture']}` "
            f"| {frontier_strs} | — |"
        )
    lines += [
        "",
        "## Legend",
        "",
        "- 🟢 `[U]` Unconditional",
        "- 🟡 `[C]` Conditional",
        "- 🔴 `[O]` Open / frontier",
        "- ✅ Branch posture: cert-close / conditional-cert-close / domain-bounded",
        "- 🔵 Branch posture: cert-proj",
        "- ⚡ Discharge edge (with mode)",
        "- 📐 Scope annotation",
    ]
    return lines


def main() -> int:
    claims = load_all_claims()
    computed = load_json(REPORTS / "computed_statuses.json")

    all_trees = []
    for status_id, basis_ids, posture, narrative in POSTURE_INFERENCE_RULES:
        branch = status_id.replace("status:", "")
        bt = generate_branch_tree(
            branch, status_id, basis_ids, posture, narrative, claims, computed
        )
        all_trees.append(bt)

    # Write JSON report
    (REPORTS / "proof_trees.json").write_text(
        json.dumps(
            [
                {
                    "branch": bt["branch"],
                    "status_id": bt["status_id"],
                    "posture": bt["posture"],
                    "narrative": bt["narrative"],
                    "active_frontiers": bt["active_frontiers"],
                    "basis_ids": bt["basis_ids"],
                }
                for bt in all_trees
            ],
            indent=2,
        ),
        encoding="utf-8",
    )

    # Write full tree Markdown
    full_lines = [
        "# v33 Branch Posture Proof Trees",
        "",
        "Per-branch structured dependency chains from posture to leaf claims.",
        "Generated by `build/proof_tree.py`.",
        "",
    ]
    for bt in all_trees:
        full_lines.extend(render_branch_md(bt))
        full_lines.append("---")
        full_lines.append("")

    (TABLES / "proof_trees.md").write_text(
        "\n".join(full_lines) + "\n", encoding="utf-8"
    )

    # Write summary
    summary_lines = render_summary_md(all_trees)
    (TABLES / "proof_trees_summary.md").write_text(
        "\n".join(summary_lines) + "\n", encoding="utf-8"
    )

    print(
        json.dumps(
            {
                "status": "passed",
                "branches_traced": len(all_trees),
                "branch_postures": {bt["branch"]: bt["posture"] for bt in all_trees},
                "active_frontiers_all": [
                    f["id"]
                    for bt in all_trees
                    for f in bt["active_frontiers"]
                ],
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
