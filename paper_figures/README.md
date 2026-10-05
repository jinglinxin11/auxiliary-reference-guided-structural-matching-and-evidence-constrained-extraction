# End-to-end reproduction of the manuscript figures

This reviewer workflow starts from the four target microscopy images and four
reference images committed under `data/input/`. It runs all sixteen candidate
registrations once, writes the numerical diagnostic source data, and generates
Figure H plus Supplementary Figures 1–5 from that same in-memory result.

No manuscript score, transform, translation landscape, or sensitivity curve is
loaded from a frozen figure or hard-coded plotting array.

## One command

From the repository root:

```powershell
python paper_figures/run_all.py
```

For the committed manuscript inputs, the same assumptions can be stated
explicitly:

```powershell
python paper_figures/run_all.py --target-scale-bar-um 200 --reference-scale-bar-um 500
```

The same command is used from Bash, zsh, or a POSIX shell:

```bash
python paper_figures/run_all.py
```

The launcher creates a disposable virtual environment in the operating
system's temporary directory, installs the pinned root requirements, safely
clears only its `algorithm_results/`, `diagnostics/`, `figure_h/` and
`supplementary/` children under `paper_figures/generated/`, runs the algorithm
and all matching plots, and
removes the temporary environment automatically.
It preserves directories not owned by the matching workflow.

Custom input directories can be supplied without changing the code:

```powershell
python paper_figures/run_all.py `
  --targets path\to\four_targets `
  --references path\to\four_references
```

Each directory must contain exactly four readable JPG or PNG images. Target
images are ordered by filename; reference filename stems are used only as
display labels. Candidate selection is determined by the algorithm scores.

## Physical-scale contract

- Target inputs carry validated native 200 µm scale bars.
- Reference inputs carry validated native 500 µm scale bars.
- Native calibrations are reporting/display metadata only. They do not enter
  free registration, search bounds or ranking; treating the reference bar as
  200 µm is still incorrect when reporting physical measurements.
- Every manuscript microscopy output is expressed at target-referenced
  sampling. Supplementary Figure 4 therefore removes the detected native
  reference annotation, isotropically resamples the full reference field from
  its 500 µm calibration to the representative target analysis sampling, and
  places every candidate on one common physical canvas using background-only
  padding before adding a 200 µm display bar. The source pixels under
  `data/input/` are never overwritten. The conversion uses no specimen crop
  or content-dependent zoom.
- `generated/diagnostics/diagnostics.json` records the native assumptions,
  detected pixels per micrometre, calibration confidence, display sampling,
  input hashes, and the text definition of this conversion.

## End-to-end data flow

The corrected calibration uses a white label panel only to locate its black
horizontal bar; label-panel width is not a calibration measurement. Diagnostics
record both the bar and annotation bounds. The corrected native transform uses
each image's own analysis dimensions, and subpixel axial directions use
double-angle interpolation. These changes do not introduce human-review logic.

```text
data/input/target_images + data/input/reference_images
                         |
                         v
        four targets x four candidate registrations
                         |
                         v
      one PipelineRun containing all scores and transforms
                         |
          +--------------+------------------+
          |              |                  |
          v              v                  v
 algorithm_results/  diagnostics/      paper figures
```

Figure H uses the reproducible worked example `target_01 -> S`, matching the
approved post-revision panel sequence. Supplementary Figure 1 reports all four
targets, so no target is omitted from the processing evidence.

## Outputs

### Current manuscript numbering

The filenames below retain internal workflow numbering, not the final merged
Supplementary Information numbering. Do not infer the paper figure number from
an internal filename suffix.

| Current manuscript figure | Internal output |
| --- | --- |
| Fig. 10a-e | `supplementary/individual_panels/suppfig1_target_01_a` through `e` |
| Fig. 11 | `figure_h/panel_c_pairwise_internal_score_matrix.png` |
| Fig. 18 | `supplementary/supplementary_figure_4_candidate_references.png` |
| Fig. 19 | `supplementary/supplementary_figure_1_casewise_evidence_flow.png` |
| Fig. 20 | `supplementary/supplementary_figure_2_pairwise_ranking_transforms.png` |
| Fig. 21 | `supplementary/supplementary_figure_5_candidate_comparison_robustness.png` |
| Fig. 22 | `supplementary/supplementary_figure_3_registration_output_sensitivity.png` |

Paths are relative to `paper_figures/generated/`. Exact filenames and final-number
export names are provided in the [machine-readable map](../manuscript_figure_map.json).
Original image bytes, scientific arrays, and internal panel names are unchanged.
The separate legacy six-ROI `figure_s14/` archive is not manuscript Fig. 14.

```text
paper_figures/generated/
  algorithm_results/
    results.json                      # selected labels and transforms
    presentation/                     # four target-derived presentation PNGs
    binary/                           # four strict matched-only PNGs

  diagnostics/
    pairwise_matches.csv              # all 16 scores, transforms, and components
    selected_matches.csv              # four selected/runner-up summaries
    translation_landscape.csv         # plotted local objective grid
    corridor_radius_sensitivity.csv   # plotted precision/recall/Dice values
    search_bound_sensitivity.csv      # independent reruns over diagnostic bounds
    diagnostics.json                  # input SHA-256 values and plot definitions

  figure_h/                           # 8 standalone 600 dpi RGB PNG panels
    panel_a_structural_response.png
    panel_b_foreground_skeleton.png
    panel_c_pairwise_internal_score_matrix.png
    panel_d_local_translation_landscape.png
    panel_e_registered_support_corridor.png
    panel_f_corridor_radius_sensitivity.png
    panel_g_strict_matched_only_output.png
    panel_h_target_derived_presentation.png

  supplementary/                     # 5 complete supplementary PNG figures
    supplementary_figure_1_casewise_evidence_flow.png
    supplementary_figure_2_pairwise_ranking_transforms.png
    supplementary_figure_3_registration_output_sensitivity.png
    supplementary_figure_4_candidate_references.png
    supplementary_figure_5_candidate_comparison_robustness.png
    individual_panels/                # 42 standalone 600 dpi RGB PNG panels
```

These are the approved post-revision layouts: Figure H contains the score
matrix, local translation contour and corridor-radius sensitivity panels;
Supplementary Figures 2, 3 and 5 use aligned parenthesized panel labels and the
requested spacing. The supplementary single-panel counts are:

- Supplementary Figure 1: 20 panels, five data-derived stages for four targets.
- Supplementary Figure 2: 3 panels, pairwise scores, ranking margins, and transforms.
- Supplementary Figure 3: 3 panels, translation objective and corridor-radius sensitivity.
- Supplementary Figure 4: 8 panels, target-referenced 200 µm image and analysis views of all four references.
- Supplementary Figure 5: 8 panels, selected/runner-up components, robustness and topology metrics.

## Quantitative definitions

- Figure H-c is read directly from the sixteen final `UnifiedMatch.score`
  values produced in the current run.
- Figure H-d fixes the selected scale and rotation, then evaluates the same
  registration geometry objective over a 41 x 41 grid of relative x/y
  translations from -24 to +24 analysis pixels.
- Figure H-f evaluates corridor radii 2–30 pixels. Precision is target
  foreground inside the corridor divided by corridor pixels; recall is target
  foreground inside the corridor divided by all target foreground; Dice is
  twice the intersection divided by the sum of target-foreground and corridor
  pixels.
- The default displayed corridor radius is 12 analysis pixels.
- Supplementary Figure 5-g reruns target_03 with generic coarse-scale upper
  bounds 1.60, 1.75 and 1.90, retaining seven grid points and all other settings.
  These are absolute analysis-scale bounds, not physical residual-scale bounds.
  Changing the endpoint also changes the interior grid spacing; the diagnostic
  assesses the complete coarse-grid setting, not only its endpoint.

The free-search grid is 0.70--1.60 (seven points), with +/-14% local scale
refinement. The physical-prior weight is zero. Each landscape uses the same
search/scoring configuration as its PipelineRun. R, Q and D are mask/corridor
retention, density and overlap, not ground-truth recognition/segmentation metrics.

Every plotted numeric value is also written under `generated/diagnostics/`.

The complete `generated/` directory is intentionally excluded from Git. A
release is defined by the committed inputs, algorithm, plotting code, and the
one-command reproduction entry point—not by cached raster outputs. Do not add
generated PNG files to a commit unless a clean end-to-end run has first passed
and the repository's publication policy is deliberately changed.

## Repository scope

The legacy six-ROI UV/NIR archive is distributed separately and is not an
input or output of structural matching.

## Rendering contract

- Python/matplotlib is the exclusive plotting backend.
- Arial and Arial Bold are required. The run stops instead of silently
  substituting another font.
- Manuscript outputs are RGB PNG with 600 dpi metadata.
- Target-derived standalone microscopy panels are exported at their analysis
  or native target dimensions without content-dependent crop, stretch,
  padding, or letterboxing. Reference-derived Supplementary Figure 4 panels
  undergo only the documented isotropic physical resampling needed to convert
  native 500 µm calibration to target-referenced sampling; no specimen crop or
  content-dependent zoom is applied, and any padding lies outside the retained
  source field. Fixed 946 x 820 canvases are used only
  for mathematical charts such as the score matrix, contour map, and
  sensitivity curve.
- Supplementary composite figures may contain explicitly fitted copies for
  page assembly; the corresponding standalone panels remain the authoritative,
  geometry-preserving evidence images.
- The workflow does not create PDF, TIFF, SVG, ZIP, or Word files.
- The target and reference scale-bar physical lengths are explicitly defined
  as 200 µm and 500 µm, respectively; the program does not infer either label
  by OCR. All manuscript display bars are 200 µm after target referencing.

## Relevant code

```text
paper_figures/
  run_all.py                              isolated reviewer launcher
  generate_all.py                        one algorithm run and shared orchestration
  diagnostics.py                         data-derived images and numerical source data
  generate_figure_h_panels.py            Figure H renderer
  scripts/export_supplementary_figures.py supplementary renderer
```
