# NFC Rewrite & Maintenance Policy

**Produced:** Phase 3 (policy only — no canon file edited).
**Binds:** every edit proposed in `CANON_REWRITE_PLAN.md` (Phase 4) and every patch applied in Phase 7.
**Supremacy:** where this policy and convenience conflict, this policy wins. Where this policy and the **core rule** (preserve meaning, proof force, dependency structure, theorem labels, obligation labels, status scope unless an explicit migration entry explains the change) conflict, the **core rule** wins.

---

## Part I — The eight required rules (as adopted, made operational)

### Rule 1 — Front blocks are constitutional intake, and must be labeled as such.
A front block (a file's `%%` header status line, its `\author{… Prospective …}` line, its "Purpose / Canonical Seed / Front Block" section, its "initial endpoint" and "strategic path" prose) records the branch's **original constitution and founding obligations**, not its current status.
- **Operationalization:** Each such block that currently reads as a status claim gets one added marker line — `%% [CONSTITUTIONAL INTAKE — original branch constitution; for current status see <capsule/prop>]` for comment headers, or a one-sentence `\emph{(Constitutional intake: …; current status in the Current Status Capsule above.)}` for in-body prose.
- **Never** delete intake language. It is load-bearing for *how the branch was constituted* (Rule 4).

### Rule 2 — Every canon book and branch gets a short Current Status Capsule near the beginning.
- **Location:** immediately after `\maketitle`/`\tableofcontents` and before or at the top of the first Purpose/Front-Block section (anchors identified per file in Phase 4).
- **Length:** ≤ ~12 lines. One posture line, one "as of" provenance line, a pointer list, and (for branches) the branch's line in each of the four frontier accountings *by reference*, never as a new derived number.
- **Form:** a `remark`-like block tagged `[R]` (non-load-bearing by construction — a capsule may never carry proof force), with a stable label `cap:<file>-status`.
- **Uniform template** (Part II).

### Rule 3 — The capsule must point to the authority, not restate it.
The capsule cites the branch's A1 status proposition (and A2 frontier section, A3 closure ledger) by `\ref`, and cites the scaffold snapshot (`NFC_STATE_OF_CANON.md`, `NFC_OBLIGATION_ROSTER.md`) by name. It **does not** re-derive status or counts. This guarantees the capsule cannot itself go stale in a contradictory way: if the pointed-to proposition changes, the capsule still points to the right place.

### Rule 4 — Historical claims are preserved when they explain constitution.
Intake obligations, the "deliberately modest initial endpoint," the UBLT pre-analysis, the "prospective" framing — all remain in the text. They are recontextualized (marked as intake, capsule added), never removed. A reader must always be able to reconstruct how the branch was originally constituted.

### Rule 5 — Stale claims are marked superseded or relocated, never silently deleted.
A claim classified SUPERSEDED in `STALE_LABEL_AUDIT.md` is handled by exactly one of:
- **(a) mark-in-place:** add "(superseded by `\ref{…}`; retained as intake record)" adjacent to it; or
- **(b) relocate:** move it under an explicitly titled "Constitutional Intake (superseded)" subsection in the same file.
Every such action carries a **migration entry** (Part III). Deleting a `\status`-tagged environment is **prohibited without human sign-off** (routes to REVIEW_NEEDED).

### Rule 6 — No status may be strengthened without a transfer/discharge record.
No `[O]`→`[C]`, `[C]`→`[U]`, `[B]`→`[U]`, or posture upgrade (CERT-PROJ→CERT-CLOSE, etc.) may be introduced by this rewrite. This rewrite is **status-preserving**. The capsules *report* the status the canon already asserts (via A1); they never *upgrade* it. If a capsule would state a status stronger than the pointed-to proposition, that is a policy violation and the capsule is wrong, not the proposition.
- Corollary: the Phase-0/1/2 finding that a branch is "further ahead than its front matter suggests" is resolved by **pointing at the already-existing in-body discharge**, not by asserting any new discharge.

### Rule 7 — No branch may claim stronger closure than its declared bridge stack permits.
Capsule and any relabeled text must respect the bridge-stack limit (Authority Model §4). Concretely: SPEC's continuum interfaces are `[B]` → the SPEC capsule says "CERT-CLOSE on the gauge-response regime; continuum interfaces licensed at bridge `[B]` force," never plain "CERT-CLOSE." GR says "domain-bounded … global open," never "CERT-CLOSE." SM says "conditionally intrinsic-structural closed, inherited-scope open," never "closed." The capsule inherits the exact hedges of the A1 proposition.

### Rule 8 — Generated files are never edited by hand.
The 17 `.pdf` files and every future generated artifact (JSON/CSV/dashboard exports, regenerated `.md` count tables) are outputs. They are regenerated from source, never hand-patched. A generated file that disagrees with its source is a regeneration task, never an edit task. (Acceptance criterion 6.)

---

## Part II — The Current Status Capsule: uniform template

Two variants (spine book vs. branch book). Both are `[R]`-tagged, stably labeled, and pointer-based.

**Branch-book capsule template:**
```
%% ============================================================
%% CURRENT STATUS CAPSULE  (added <PhaseX>; non-load-bearing [R])
%% ============================================================
\begin{remark}[\status{R}]\label{cap:<BRANCH>-status}
\textbf{Current Status Capsule.}
\emph{Current posture:} <verbatim posture phrase from the branch's A1 proposition>.
\emph{Authoritative source:} Prop.~\ref{prop:<BRANCH>-status}
(final status), §\ref{sec:<BRANCH>-frontier} (named failure frontier),
§<closure ledger> (per-obligation discharge basis).
\emph{Frontier accountings} (see \texttt{NFC\_OBLIGATION\_ROSTER.md};
never summed): syntactic [O] census — <n or "0 in this branch">;
reduced irreducible frontier — <this branch's item(s) or "none">;
branch posture — <posture>.
\emph{Constitutional intake note:} the Purpose/Seed and front-block
material below records how this branch was \emph{constituted}
(founding question and original obligations); it is intake, not
current status. Most founding obligations are now discharged at the
scope stated in Prop.~\ref{prop:<BRANCH>-status}.
\emph{As of:} <session/date carried from the status proposition, or
"see Canon Ledger for live record">.
\end{remark}
```

**Spine-book capsule template:** same skeleton, but posture is "[U]/[C] stable foundational layer" and the pointers are to the book's own governing theorems and to Book VII's governance rules; no branch-frontier line.

**Hard constraints on every capsule:**
- Tagged `[R]`. Never cited for proof force.
- Contains **no new number** that isn't a `\ref` or a named-file reference.
- Never states a posture stronger than the A1 proposition it points to (Rule 6/7).
- Uses a fresh `cap:` label namespace (no collision with existing labels — verified before insertion).

---

## Part III — Migration entries (the audit trail; acceptance criterion 9)

Every edit that changes visible text carries a migration entry appended to a new scaffold file `MIGRATIONS.md`, with fields:

`ID | date/phase | file | location (label or line) | class (from STALE_LABEL_AUDIT) | before (quoted) | after (quoted) | authority basis (which A-tier text licenses this) | labels touched (must be "none" for canon body, or explicitly listed) | compile result`

- No canon edit may claim to "strengthen" status (Rule 6); the migration `authority basis` must be an **already-existing** A-tier proposition.
- If `labels touched` is non-empty for any theorem/obligation/dependency label, the entry is **blocked** and escalated to REVIEW_NEEDED (protects acceptance criterion 5).

---

## Part IV — Edit-safety rules (protect labels, refs, proofs, compile)

1. **Label immutability.** No `\label{}` key is renamed, removed, or added on any existing theorem/proposition/corollary/lemma/definition/obligation. Capsules introduce only new `cap:` labels. (The one known duplicate-label cleanup candidate — none is required by this rewrite — would be a separate, individually-reviewed task; this rewrite does not touch labels.)
2. **Reference integrity.** After every file edit, re-run the corpus-wide label/ref audit (Phase-0 script). Dangling refs must remain **0**; duplicate-label set must remain the known 12 (no new collisions — in particular, a new `cap:` label must be unique corpus-wide).
3. **Proof force untouched.** No proof body is edited. No hypothesis list is edited. No `\status{}` argument is changed. (This rewrite touches front matter, capsules, section titles, and scaffold — not mathematics.)
4. **Compile gate.** After each file's edits, compile twice with `pdflatex -interaction=nonstopmode -halt-on-error`; exit code must be 0 and page count must not collapse. Real (corpus-global) undefined-reference count must not increase.
5. **Comment-only edits are lowest risk; in-body edits are higher; spine-book in-body edits are highest** (they feed many branches). Risk levels are assigned per file in Phase 4 and dictate ordering in Phase 7.
6. **Section renames** preserve the section's `\label{}` (rename the visible title only, never the label key) so all `\ref`s survive.

---

## Part V — What this policy forbids outright

- Deleting any `\status`-tagged environment. (REVIEW_NEEDED.)
- Changing any `\status{}` value. (Status-preserving rewrite.)
- Renaming/removing/adding theorem or obligation labels. (Criterion 5.)
- Mass-renaming the `openobligation` environment (F-5). (REVIEW_NEEDED; separate approved pass only.)
- Editing any `.pdf` or other generated artifact. (Rule 8.)
- Resolving a same-tier in-canon contradiction (F-6, D-3, B-1 mechanism) by mechanical choice. (REVIEW_NEEDED.)
- Introducing any new derived count into canon. (Capsules point; they don't compute.)
- "Cleaning up" an uncertain item by guessing. (Mark AMBIGUOUS/REVIEW_NEEDED.)
