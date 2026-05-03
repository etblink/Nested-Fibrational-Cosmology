from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

import yaml

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / "canon"
REPORTS = ROOT / "output" / "reports"
TABLES = ROOT / "output" / "tables"


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def project_config() -> Dict[str, Any]:
    return load_yaml(CANON / "project_governance.yaml")


def release_path(name: str) -> Path:
    # Config uses file stem form, e.g. L_plus_4, L_plus_5_draft.
    return CANON / "releases" / f"{name}.yaml"


def normalize_set(values: Any) -> set[str]:
    if values is None:
        return set()
    return set(str(v) for v in values)


def change_basis_index(target: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for entry in target.get("change_basis", []) or []:
        cid = entry.get("change_id")
        if cid:
            out[str(cid)] = entry
    return out


def add_change(
    changes: List[Dict[str, Any]],
    basis_index: Dict[str, Dict[str, Any]],
    change_id: str,
    category: str,
    item: str,
    before: Any = None,
    after: Any = None,
) -> None:
    basis = basis_index.get(change_id)
    changes.append({
        "change_id": change_id,
        "category": category,
        "item": item,
        "before": before,
        "after": after,
        "has_basis": basis is not None,
        "basis": basis.get("basis", []) if basis else [],
        "change_type": basis.get("change_type") if basis else None,
        "scope_relation": basis.get("scope_relation") if basis else None,
        "note": basis.get("note", "") if basis else "",
    })


def diff_releases(source: Dict[str, Any], target: Dict[str, Any]) -> Dict[str, Any]:
    source_name = source.get("release", "source")
    target_name = target.get("release", "target")
    basis_index = change_basis_index(target)
    changes: List[Dict[str, Any]] = []

    # Branch posture changes.
    source_postures = source.get("effective_branch_postures", {}) or {}
    target_postures = target.get("effective_branch_postures", {}) or {}
    for branch in sorted(set(source_postures) | set(target_postures)):
        before = source_postures.get(branch)
        after = target_postures.get(branch)
        if before != after:
            if before is None:
                change_id = f"branch-posture:add:{branch}"
            elif after is None:
                change_id = f"branch-posture:remove:{branch}"
            else:
                change_id = f"branch-posture:update:{branch}"
            add_change(changes, basis_index, change_id, "branch-posture", branch, before, after)

    # Active obligation/frontier changes.
    source_open = normalize_set(source.get("active_obligations"))
    target_open = normalize_set(target.get("active_obligations"))
    for item in sorted(source_open - target_open):
        add_change(
            changes,
            basis_index,
            f"active-obligation:remove:{item}",
            "active-obligation",
            item,
            before="active",
            after="absent",
        )
    for item in sorted(target_open - source_open):
        add_change(
            changes,
            basis_index,
            f"active-obligation:add:{item}",
            "active-obligation",
            item,
            before="absent",
            after="active",
        )

    missing_basis = [c for c in changes if not c.get("has_basis")]
    category_counts: Dict[str, int] = {}
    for c in changes:
        category_counts[c["category"]] = category_counts.get(c["category"], 0) + 1

    return {
        "source_release": source_name,
        "target_release": target_name,
        "target_status": target.get("status", "unspecified"),
        "changes": changes,
        "change_count": len(changes),
        "missing_basis_count": len(missing_basis),
        "category_counts": category_counts,
        "missing_basis": missing_basis,
    }


def write_reports(diff: Dict[str, Any]) -> None:
    REPORTS.mkdir(parents=True, exist_ok=True)
    TABLES.mkdir(parents=True, exist_ok=True)

    with (REPORTS / "release_diff_report.json").open("w", encoding="utf-8") as f:
        json.dump(diff, f, indent=2)

    lines = [
        "# Release Diff Report",
        "",
        f"**Source release:** `{diff.get('source_release')}`",
        f"**Target release:** `{diff.get('target_release')}`",
        f"**Target status:** `{diff.get('target_status')}`",
        f"**Detected changes:** {diff.get('change_count', 0)}",
        f"**Changes missing basis:** {diff.get('missing_basis_count', 0)}",
        "",
        "| Change ID | Category | Item | Before | After | Basis? | Type | Scope | Note |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    for change in diff.get("changes", []):
        row = [
            change.get("change_id", ""),
            change.get("category", ""),
            change.get("item", ""),
            change.get("before", ""),
            change.get("after", ""),
            "yes" if change.get("has_basis") else "NO",
            change.get("change_type", ""),
            change.get("scope_relation", ""),
            change.get("note", ""),
        ]
        lines.append("| " + " | ".join(str(x).replace("|", "\\|") for x in row) + " |")

    if diff.get("missing_basis"):
        lines += ["", "## Missing basis items", ""]
        for change in diff["missing_basis"]:
            lines.append(f"- `{change['change_id']}`")

    (TABLES / "release_diff_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    cfg = project_config()
    source_name = cfg.get("active_release", "L_plus_4")
    target_name = cfg.get("comparison_release", "L_plus_5_draft")
    source = load_yaml(release_path(source_name))
    target = load_yaml(release_path(target_name))
    diff = diff_releases(source, target)
    write_reports(diff)
    print(json.dumps({
        "source_release": diff["source_release"],
        "target_release": diff["target_release"],
        "change_count": diff["change_count"],
        "missing_basis_count": diff["missing_basis_count"],
    }, indent=2))


if __name__ == "__main__":
    main()
