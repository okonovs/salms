# salms — Random Window for DaVinci Resolve

A reusable Fusion generator that reads the composited video tracks underneath it, blurs and grains the image, and reveals a sharp rectangular window with a matching border. The window jumps to a deterministic random position and size at a configurable frame interval.

## Features

- Timeline background input; no source media imported into the graph.
- Blur and film grain on the exterior, with a sharp interior.
- One master rectangle drives the window and border.
- Discrete random changes, defaulting to every four frames.
- Edit Inspector controls for blur, grain, grayscale, interval, seed, minimum/maximum width and height, border width, color and opacity.
- White border by default. Grayscale affects the footage while preserving the chosen border color.

## Build

Python 3 with the standard library is sufficient. From this repository:

```sh
python3 build_random_grain.py
python3 build_plugin.py
```

The installer is generated at `dist/Salms Random Window.drfx`. Build scripts also write local validation reports under `tests/`. Generated packages, reports, media and Resolve project backups are deliberately excluded from Git.

## Install and use

Double-click the generated `.drfx` file and confirm installation in Resolve. In the Edit page Effects Library, search Generators for **Salms Random Window**. Place it on V2 above footage on V1, stretch it to the desired duration, then select it to adjust the Generator Inspector. See [installation and manual checks](docs/INSTALL.txt).

## Source layout

- `Phase1.setting`: user-confirmed basic blur/window/border graph.
- `Random4_Grain.setting`: pasteable random-window and grain prototype.
- `build_random_grain.py`: regenerates the prototype and checks timing/bounds.
- `build_plugin.py`: builds the macro and standard `Edit/Generators/Salms` installer archive; checks archive integrity and internal references.
- `TEST_RANDOM4.md`: prototype manual verification steps.
- `AGENTS.md`: instructions for future development sessions.

## Validation status

The base graph and random/grain prototype received positive user feedback. The packaged generator has passed local structural checks; installation, Inspector behavior and rendered output still need explicit verification in Resolve. Local Python checks do not prove Fusion expression evaluation or rendering correctness.

The graph uses `MediaIn` with `MediaSource = Background`. See the [Blackmagic Fusion reference manual](https://documents.blackmagicdesign.com/UserManuals/Fusion19_Manual.pdf). This is a Fusion template, not a compiled OFX or Codex plugin.

## Development

Keep development incremental and preserve the known-working graphs. Resolve automation previously returned an error; no further mutations should be attempted without resolving that issue. Prefer locally generated settings and manual validation when automation is unreliable. Commit meaningful working milestones with accurate validation notes; never commit credentials, footage or project backups.
