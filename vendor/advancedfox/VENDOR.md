# Vendored AdvancedFox — provenance

Do NOT hand-edit files in this directory. To update: download the upstream
release below, re-run the mapping, update this file.

- **Upstream:** https://gitlab.com/iahmed_7024-group/advancedfox
- **Release:** `AdvancedFox_1.0.0-release` (unified version 1.0.0, latest stable at vendor time)
- **Released:** 2026-09-23
- **Source zip:** https://gitlab.com/iahmed_7024-group/advancedfox/-/archive/AdvancedFox_1.0.0-release/advancedfox-AdvancedFox_1.0.0-release.zip
- **Zip SHA256:** `af2c4fe4a0bb87a6ea71e72673d856a16b87d1c3e268012fa2be09538e0c8d3f`
- **Upstream license:** MIT (shipped in upstream `LICENSE`; our project is MIT too)
- **Vendored on:** 2026-09-25

## Mapping (upstream path → local name)

| Local file | Upstream path inside release |
|---|---|
| `linux-weak.js` | `Privacy & Security/Firefox ESR 140/user.js/Linux/Weak/AdvancedFox_priv_weak-release.js` |
| `linux-medium.js` | `…/Linux/Medium/AdvancedFox_priv_medium-release.js` |
| `linux-strong.js` | `…/Linux/Strong/AdvancedFox_priv_strong-release.js` |
| `windows-weak.js` | `…/Windows/Medium…` (same pattern, Windows tree) |
| `windows-medium.js` | `…/Windows/Medium/AdvancedFox_priv_medium-release.js` |
| `windows-strong.js` | `…/Windows/Strong/AdvancedFox_priv_strong-release.js` |
| `policies-{weak,medium,strong}.json` | `Privacy & Security/Firefox ESR 140/policies/{Weak,Medium,Strong}/policies.json` |

Installer default: per-OS **medium** level (`--adv-level weak|medium|strong` to change).
macOS has no upstream variant — Linux variant is used (documented in the picker).

## Deliberately excluded

- `DMT/user.js/DMT-testing.js`, `Disable AI Features/user.js/DAIF-testing.js` — testing files, not releases
- `Performance/Softfox.js`, `Performance/155`, `ESR/*` — empty/stub dirs; we ship our own `Softfox.js`
- `images/`, upstream `README.md`s — docs/assets, not installable config
