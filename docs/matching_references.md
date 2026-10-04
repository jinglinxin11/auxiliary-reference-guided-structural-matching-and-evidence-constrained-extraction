# Matching References and Implementation Mapping

Verified on 2026-10-04 against publisher-deposited Crossref metadata, original
papers and official package documentation. Numbers are the SI reference numbers,
not a new numbering scheme. References 1--33 are outside this targeted update.

| SI reference | Role | Code |
| --- | --- | --- |
| 34 | Phase-correlation translation seeds; methodological background, not an exact claim of reimplementing the paper | `registration.py`, `cv2.phaseCorrelate` |
| 35 | Chamfer/distance-based matching background; the exponential weighting and component combination are project-specific | `registration.py`, `_geometry_score` |
| 36 | Local structure-tensor orientation estimation | `image_processing.py`, `orientation_fields` |
| 37 | Nelder-Mead optimization method | `registration.py`, `scipy.optimize.minimize` |
| 38 | Douglas-Peucker path simplification for directional segments | `topology_metrics.py` |
| 39 | Zhang-Suen thinning; the default 2D skeletonization family | `skimage.morphology.skeletonize` |
| 40 | scikit-image implementation library (new SI citation) | `image_processing.py`, `registration.py`, `topology_metrics.py` |
| 41 | SciPy numerical implementation library (new SI citation) | `registration.py` |

## Verified References

34. Foroosh, H., Zerubia, J. B. & Berthod, M. Extension of phase correlation to
subpixel registration. IEEE Trans. Image Process. 11, 188-200 (2002).
https://doi.org/10.1109/83.988953

35. Borgefors, G. Hierarchical chamfer matching: a parametric edge matching
algorithm. IEEE Trans. Pattern Anal. Mach. Intell. 10, 849-865 (1988).
https://doi.org/10.1109/34.9107

36. Bigun, J., Granlund, G. H. & Wiklund, J. Multidimensional orientation
estimation with applications to texture analysis and optical flow. IEEE Trans.
Pattern Anal. Mach. Intell. 13, 775-790 (1991).
https://doi.org/10.1109/34.85668

37. Nelder, J. A. & Mead, R. A simplex method for function minimization.
Comput. J. 7, 308-313 (1965). https://doi.org/10.1093/comjnl/7.4.308

38. Douglas, D. H. & Peucker, T. K. Algorithms for the reduction of the number
of points required to represent a digitized line or its caricature.
Cartographica 10, 112-122 (1973). https://doi.org/10.3138/fm57-6770-u75u-7727

39. Zhang, T. Y. & Suen, C. Y. A fast parallel algorithm for thinning digital
patterns. Commun. ACM 27, 236-239 (1984).
https://doi.org/10.1145/357994.358023

40. van der Walt, S. et al. scikit-image: image processing in Python.
PeerJ 2, e453 (2014). https://doi.org/10.7717/peerj.453

41. Virtanen, P. et al. SciPy 1.0: fundamental algorithms for scientific
computing in Python. Nat. Methods 17, 261-272 (2020).
https://doi.org/10.1038/s41592-019-0686-2

## Implementation Checks and Citation Limits

- [scikit-image skeletonize documentation](https://scikit-image.org/docs/0.25.x/api/skimage.morphology.html#skimage.morphology.skeletonize) identifies Zhang's algorithm as the default for 2D inputs.
- [SciPy Nelder-Mead documentation](https://docs.scipy.org/doc/scipy-1.15.3/reference/optimize.minimize-neldermead.html) identifies the implemented optimization method.
- [OpenCV phase-correlation documentation](https://docs.opencv.org/4.13.0/d7/df3/group__imgproc__motion.html) documents the translation-seed API actually called by this project.
- The SciPy article has an [author/affiliation correction](https://www.nature.com/articles/s41592-020-0772-5). It does not change the algorithm citation used here.
- These references support method lineage or software implementation. They do
  not validate the project's weights, physical metadata, scoring matrix,
  recognition accuracy, segmentation accuracy or performance on four cases.
- Free matching still uses bounded scale/angle/translation search, not an
  unbounded or externally validated matching method. No physical-prior method
  is being introduced or cited as an active component.
