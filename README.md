# Auxiliary-reference-guided structural matching and evidence-constrained extraction of laser-written photochromic patterns

Repository: [Source code](https://github.com/jinglinxin11/auxiliary-reference-guided-structural-matching-and-evidence-constrained-extraction).

This project implements auxiliary-reference-guided structural matching and
evidence-constrained extraction for laser-written photochromic patterns. It
independently matches target microscopy images against
structural reference images. It registers each reference to a target, retains
only target evidence inside the selected corridor, and exports both a
natural-background presentation image and a non-fabricating binary mask.

## Input Layout

```text
data/input/
  target_images/       # Four target JPG or PNG images, ordered by filename
  reference_images/    # Four reference PNG images; filenames supply labels
```

The committed targets are byte-identical copies of the four main-directory
JPEG images. The reference PNGs are byte-identical copies of the verified
auxiliary images.

## Physical-scale convention

The two input sets do not use the same acquisition annotation:

| image set | validated native scale-bar length | role in the workflow |
| --- | ---: | --- |
| target images | 200 µm | physical reporting and figure display |
| reference images | 500 µm | physical reporting and figure display only |

The program detects the scale-bar graphic but does not infer its text by OCR.
The validated lengths above are explicit defaults and are recorded in the
generated JSON/CSV provenance. Calibration does not constrain registration or
contribute to candidate ranking on this free-matching branch. Any reference view exported for the manuscript is
then isotropically resampled to target-referenced sampling and labelled with a
200 µm bar. A common physical canvas is formed with background-only padding,
so the composite uses the same pixels-per-micrometre for every candidate. The
committed native inputs remain unchanged for audit. No specimen crop or
content-dependent zoom is used in this conversion.

Matching uses the archived generic seven-point scale grid from 0.70 to 1.60,
with local scale refinement of +/-14%, coarse rotations -5/0/5 degrees and
translations limited to +/-144 analysis pixels. It is free of a physical-scale
prior, not an unbounded transform search. Registration optimizes geometry G;
topology T is evaluated at that transform, and F = 0.72G + 0.28T ranks candidates.
The score matrix is not a statistical confusion matrix or an accuracy estimate.
No human-review thresholds or flags participate in the pipeline.

## Run

For a white annotation panel, calibration measures the black horizontal bar
inside the panel, not the panel width. The detected bar and annotation bounds
are recorded separately in the figure diagnostics. Bar width uses its outer
pixel-edge span, including the endpoint ticks. Native affine conversion uses
the separate source and target analysis shapes; axial directions are sampled
through their double-angle vectors rather than interpolating wrapped angles.

```powershell
python -m pip install -r requirements.txt
python -B run_matching.py --targets data\input\target_images --references data\input\reference_images --outdir artifacts\matching_results
```

On Linux or macOS, use forward slashes:

```bash
python -m pip install -r requirements.txt
python -B run_matching.py --targets data/input/target_images --references data/input/reference_images --outdir artifacts/matching_results
```

The generated directory contains one `results.json`, four presentation PNGs,
and four matched-only binary PNGs. Generated artifacts are intentionally not
tracked by Git.

## Test

```powershell
python -B -m pytest -q tests
```

## Paper-figure code

The reviewer entry point under [`paper_figures/`](paper_figures/README.md)
runs the four-by-four matching algorithm directly from `data/input/`, writes
all plotted diagnostic values, and exports eight standalone Figure H PNG
panels, five complete supplementary figures, and all 42 constituent
supplementary panels from that same run:

```powershell
python paper_figures/run_all.py
```

This is the reviewer command recommended in the Supplementary Information. It
creates an isolated temporary environment, reruns all 16 target–reference
registrations, and regenerates every Figure H and Supplementary Figure panel
from the committed inputs. The scale assumptions can be stated explicitly,
without editing code:

```powershell
python paper_figures/run_all.py --target-scale-bar-um 200 --reference-scale-bar-um 500
```

It requires Arial and does not generate a ZIP, Word document, PDF, SVG, or
TIFF. No manuscript score or sensitivity curve is loaded from a frozen figure.

Generated manuscript figures are intentionally not tracked by Git. Reviewers
recreate them from the committed input images and current algorithm with the
single command above. This prevents stale or manually post-processed PNG files
from diverging from the published source code.

Detailed file definitions, numerical formulas, output counts, and the
scale-conversion audit are documented in
[`paper_figures/README.md`](paper_figures/README.md). The manuscript may cite
the repository root and this reviewer entry point.

## Free-matching revision

The free-matching revision, developed on `free-matching-si-20261004` and merged
into `main`, integrates the free-search settings from the
supplied reproduction archive with the existing figure framework. Black-bar
calibration, source/target native-coordinate conversion and axial double-angle
interpolation are corrected. Scores must therefore be regenerated, not copied
from the historical screenshot. See `docs/free_matching_revision.md` for the
code/Supplementary Information alignment. Supplementary documents are delivered
locally and are not published with the code branch.
Verified method and implementation citations are mapped to the actual code in
[`docs/matching_references.md`](docs/matching_references.md).

## Supplementary Figure S14 reproduction

The UV-versus-NIR spatial-confinement analysis has two additional plotting
entry points under
[`paper_figures/figure_s14/`](paper_figures/figure_s14/README.md). The first
regenerates the complete eight-panel Figure S14; the second exports its eight
logical panels separately:

```powershell
python paper_figures/figure_s14/plot_figure_s14.py
python paper_figures/figure_s14/export_figure_s14_panels.py
```

The directory includes pinned plotting dependencies, 138 checksum-protected
figure-level source-data files and detailed reviewer instructions. These two
commands reproduce the plotting stage from archived registered images and
ROI-level outputs; they do not rerun the upstream registration or ROI
measurement workflow.
