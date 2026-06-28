---
name: research-power
description: Use when planning sample size, minimum detectable effect, power curves, dropout-adjusted enrollment, or grant/protocol sample-size justification for scientific studies.
---

# Research Power

Use this skill before data collection or when explaining what an existing sample can detect.

## Workflow

Run a two-group planning curve:

```bash
python skills/research-power/scripts/research_power.py \
  --test t_ind --effect-size 0.5 --power 0.8 --alpha 0.05 \
  --out-dir outputs/power
```

## Outputs

| File | Purpose |
| --- | --- |
| `power_report.md` | Sample-size/MDE summary |
| `power_curve.csv` | Power by n |
| `power_curve.png` | Planning figure |

## Rules

- Use a defensible effect size. Prefer SESOI or prior/pilot evidence.
- Report a range or curve when the effect size is uncertain.
- Treat post-hoc observed power as a warning sign; use MDE/sensitivity instead.

