# Install and test

1. Run `python3 scripts/build_release.py` from the repository root.
2. Double-click `dist/Salms Random Window.drfx` and confirm installation/replacement.
3. Save and restart Resolve if its Effects Library has not refreshed.
4. Add a **new** Salms Random Window generator above footage. Existing timeline instances can retain the previous embedded graph; reinstalling does not reliably migrate them.
5. Select the generator on Edit and adjust the Generator Inspector.

## Version 0.2 controls

- Blur: 12 by default. Grain blend: 0.5. Grayscale: off.
- Interval: 4 frames. Seed: 17.
- Area: 4–18% of the frame. Reversed min/max bounds are sorted.
- Shape ratio: 0.25–4, measured as visible width/height for square-pixel footage. Equal limits give a fixed shape when it fits.
- Border: white, opaque, normalized width 0.003.

For pronounced tall/wide windows, use smaller areas and a broad shape range. Large areas necessarily restrict available ratios. Thick borders may exceed the 1% window margin.

## Acceptance checks

- Verify source footage appears from lower tracks; move the generator over another shot.
- Toggle grayscale on saturated footage. Both window and exterior must lose color, while a colored border stays colored.
- At a fixed small area, set both ratio limits to 1: the window should be square on 16:9 and 9:16 timelines. Try 0.25 and 4 for tall/wide shapes.
- Set equal area limits and vary ratio: the occupied area should stay constant.
- Step frames 0–3, 4–7, 8–11: hold within each block, jump at boundaries.
- Verify all Inspector controls, stretched duration, border alignment, and two independent instances.

These are manual rendering checks; Python tests do not validate Fusion itself. Previous Resolve API errors mean automated mutations remain paused.
