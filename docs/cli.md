# CLI Reference — phaethon

## `phaethon run`

Run a full Phaethon-Chimera simulation cycle.

```
Usage: phaethon run [OPTIONS]

Options:
  -n, --n-orbits INTEGER         Number of orbits to simulate [default: 10]
  --destiny-predictions          Print all 47 DESTINY+ predictions after run
  --json                         Output results as JSON (machine-readable)
```

**Examples**

```bash
# Standard run
phaethon run --n-orbits 10

# With all 47 predictions printed
phaethon run --n-orbits 10 --destiny-predictions

# Machine-readable JSON output
phaethon run --json
```

---

## `phaethon chimera-state`

Detect and report the chimera state from a simulation.

```
Usage: phaethon chimera-state [OPTIONS]

Options:
  --n-orbits INTEGER   Number of orbits [default: 10]
  --threshold FLOAT    R threshold for chimera classification [default: 0.5]
```

```bash
phaethon chimera-state
# → Order parameter R = 0.4823  → chimera
```

---

## `phaethon destiny-report`

Print all 47 DESTINY+ mission predictions.

```
Usage: phaethon destiny-report [OPTIONS]

Options:
  --format TEXT   Output format: table | json  [default: table]
```

```bash
phaethon destiny-report
phaethon destiny-report --format json
```
