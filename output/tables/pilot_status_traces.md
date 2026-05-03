# Pilot Status Traces

## GR

### `status:GR`
- **Effective:** `domain-bounded-cert-close`
- **Source:** `branch-packet-inference`
- **Basis:** `thm:GR.domain`, `ob:GR.global-subcriticality`
- **Trace:**
  - Matched branch-packet inference rule.
  - Basis item(s): thm:GR.domain, ob:GR.global-subcriticality.
  - Computed branch posture: domain-bounded-cert-close.
  - Local GR pilot packet supports domain-bounded closure while global curvature-subcriticality / BF-9 remains open.
- **Reason:** Local GR pilot packet supports domain-bounded closure while global curvature-subcriticality / BF-9 remains open.

### `thm:GR.domain`
- **Effective:** `C`
- **Source:** `declared`
- **Basis:** _none_
- **Trace:**
  - Declared status/posture used as the initial effective value.
- **Reason:** No stronger inference applied.

### `ob:GR.global-subcriticality`
- **Effective:** `O`
- **Source:** `declared`
- **Basis:** _none_
- **Trace:**
  - Declared status/posture used as the initial effective value.
- **Reason:** No stronger inference applied.

### `ob:GR.EFE1`
- **Effective:** `C`
- **Source:** `local-discharge-inference`
- **Basis:** `thm:GR.compat`
- **Trace:**
  - Located explicit closing discharge edge(s).
  - Accepted discharge kinds: full, scoped, superseding.
  - Basis claim(s): thm:GR.compat.
  - Inferred obligation status: C.
- **Reason:** Locally inferred from explicit closing discharge edges by thm:GR.compat.

### `ob:GR.EFE2`
- **Effective:** `C`
- **Source:** `local-discharge-inference`
- **Basis:** `thm:GR.compat`
- **Trace:**
  - Located explicit closing discharge edge(s).
  - Accepted discharge kinds: full, scoped, superseding.
  - Basis claim(s): thm:GR.compat.
  - Inferred obligation status: C.
- **Reason:** Locally inferred from explicit closing discharge edges by thm:GR.compat.

### `ob:GR.EFE3`
- **Effective:** `C`
- **Source:** `local-discharge-inference`
- **Basis:** `thm:GR.compat`
- **Trace:**
  - Located explicit closing discharge edge(s).
  - Accepted discharge kinds: full, scoped, superseding.
  - Basis claim(s): thm:GR.compat.
  - Inferred obligation status: C.
- **Reason:** Locally inferred from explicit closing discharge edges by thm:GR.compat.

## YM

### `status:YM`
- **Effective:** `conditional-cert-close`
- **Source:** `branch-packet-inference`
- **Basis:** `thm:YM.7`, `thm:YM.B1.bridge`, `thm:YM.B2.bridge`, `thm:YM.B3.bridge`, `ob:YM.B3.A2`
- **Trace:**
  - Matched branch-packet inference rule.
  - Basis item(s): thm:YM.7, thm:YM.B1.bridge, thm:YM.B2.bridge, thm:YM.B3.bridge, ob:YM.B3.A2.
  - Computed branch posture: conditional-cert-close.
  - Local YM pilot packet supports conditional closure through B1/B2/B3 bridge packets while B3-A2 remains the surviving residual frontier.
- **Reason:** Local YM pilot packet supports conditional closure through B1/B2/B3 bridge packets while B3-A2 remains the surviving residual frontier.

### `thm:YM.7`
- **Effective:** `C`
- **Source:** `declared`
- **Basis:** _none_
- **Trace:**
  - Declared status/posture used as the initial effective value.
- **Reason:** No stronger inference applied.

### `thm:YM.B1.bridge`
- **Effective:** `C`
- **Source:** `declared`
- **Basis:** _none_
- **Trace:**
  - Declared status/posture used as the initial effective value.
- **Reason:** No stronger inference applied.

### `thm:YM.B2.bridge`
- **Effective:** `C`
- **Source:** `declared`
- **Basis:** _none_
- **Trace:**
  - Declared status/posture used as the initial effective value.
- **Reason:** No stronger inference applied.

### `thm:YM.B3.bridge`
- **Effective:** `C`
- **Source:** `declared`
- **Basis:** _none_
- **Trace:**
  - Declared status/posture used as the initial effective value.
- **Reason:** No stronger inference applied.

### `ob:YM.B3.A2`
- **Effective:** `O`
- **Source:** `declared`
- **Basis:** _none_
- **Trace:**
  - Declared status/posture used as the initial effective value.
- **Reason:** No stronger inference applied.
