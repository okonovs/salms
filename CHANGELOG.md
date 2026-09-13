# Changelog

## 0.2.1 — 2026-09-13

- Apply grayscale only to the processed exterior, preserving original color in the sharp window.
- Document every Inspector control, its default and practical use in the README.
- Local checks pass; updated Resolve rendering validation remains pending.

## 0.2.0 — 2026-09-13

- Replace invalid grayscale input wiring with BrightnessContrast's native Saturation input.
- Replace width/height percentage controls with frame-area limits and independent visual shape-ratio limits.
- Correct shape dimensions for landscape and portrait frame sizes; preserve area when restricting shapes to fit.
- Organize source, scripts, tests and documentation; add GitHub build validation and installer artifacts.
- Rendering validation pending; use a fresh generator instance after reinstalling.

## 0.1.0 — 2026-09-10

- Initial private repository with a packaged random-window Fusion generator and Edit controls.
