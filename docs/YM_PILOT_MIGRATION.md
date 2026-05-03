# YM Pilot Migration

v12 migrates the Yang--Mills branch from a minimal representative sample into a
more live-shaped governance packet.

## Purpose

The YM pilot is designed to stress a different governance pattern from GR:

- conditional closure rather than domain-bounded closure;
- post-program obligations rather than a single global extension frontier;
- B1/B2/B3 bridge structure;
- a surviving B3-A2 residual frontier;
- explicit prevention of an unconditional Clay-grade upgrade.

## Expected computation

The local packet should compute:

```text
status:YM = conditional-cert-close
```

with:

```text
ob:YM.B3.A2 = O
```

The branch posture is successful only if the system represents conditional endpoint
closure without promoting YM to unconditional `cert-close`.

## Migrated records

The v12 packet includes:

- `ob:YM.O-ID`, `thm:YM.ID`
- `ob:YM.O-RIG`, `thm:YM.RIG`
- `ob:YM.O-ENC`, `thm:YM.ENC`
- `ob:YM.O-GLOB`, `thm:YM.GLOB`
- `ob:YM.O-CLU`, `thm:YM.CLU`
- `thm:YM.7`
- `ob:YM.B1`, `thm:YM.B1.bridge`
- `ob:YM.B2`, `thm:YM.B2.bridge`
- `ob:YM.B3`, `thm:YM.B3.bridge`
- `ob:YM.B3.A2`
- `status:YM`

## Governance rule

The YM inference rule requires:

```text
thm:YM.7 in {C,U}
thm:YM.B1.bridge in {C,U}
thm:YM.B2.bridge in {C,U}
thm:YM.B3.bridge in {C,U}
ob:YM.B3.A2 == O
```

Then:

```text
status:YM = conditional-cert-close
```
