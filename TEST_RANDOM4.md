# Random rectangle + grain prototype

Phase1.setting is user-confirmed working and is preserved.
Random4_Grain.setting adds a four-frame rectangle hold and native Fusion FilmGrain after Blur, before the sharp-original Merge. The outline still inherits the master rectangle's geometry.

## Test

Duplicate your working Fusion Composition on the Edit timeline as a backup. In the test copy, open Fusion, select all existing graph nodes and delete them, then paste the entire contents of Random4_Grain.setting. Do not paste alongside the original graph: duplicate names could break expression links.

Select MediaOut1 and press 2. Step frame-by-frame: relative frames 0–3 must match, frame 4 must jump, frames 4–7 must match, frame 8 must jump. Return to Edit and play.

Select SalmsFilmGrain to adjust its native grain parameters. Settings > Blend starts at 0.5; lower it for subtler grain. Grain affects only the exterior because the sharp interior is composited from the original afterwards.

Rectangle defaults: widths 18–58%, heights 18–62%, minimum edge margin 1%. Shape changes mean wider/taller rectangles, not different geometric shapes. Seed 17 and four-frame cadence are fixed in the expressions for this prototype. Frames are relative to comp.RenderStart. No smoothing, random modifier, macro, installed template or custom Edit Inspector controls.

Python math checks pass for 10000 frames. Actual Fusion expression evaluation and FilmGrain rendering still require testing in Resolve. No Resolve automation was attempted in this update because the previous session returned an API error.
