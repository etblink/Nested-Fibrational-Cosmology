#!/usr/bin/env python3
"""
Regenerate the current-snapshot portion of NFC_STATE_OF_CANON.md from the
metadata layer (post-v1.0 task: counts, branch table, frontier table, and
validation facts are GENERATED, never hand-typed).

Contract:
  * Everything ABOVE the HISTORICAL_MARKER is regenerated from metadata/.
  * Everything BELOW the marker is hand-maintained history, preserved verbatim.
  * Idempotent: rerunning on unchanged metadata yields identical output except
    the timestamp line, which carries the census commit for provenance.
Run via `make state` (wired in Makefile). Requires `make metadata` first.
"""
import json, subprocess, datetime, sys, os, collections

def build_timestamp():
    sde = os.environ.get("SOURCE_DATE_EPOCH")
    if sde:
        return datetime.datetime.fromtimestamp(int(sde), datetime.timezone.utc)
    try:
        ct = subprocess.check_output(["git","log","-1","--format=%ct"],
                                     stderr=subprocess.DEVNULL).decode().strip()
        return datetime.datetime.fromtimestamp(int(ct), datetime.timezone.utc)
    except Exception:
        return datetime.datetime.now(datetime.timezone.utc)

def resolve_commit(census):
    # explicit CLI arg > env > census.json value
    for i, a in enumerate(sys.argv):
        if a == "--commit" and i + 1 < len(sys.argv):
            return sys.argv[i + 1]
    return os.environ.get("NFC_CENSUS_COMMIT") or census.get("census_commit", "unknown")

MARKER = "<!-- ===== HISTORICAL HAND-MAINTAINED RECORD BELOW: GENERATOR PRESERVES VERBATIM ===== -->"
TARGET = "NFC_STATE_OF_CANON.md"

def load(p): return json.load(open(p))

def validation_facts():
    r = subprocess.run([sys.executable, "scripts/validate.py"], capture_output=True, text=True)
    out = r.stdout
    j = out[out.index("{"):out.rindex("}")+1]
    return json.loads(j), ("PASS" if r.returncode == 0 else "FAIL")

def main():
    census = load("metadata/census.json"); views = load("metadata/views.json")
    claims = load("metadata/claims.json")
    vfacts, vstatus = validation_facts()
    raw = census["raw_grep_census"]; env = census["environment_census"]
    acc = census["frontier_accountings"]

    per_branch = collections.defaultdict(lambda: collections.Counter())
    for c in claims: per_branch[c["branch"]][c["status_tag"]] += 1

    open_items = [c for c in claims if c["status_tag"] == "O"]

    L = []
    A = L.append
    A("# NFC Canon: State of the Canon")
    A("")
    A(f"> **GENERATED SNAPSHOT** — produced by `scripts/generate_state_of_canon.py` from the")
    A(f"> metadata layer (census commit `{resolve_commit(census)}`, generated {build_timestamp().strftime('%Y-%m-%d %H:%MZ')}).")
    A(f"> Do not hand-edit above the historical marker; run `make state` to refresh.")
    A(f"> Historical session material is preserved verbatim below the marker.")
    A("")
    A("## Corpus Overview (generated)")
    A("")
    A("| Measure | Value |")
    A("|---|---|")
    A("| Canon files | 17 (7 spine + 10 branch) |")
    A(f"| Status-tagged claim records | {len(claims)} |")
    for k in ["D","U","C","B","O","R"]:
        A(f"| [{k}]-tagged (raw census) | **{raw[k]}** |")
    A(f"| Prose-mention delta (raw − declarations) | {census['prose_mention_delta']} |")
    A(f"| Unique labels | {vfacts['labels'] and vfacts['unique_labels']} |")
    A(f"| Dangling references | {vfacts['dangling']} |")
    A(f"| Proof-citation cycles | {vfacts['cycles']} |")
    A(f"| Validation suite | **{vstatus}** |")
    A("")
    A("*Counting note: the raw census counts every `\\status{X}` occurrence; the")
    A("environment-declaration census (claim records) excludes inline prose mentions.")
    A(f"Declarations: {dict(env)}. Both are regenerated, never hand-typed (F-3 resolution).*")
    A("")
    A("## Branch Status Summary (generated)")
    A("")
    A("| Branch | Current posture (verbatim A1 status proposition) | D | U | C | B | O | R |")
    A("|---|---|---|---|---|---|---|---|")
    for b, posture in views["branch_posture_view"].items():
        s = per_branch[b]
        A(f"| {b} | {posture} | {s['D']} | {s['U']} | {s['C']} | {s['B']} | {s['O']} | {s['R']} |")
    s = per_branch["SPINE"]
    A(f"| SPINE (Books I–VII) | Stable foundational/governance layer | {s['D']} | {s['U']} | {s['C']} | {s['B']} | {s['O']} | {s['R']} |")
    A("")
    A(f"## Open Obligation Register (generated — syntactic [O] census: {len(open_items)} items)")
    A("")
    A("| Label | Branch | Section | Discharge basis / residual |")
    A("|---|---|---|---|")
    for c in sorted(open_items, key=lambda x: x["claim_id"]):
        A(f"| `{c['claim_id']}` | {c['branch']} | {c['source_section']} | {c.get('discharge_basis') or '—'} |")
    A("")
    A("## Frontier Accountings (generated — four accountings, NEVER summed)")
    A("")
    A(f"| # | Accounting | Count | Measures |")
    A(f"|---|---|---|---|")
    A(f"| I | Syntactic [O] census | {acc['I_syntactic_O_census']['count']} | {acc['I_syntactic_O_census']['measures']} |")
    A(f"| II | Named `ob:` roster | {acc['II_named_obligation_roster']['count']} | {acc['II_named_obligation_roster']['measures']} |")
    A(f"| III | Reduced irreducible frontier | {acc['III_reduced_irreducible_frontier']['count']} | {acc['III_reduced_irreducible_frontier']['measures']} |")
    A(f"| IV | Branch posture | 10 branches | {acc['IV_branch_posture']['measures']} |")
    A("")
    A("**Reduced irreducible frontier (III):**")
    for it in acc["III_reduced_irreducible_frontier"]["items"]:
        A(f"- **{it['item']}** — labels: " + ", ".join(f"`{l}`" for l in it["labels"]))
    A("")
    A(MARKER)
    generated = "\n".join(L) + "\n"

    old = open(TARGET, encoding="utf-8").read()
    if MARKER in old:
        historical = old.split(MARKER, 1)[1]
    else:
        # first run: everything from "## Governance Additions" onward is historical
        idx = old.index("## Governance Additions")
        historical = old[idx:]
    historical = "\n\n" + historical.lstrip("\n")
    open(TARGET, "w", encoding="utf-8").write(generated + historical)
    print(f"regenerated {TARGET}: {len(generated.splitlines())} generated lines + preserved history")

if __name__ == "__main__":
    main()
