# Free Matching / Supplementary Information Alignment

This branch combines the supplied screenshot-reproduction free matching
configuration with the existing GitHub paper-figure framework. It does not
overwrite main, read a main manuscript, or publish a supplementary document.

## Retained Framework

Inputs, response extraction, observed reference-support selection, geometry and
topology definitions, independent candidate ranking, evidence-only binary
output, presentation reconstruction, figure panel order and reproduction entry
points are unchanged. Human-review flags and thresholds remain absent.

## Necessary Changes

- Calibration measures the black bar, not its white label panel.
- Registration uses no physical prior (weight zero), a generic seven-point
  coarse scale grid 0.70--1.60 and +/-14% local scale refinement, matching the
  archived free-search configuration.
- Native affine export uses each image's own analysis dimensions.
- Axial subpixel directions use double-angle interpolation.
- All figures derive scores and transforms from the same current PipelineRun.
- The scale-sensitivity diagnostic varies the generic grid upper bound, not a
  physical residual bound. Seven points remain, so grid spacing also changes.

## SI Changes

Revise only matching-related method descriptions, calibration roles, search
parameters, result values, component/sensitivity tables, provenance links and
their corresponding embedded figures. Preserve other text, equations, table
formatting, figure placement and package entries. Color inserted/replaced text
red against the user's original SI; remove obsolete human-review content.
Deliver the revised SI locally, not in this public repository.

## Evidence Boundaries

The 4x4 matrix contains internal matching scores, not confusion counts or
probabilities. F = 0.72G + 0.28T; geometry is optimized first and topology is
evaluated at that transform. Corridor R/Q/D are foreground retention, corridor
density and spatial overlap. Four examples and sensitivity reruns do not
establish recognition or segmentation accuracy. Physical normalization of
reference panels is display-only and never fed back into free registration.
