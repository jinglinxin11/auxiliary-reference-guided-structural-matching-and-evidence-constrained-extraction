# Reproduction integrity fixes, 5 October 2026

The subsequent naming/structure revision adds a final-manuscript figure map,
preserves unrelated outputs when rerunning matching, and records export paths
relative to their manifests with explicit path bases. The legacy archive is
identified separately from current manuscript Fig. 14. Original filenames,
plotting calculations and scientific results are retained.

This additive maintenance revision does not change registration, topology,
candidate ranking, image evidence, the generic search grid, or the manuscript's
200/500 micrometre default acquisition assumptions and 200 micrometre display
bar. Historical source commits remain intact.

Native scale-bar provenance is read from the actual calibrations, rather than
hard-coded. The manuscript display bar remains a separate quantity. Default
200/500 output JSON bytes and numerical results are retained; custom lengths
are now reported consistently.

## Scope and privacy cleanup

The unrelated legacy six-ROI UV/NIR source data, plotting scripts and integrity
tests have moved out of this repository into a standalone historical archive.
Its earlier hash and lossless-export repairs are retained there. Matching CI
now tests only matching; the reviewer command is unchanged.

Current source files and delivery artifacts are scanned for personal filesystem
roots. Paths in new export manifests are relative. Git history and old release
tags are intentionally not rewritten. No manuscript file or scientific formula
is modified; maintenance revisions are distinct from the original study record.
