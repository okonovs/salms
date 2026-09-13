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

## Inspector control guide

Select the generator on the **Edit page** and open the **Generator Inspector**.

| Control | Default | What it does |
| --- | --- | --- |
| **Blur Amount** | 12 | Softens only the exterior. `0` disables blur; larger values increase softness. Range: 0–100 in Fusion blur units, not a percentage. |
| **Film Grain Amount** | 0.5 | Blends grain into the exterior. `0` removes added grain; `1` applies the grain node's full result. Does not change grain size. |
| **Grayscale** | Off | Makes only the blurred/grainy exterior monochrome. The sharp rectangle keeps the original footage color; the border keeps its chosen color. |
| **Change Every Frames** | 4 | Holds one rectangle for this many frames, then jumps to another. `4`: frames 0–3 hold, frame 4 jumps. `12` gives slower changes. Range: 1–240 frames. |
| **Random Seed** | 17 | Chooses another repeatable sequence of positions, areas and shapes. Same seed and settings reproduce the same sequence. Range: 0–100000. |
| **Minimum Area (%)** | 4 | Smallest sampled window area as a percentage of the entire image. `4` means 4% of all frame pixels, not 4% of either side. Range: 0.1–90%. |
| **Maximum Area (%)** | 18 | Largest sampled window area. Set both area limits equal for constant area while position and shape still change. Range: 0.1–90%. |
| **Minimum Shape Ratio (W/H)** | 0.25 | Lower limit of visible width divided by height. `0.25` is four times taller than wide; `1` is square. Range: 0.1–10. |
| **Maximum Shape Ratio (W/H)** | 4 | Upper shape limit. `4` is four times wider than tall. Keep the minimum below `1` and maximum above `1` to allow both orientations. Range: 0.1–10. |
| **Border Width** | 0.003 | Outline thickness in Fusion's normalized mask units. Smaller values make a finer line; larger values make a thicker line. Use Border Opacity to hide it. |
| **Border Color** | White | Sets the outline's RGB color. If individual channel controls appear, Red, Green and Blue each set that color component. Grayscale does not change it. |
| **Border Opacity** | 1 | Outline visibility: `0` is invisible, `0.5` is translucent and `1` is fully opaque. |

Reversed area or shape limits are sorted internally. Very large areas restrict the shapes that fit inside the frame; use smaller areas for more extreme tall and wide windows. All size examples assume square pixels.

## Area defines size. Ratio defines shape.

**Area** is the percentage of the whole frame occupied by the sharp window. **Shape ratio** is its visible width divided by height: `0.25` is tall, `1` is square, and `4` is wide. The default range spans tall and wide shapes equally in logarithmic space, independently of the timeline's orientation.

Area and shape are sampled separately. Frame dimensions convert the sampled shape into Fusion's normalized coordinates. Each result holds for four frames by default, then jumps without interpolation. If a shape cannot fit at the chosen area, its ratio is restricted to preserve the area and a 1% edge margin. Square pixels are currently assumed.

## Download

Get the installable **Salms Random Window.drfx** from [GitHub Releases](https://github.com/okonovs/salms/releases). Double-click it to install. No Python or source build is needed for the downloaded installer.

The default sequence generates **both tall/narrow and wide/horizontal windows**, not one orientation per timeline. Keep the shape range at **0.25–4** to allow both. Shapes are sampled randomly, so they need not alternate at each jump.

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

The original prototype was tested by the user. Version 0.2.1 limits grayscale to the exterior and retains area-driven geometry; its numerical and archive checks pass locally. **The updated installer still needs visual verification in Resolve**, including the new image-dimension expressions and Inspector controls. Reinstall and add a fresh generator instance to test it.

Built using [Fusion's timeline background input](https://documents.blackmagicdesign.com/UserManuals/Fusion19_Manual.pdf). No footage is embedded in the generator.
