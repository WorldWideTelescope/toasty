# toasty 0.10.0 (2021-09-10)

- Add `toasty check-avm`, which opens up an image file and reports whether it
  contains AVM (Astronomy Visualization Metadata) tags. This requires that the
  `pyavm` module is installed (#59, @pkgw).
- Add the `--avm` option to the `toasty tile-study` command (#59, @pkgw). When
  specified, spatial positioning information for the input image will be loaded
  from AVM tags in the input image and preserved in the resulting WTML file.
  This option doesn't "just work" automatically (for now) because it requires
  the `pyavm` module to be present, and we don't want to make that a hard
  requirement of installing Toasty.
- Fix `toasty tile-wwtl` to emit correct WTML files once again (#58, @pkgw).
- Increase the ability of the "multi-WCS" FITS tiling functionality to handle
  huge images by reprojecting them in (large) chunks. This shouldn't affect
  performance with reasonable-sized images, but makes it possible to handle
  large ones. Here "large" means that the image consumes something like 10-25%
  of the available system memory.
- Silence various unhelpful Python warnings
- Enable FITS processing to work when the input image has more than two axes,
  if the other axes are only one element long (#57, @pkgw).
- Write out `DATAMIN` and `DATAMAX` headers in output FITS files, which helps
  WWT set the correct scaling for FITS visualization (#57, @pkgw).


# toasty 0.9.0 (2021-08-25)

- Add a `plate-caree-panorama` projection mode to the `tile-allsky` command
  (#55, @astrodavid10).


# toasty 0.8.0 (2021-08-19)

- Add a `--name` argument to the `tile-wwtl` command (#53, #54, @astrodavid10,
  @pkgw).


# toasty 0.7.1 (2021-08-06)

- No code changes from 0.7.0. The Python package didn't publish to PyPI due
  to an issue with the automation, which should now be fixed.


# toasty 0.7.0 (2021-08-06)

- Add the `toasty pipeline ignore-rejects` command to allow you to tell the
  Toasty pipeline system to ignore certain images going forward. This will be
  helpful if your pipeline provides some images that, say, aren't actually
  images of the sky (#51, @pkgw).
- Start requiring and using version 0.10 of the [wwt_data_formats] support
  library. This version includes important improvements to how image coordinates
  (WCS) are handled. Previously, some kinds of coordinates weren't handled
  completely correctly. While it's better to do this correctly, the new code may
  break some existing workflows if they accidentally relied on the broken
  behavior.
- Implement end-to-end support for tiling FITS data in the backend (#52, @pkgw)!
  These datasets can be displayed using the very latest version of the WWT
  rendering engine. Toasty's support for creating these datasets needs to be
  exposed in a more user-friendly way, including documentation and examples,
  but the core algorithms should generate working datasets.

[wwt_data_formats]: https://wwt-data-formats.readthedocs.io/


# toasty 0.6.4 (2021-02-09)

- Properly handle CLI glob arguments on Windows. It turns out that we need to
  handle them manually, sigh. This relies on new functionality added in
  `wwt_data_formats` 0.9.1 (which I should have versioned as 0.10.0 because it
  adds a new API, but oh well).


# toasty 0.6.3 (2021-02-03)

- If a PIL image loads up with an unexpected mode, try to convert it to regular
  RGB or RGBA. This should fix handling of images with palette color ("P" mode)
- In the Djangoplicity pipeline, handle a test case where the second
  Spatial.Scale tag is empty (observed in NOIRLab noao-02274).
- In the Djangoplicity pipeline, make sure to use UTF8 encoding when writing out
  JSON. Should fix processing of images whose descriptions contain non-ASCII,
  when running on Windows.
- Fix the pyramid I/O code, which was incorrectly choosing a "none" output format
  in certain codepaths. Closes #43.


# toasty 0.6.2 (2020-12-17)

- Add a few knobs so that we can get the Djangoplicity pipeline working for
  `eso.org`
- Tidy up the pipeline output a little bit.


# toasty 0.6.1 (2020-12-09)

Some fixes to the pipeline functionality:

- Add globbing support for the operations that take image-id arguments
- Attempt to fix crashing on non-actionable candidates on Windows
- Improvements to the relevant docs
- Bump the required version of `wwt_data_formats` to the correct value


# toasty 0.6.0 (2020-12-04)

- Start supporting the pipeline processing framework! See the documentation for
  a workflow outline and explanations of the `toasty pipeline` commands (#40,
  @pkgw)
- Start supporting FITS tiling! FITS files can now be procesed with the
  `tile-study` subcommand (@astrofrog, #30)
- In service of the above, improve how image modes and their corresponding file
  formats are handled. The internal systems are now more sensible and can
  properly handle FITS images (@astrofrog, #30)
- Also start supporting the attachment of WCS information to images. This should
  help us make it so less special-casing of different image types is needed.
- Fix some dumb bugs in the merging machinery so that our high-level tiles
  don't come out busted.


# toasty 0.5.0 (2020-10-26)

- Add a `plate-carree-ecliptic` projection mode, for images that are in a plate
  carrée projection but in a barycentric true ecliptic coordinate system
- Add a `--crop` option to generic image-loading commands that allows you to crop
  pixels off the edges of input images before processing them.
- Add a new image mode, “F16x3”, corresponding to three planes of “half
  precision” floating-point numbers. This is useful for high-dynamic-range (HDR)
  processing.
- Process OpenEXR files using the new F16x3 mode, rather than converting them to
  RGB upon load.
- Add a `--type` option to the `cascade` command to allow cascading more file
  types than just PNG: now arrays of floating-point data can be cascaded from
  the command line, too, including F16x3 tiles.
- Add a `transform fx3-to-rgb` command to transform three-plane floating-point
  pyramids into RGB data. In combination with the above features, this means
  that you can tile large OpenEXR files and preserve the dynamic range all the
  way down to the base tile. If the image is converted to RGB first, the
  dynamic-range limitations of 8-bit colors cause the detail to be washed out as
  the image is downsampled.

Some lower-level changes:

- Group pipeline commands under a subcommand
- Rename `healpix-sample-data-tiles` to `tile-healpix`
- Start building support for multi-generic-WCS tiling
- Avoid deadlocking in very large cascade operations
- Avoid annoying warnings in the averaging_merger when there are NaNs
- Specify UTF-8 encoding whenever working with text

# toasty 0.4.0 (2020-10-05)

- In WTML outputs, omit the <Place> wrapper for all-sky data sets
- When using `tile-allsky` in `plate-carree-planet` mode, use the "Planet" data
  set type
- Add `--name` options to `tile-allsky` and `tile-study`

# toasty 0.3.3 (2020-09-29)

- Make sure to close WWTL files after reading them in. May fix the test suite
  on some Windows machines.

# toasty 0.3.2 (2020-09-29)

- Switch to Cranko for versioning and release management, and Azure Pipelines
  for CI/CD, and Codecov.io for coverage monitoring.
- Fix tests on Windows, where there is no `healpy`

# 0.3.1 (2020 Sep 21)

- If PIL is missing colorspace support, don't crash with an error, but provide a
  big warning.
- Add a `plate-carree-galactic` projection type, for equirectangular images in
  Galactic coordinates.
- In the plate carrée image samplers, round nearest-neighbor pixel coordinates
  rather than truncating the fractional component. This should fix a half-pixel
  offset in TOASTed maps.
- Remove some old functionalities that are currently going unused, and not
  expected to become needed in the future.

# 0.3.0 (2020 Sep 18)

- Attempt to properly categorize Cython as a build-time-only dependency. We don't
  need it at runtime.

# 0.2.0 (2020 Sep 17)

- Add a first cut at support for OpenEXR images. This may evolve since it might
  be valuable to take more advantage of OpenEXR's support for high-dynamic-range
  imagery.
- Add cool progress reporting for tiling and cascading!
- Fix installation on Windows (hopefully).
- Add a new `make-thumbnail` utility command.
- Add `--placeholder-thumbnail` to some tiling commands to avoid the thumbnailing
  step, which can be very slow and memory-intensive for huge input images.
- Internal cleanups.

# 0.1.0 (2020 Sep 15)

- Massive rebuild of just about everything about the package.
- New CLI tool, `toasty`.

# 0.0.3 (2019 Aug 3)

- Attempt to fix ReadTheDocs build.
- Better metadata for PyPI.
- Exercise workflow documented in `RELEASE_PROCESS.md`.

# 0.0.2 (2019 Aug 3)

- Revamp packaging infrastructure
- Stub out some docs
- Include changes contributed by Clara Brasseur / STScI
