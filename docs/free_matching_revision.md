# Free Matching / Supplementary Information Alignment

This revision combines the supplied screenshot-reproduction free matching
configuration with the existing GitHub paper-figure framework. It was developed
on `free-matching-si-20261004` and merged into `main` at the user's request.
No main manuscript was read and no supplementary document is published here.

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

## Method Alignment

The matching-related method descriptions, scale roles, search parameters and
versioned results use the active free-search convention G = G0, w = 0.
Manuscript editing instructions are not part of the scientific implementation.

Method references 34--39 remain applicable; their DOI records were verified.
References 40 (scikit-image) and 41 (SciPy) identify the actual implementation
libraries. Earlier SI reference numbers remain unchanged. The code/citation
mapping and evidence limits are in `matching_references.md`.

## Evidence Boundaries

The 4x4 matrix contains internal matching scores, not confusion counts or
probabilities. F = 0.72G + 0.28T; geometry is optimized first and topology is
evaluated at that transform. Corridor R/Q/D are foreground retention, corridor
density and spatial overlap. Four examples and sensitivity reruns do not
establish recognition or segmentation accuracy. Physical normalization of
reference panels is display-only and never fed back into free registration.
