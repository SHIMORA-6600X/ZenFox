# Benchmarks — ZenFox v157

> No published numbers yet. This file defines the method so claims stay honest.
> Do not claim "fastest" without filling the table below.

## Method
- Profiles: clean Firefox profile vs ZenFox v157 Balanced (`user.js` + `LiteFox.js` + `Softfox.js` ZEN).
- Support range: Firefox 128 ESR + latest Stable.
- Machines: record OS, CPU/GPU, RAM, disk (SSD/HDD), display Hz, connection.
- Runs: 3 cold starts + 3 warm runs per test, report median.
- Tools: `about:profiling`, Speedometer 3.x, cold-start stopwatch, YouTube 4K60 drop-frame count (`about:support > Media`).

## Table (fill per release)

| Machine | Firefox | Stock cold (s) | ZenFox cold (s) | Speedometer stock | Speedometer ZenFox | YT 4K dropped | Notes |
|---------|---------|----------------|-----------------|-------------------|--------------------|---------------|-------|
| e.g. Win11/R5/16GB/SSD/120Hz | 142 Stable | — | — | — | — | — | — |
| e.g. Fedora/KDE/i5/8GB/SSD/60Hz | 128 ESR | — | — | — | — | — | — |

## Rules
- Aggressive `Max opt-in` values (see `user.js` comments) must be benchmarked separately — never ship as default without numbers.
- If a tweak shows <2% gain or regresses cold start, revert to default and note in `CHANGELOG.md`.
