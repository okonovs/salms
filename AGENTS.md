# Working on salms

## Scope and architecture
- This directory is the project and Git repository root. Keep all project files, scratch work and backups here.
- Build a DaVinci Resolve Fusion generator usable above footage from the Edit page Inspector.
- Read lower timeline tracks using MediaIn MediaSource=Background. Never copy/import source footage into the composition.
- One master rectangle controls center, width and height; the outline inherits all three.
- Randomization must be deterministic and held for discrete frame intervals, without smoothing or shaking. Respect size bounds and image containment.
- Keep the original and blurred/grained branches distinct. Grayscale affects only the processed exterior after grain. The sharp interior retains the original color, and border color remains independent.

## Safety and workflow
- Preserve user edits and known-working prototypes. Do not assume the active Resolve composition is the intended target.
- Previous automation returned an error while setting MediaSource/adding Blur. Treat execution state as uncertain; do not resume mutations blindly.
- For any future authorized automation, use small explicit tool operations and identify project, timeline, item and composition. Verify state between important operations.
- On API errors or Bad Request, stop mutations rather than retry. Reacquire references after state changes. Work locally on settings/scripts instead.
- Never send giant serialized graphs through generic Resolve API calls.
- Keep graph design, API transport failures and template packaging bugs separate.

## Build and validation
- Python standard library only: run `python3 scripts/build_prototype.py` and `python3 scripts/build_release.py`.
- `scripts/build_release.py` consumes src/random-window-base.setting. If prototype behavior changes, update its builder too; avoid generated-source drift.
- Keep installation instructions in docs/installation.md; dist is disposable build output.
- Local checks cover math, connections and archive structure, not Resolve rendering. Never claim a packaged change works without rendered/manual evidence.
- Verify Inspector controls, grayscale, four-frame holds, border geometry, independent instances, lower-track input and stretched duration in Resolve before declaring a release validated.

## Git and secrets
- User explicitly requests commits at meaningful working milestones. Review the diff, run appropriate checks, and commit coherent verified changes with descriptive messages.
- Do not claim a commit/push succeeded until checked. Do not force-push or rewrite existing history without authorization.
- The user explicitly authorized making this repository public on 2026-09-13. Keep credentials, footage and local backups excluded. Publish installable .drfx files as GitHub Release assets, not tracked build output.
- Before staging, check for secrets and unintended files. Never commit .env files, credentials, keys, user media, Resolve backups, generated installers, caches or reports.
- Use work/ for temporary tools and files; backups/ for local safety copies; dist/ for generated deliverables. These are ignored.
- Record remaining limitations honestly in documentation and milestone messages.

## Geometry and regression checks
- Run `python3 -m unittest discover -s tests -v` before committing geometry changes.
- Area is a fraction of frame area; visual shape ratio is corrected for frame dimensions (square pixels currently assumed). Preserve sampled area by constraining infeasible ratios.
- Grayscale uses BrightnessContrast.Saturation; do not restore the invalid MasterRGBSaturation input.

## Authorized demonstration asset
- The user explicitly authorized publishing salms-preview.mov on 2026-09-13. docs/assets/demo.gif is its README derivative; the original belongs in Release assets. This exception does not authorize publishing other footage.
