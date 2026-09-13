<div align="center">

# SALMS
### A moving window of clarity.

A Fusion generator for DaVinci Resolve: sharp rectangular windows over blurred, grainy footage.

[![Validate](https://github.com/okonovs/salms/actions/workflows/validate.yml/badge.svg)](https://github.com/okonovs/salms/actions/workflows/validate.yml)

**Edit-page controls · Deterministic motion · No external media**

</div>

---

## One layer. A changing perspective.

Place **Salms Random Window** above your footage, stretch it over a section, and control it from the Edit Inspector. The generator reads the composited tracks beneath it. One master rectangle drives both the sharp window and its outline.

| Image | Rectangle | Border |
| --- | --- | --- |
| Blur amount | Change interval and seed | Width |
| Film grain amount | Minimum / maximum area | Color |
| Grayscale | Minimum / maximum shape ratio | Opacity |

## Area defines size. Ratio defines shape.

**Area** is the percentage of the whole frame occupied by the sharp window. **Shape ratio** is its visible width divided by height: `0.25` is tall, `1` is square, and `4` is wide. The default range spans tall and wide shapes equally in logarithmic space, independently of the timeline's orientation.

Area and shape are sampled separately. Frame dimensions convert the sampled shape into Fusion's normalized coordinates. Each result holds for four frames by default, then jumps without interpolation. If a shape cannot fit at the chosen area, its ratio is restricted to preserve the area and a 1% edge margin. Square pixels are currently assumed.

## Build and install

Requires Python 3 and DaVinci Resolve with Fusion.

```sh
python3 -m unittest discover -s tests -v
python3 scripts/build_release.py
```

Double-click **`dist/Salms Random Window.drfx`**, confirm installation, then search **Effects → Generators → Salms Random Window** on the Edit page. Put it on V2 above your footage and select it to access the Generator Inspector.

[Installation and upgrade guide](docs/installation.md) · [Changes](CHANGELOG.md) · [Development instructions](AGENTS.md)

## Project map

```text
src/                 Base Fusion graph
scripts/             Prototype and installer builders
tests/               Geometry contract tests
docs/                Installation and archived prototypes
.github/workflows/   Build validation and installer artifacts
```

The build has no third-party Python dependencies. Installers, footage, caches, credentials, and Resolve backups are excluded from version control. GitHub Actions builds an installer artifact for each validated push; it is not automatically a tested release.

## Validation status

The original prototype was tested by the user. Version 0.2 corrects grayscale wiring and introduces area-driven geometry; its numerical and archive checks pass locally. **The updated installer still needs visual verification in Resolve**, including the new image-dimension expressions and Inspector controls. Reinstall and add a fresh generator instance to test it.

Built using [Fusion's timeline background input](https://documents.blackmagicdesign.com/UserManuals/Fusion19_Manual.pdf). No footage is embedded in the generator.
