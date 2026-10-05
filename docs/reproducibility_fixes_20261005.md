# Reproduction integrity fixes, 5 October 2026

This additive maintenance revision does not change registration, topology,
candidate ranking, image evidence, the generic search grid, or the manuscript's
200/500 micrometre default acquisition assumptions and 200 micrometre display
bar. Historical source commits remain intact.

Native scale-bar provenance is read from the actual calibrations, rather than
hard-coded. The manuscript display bar remains a separate quantity. Default
200/500 output JSON bytes and numerical results are retained; custom lengths
are now reported consistently.

Figure S14 source text is stored with canonical LF bytes and protected with
`-text` attributes so Git never converts its hash-protected bytes on checkout.
The 138-entry manifest is refreshed against those canonical committed bytes,
including the already-committed analysis_pipeline.md. Only line endings and
integrity metadata are revised; parsed CSV/JSON values, profile samples, images
and plotting calculations are unchanged. The validator also checks coverage,
duplicate entries and byte sizes.

PNG is the canonical 600-dpi raster for S14. TIFF is now saved losslessly from
that PNG, rather than by a second Matplotlib renderer pass, and its size, mode
and every pixel are verified after reload. PDF/SVG and all scientific plotting
calculations are unchanged.

CI checks S14 input integrity on Windows and Linux and runs both plotting entry
points on Windows, where the required Arial family is available. This does not
claim a local Linux end-to-end plotting test.

The original reviewer command and both Figure S14 commands remain unchanged.
S14 regenerates archived plots only, not its upstream ROI measurement workflow.
No scientific manuscript changes are required by these fixes. To cite the
maintenance implementation itself, record its new revision separately from the
historical source revision that produced the original study results.
