# toasty 0.20.0 (2024-12-29)

- Add multi-WCS support to the core FITS loading support (#103, @pkgw). This
  allows you to choose which set of WCS information to load from a FITS HDU when
  it has multiple ones using different lettered "keys". DASCH mosaics use these
  to capture astrometric solutions for multiple-exposure plates.
- In the pipeline, fix incoming JSON from some installations of Djangoplicity
  (#104, @pkgw). These clearly have some Python 3 issue where strings come
  through as encoded Python bytes, `b"..."`. These results are coming directly
  from the servers, so we have to patch them up ourselves.
- Add `--tunnel-initcmd` option to `toasty view` (#104, @pkgw). If you are using
  the `toasty view` remote-tunnel functionality, you may need to run some
  commands on the remote host to set up the shell environment to make the remote
  `toasty` command available. This option allows you to do that.

The DOI of this release is [10.5281/zenodo.14570962][xdoi].

[xdoi]: 10.5281/zenodo.14570962


# toasty 0.19.1 (2024-07-21)

- Update for Numpy 2.0 compatibility (#102, @pkgw). Previous releases will
  work in most cases, but are not 100% compatible.
- If guessing parallelism in a Slurm HPC execution environment, try to respect
  the job's resource allocation (#101, @pkgw). Often, on an HPC cluster the
  number of CPU cores on the host machine will be a bad indicator of the
  parallelism level that you should target, because you may only be allocated a
  small fraction of them.


# toasty 0.19.0 (2023-12-14)

- Implement a `--tiling-method` argument for `toasty view` (#97, @pkgw). This
  allows you to force the choice of a specific method. In particular, sometimes
  it is helpful to force the use of TOAST to get the most accurate display over
  large angular sizes.
- Fix an outdated usage that broke processing of all-sky plate carrée ecliptic
  images with Astropy 6.x (#99, @pkgw)
- Fix TOASTing of multi-plane (e.g, RGB) images that don't cover the whole sky
  (#99, @pkgw). This fixes processing of RGB images that have lots of pixels but
  don't necessarily cover huge solid angles.
- In `toasty tile-study`, if we're getting WCS information from a FITS file but
  its dimensions disagree with the input image, try rescaling the pixel size if
  the overall image shape is the same (#99, @pkgw). This reproduces behavior
  already implemented for AVM processing, and helps if, say, you want to process
  a large image where you've submitted a scaled-down version of it to
  Astrometry.Net.
- Various fixes to the test suite and CI system.


# toasty 0.18.1 (2022-09-07)

- Fix tiling on macOS+Py3.7 due to an unexpectedly unimplemented API (#94,
  @pkgw).

The DOI of this release is [10.5281/zenodo.7058238][xdoi].

[xdoi]: https://doi.org/10.5281/zenodo.7058238


# toasty 0.18.0 (2022-09-06)

This release of Toasty contains a whole boatload of improvements! There are
no less than three major ones:

- Support tiling FITS data to the all-sky TOAST projection (#86, @imbasimba)!
  Now you can create all-sky FITS datasets that can be displayed in the latest
  release of the WWT engine. This includes a new routine to automatically
  determine the appropriate TOAST resolution level.
- A new `-t` option to `toasty view` allows you to view FITS data on remote
  systems using SSH tunneling (#87, @pkgw)! The tunnel mode uses SSH to tile
  the data on the remote machine, run a server, and tunnel the server to the
  local machine for display by your web browser.
- Finally, Toasty releases are now automatically deposited with Zenodo and
  assigned DOIs in the process. This makes it possible to cite the Toasty
  software, indicating exactly which version you were using, in scholarly
  context. The new command `toasty show version-doi` will display the DOI of the
  specific version of Toasty that you're running.

Some smaller improvements support these changes:

- Some of Toasty's internal systems were reorganized to allow for more efficient
  and flexible processing of pyramids (#89, #90, @pkgw). It is now possible to
  perform the "cascade" operation on sub-pyramids of data, allowing for parallel
  processing in HPC scenarios. A new `toasty.pyramid.Pyramid` data structure
  consolidates related code, reducing several nearly duplicate algorithms, and
  provides a more coherent formalism for treating operations on pyramids.
- Also, the code for filtering TOAST pyramids based on latitude/longitude bounds
  was fixed to work when the in-bounds area spanned more than 180 degrees, and
  also was made faster using Cython.
- Other efficiency improvements include:
  - Not writing all-flagged images (#88, @pkgw)
  - Avoiding creation of pyramid directories when reading imagery
  - Avoiding launching parallel operations when there is no work to do
  - Consolidating preparatory work for parallelized cascading
- When Toasty operations are being run in non-interactive scenarios, progress
  bars are now printed much more rarely and without screen overwrites, making
  for smaller and more readable log files (#88, @pkgw). This functionality is
  provided by a small new `toasty.progress` module.
- 16-bit integer images are now supported (#84, @imbasimba).
- DASCH FITS files with TPV distortions are now loaded with the correct LONPOLE
  setting.

The DOI of this release is [10.5281/zenodo.7055477][xdoi].

[xdoi]: https://doi.org/10.5281/zenodo.7055477


# toasty 0.17.1 (2022-07-14)

- Properly match and propagate diagonal PC headers in multi-tan processing (#83,
  @pkgw). This fixes processing of the JWST Level 3 FITS data for the deep
  field, which are on a rotated TAN projection.


# toasty 0.17.0 (2022-07-12)

- Add an `--avm-from` option to `toasty tile-study`, which would have been
  useful with the JWST imagery released yesterday (#82, @pkgw).
- Support tiled FITS in `toasty tile-healpix` (#79, #80, @pkgw), and add a
  `--force-galactic` option.
- Avoid HEALPix HDUs without data (#79, @pkgw)
- Add some diagnostics for spatial AVM information in `toasty check-avm` (#78,
  @pkgw)
- Update tests for new `wwt_data_formats` constellation support and other
  changing dependencies.


# toasty 0.16.1 (2022-01-27)

- Toasty is now more forgiving with FITS and WCS shapes when tiling FITS data
  (#76, @pkgw). In particular, it will behave more correctly when the data and
  WCS shapes disagree, and if the data have interesting structure in the
  non-celestial axes, Toasty will take the first celestial plane it finds rather
  than rejecting the input file.


# toasty 0.16.0 (2022-01-25)

- Add support for some more kinds of longitude arrangements seen in planetary
  maps: "zero left" where the longitude = 0 line is on the left edge of the
  image, rather than in the center, and "zero right" which is comparable except
  that longitude increases to the left, as usually seen in sky maps, rather than
  to the right (#75, @pkgw). These are available in the CLI with the new
  `plate-carree-planet-zeroleft` and `plate-carree-planet-zeroright` projection
  types.
- When creating planetary TOAST maps, actually use the planetary TOAST
  coordinate system by default (#75, @pkgw).


# toasty 0.15.0 (2022-01-14)

- Start adding metadata about data min/max values and suggested pixel range cuts
  for tiled FITS data sets, for either TOAST or HiPS-based data processing (#71,
  @imbasimba). This will allow the renderer to provide nice default settings
  when opening up FITS datasets.
- Add support for 32-bit integer FITS (#72, @imbasimba)
- Allow Astropy's WCS code to fix non-standard FITS headers, which increases our
  compatibility with more FITS datasets in the wild (#73, @imbasimba)
- Add the `--fits-wcs` argument to `tile-study`, to apply coordinates to an RGB
  image based on the data contained in a separate FITS file (#74, @pkgw). This
  is especially useful if you have an image that Astrometry.Net can solve, since
  that service produces small downloadable FITS files with its solution
  information.
- Reorganize the API docs a bit (#74, @pkgw)


# toasty 0.14.0 (2021-12-13)

- Expand the all-in-one FITS API, [`toasty.tile_fits`], to invoke the
  [`hipsgen`] program when given an image that is larger than about 20° on the
  sky ([#69], [@imbasimba], [@pkgw]). This is the breakpoint at which WWT's tangential
  projection starts yielding visually poor results.
- Add the [`toasty view`] CLI tool the builds on the above, and the new
  scripting support in the resarch app, to act as a command-line FITS viewer
  ([#69], [@pkgw])! Just run `toasty view myfile.fits` to view interactively in your
  browser, with sky context and all of the features provided by the research
  app.
- When loading FITS collections, the `hdu_index` can now be a list of integers,
  instead of just one integer ([#69], [@imbasimba]). This lets you specify different
  image HDUs to use for different input files.
- Various new APIs and internal improvements to enable the above; there's a new
  [`toasty.fits_tiler`] module and new interfaces in [`toasty.collection`].
- Add a hack to strongarm AstroPy into being willing to load WCS from improper
  files that include TPV distortions without using the `-TPV` projection type
  ([#69], [@pkgw]). This allows us to view some of the [DASCH] FITS files.

[`toasty.tile_fits`]: https://toasty.readthedocs.io/en/latest/api/toasty.tile_fits.html
[`hipsgen`]: https://aladin.u-strasbg.fr/hips/HipsIn10Steps.gml
[#69]: https://github.com/WorldWideTelescope/toasty/pull/69
[@imbasimba]: https://github.com/imbasimba
[@pkgw]: https://github.com/pkgw
[`toasty view`]: https://toasty.readthedocs.io/en/latest/cli/view.html
[`toasty.tile_fits`]: https://toasty.readthedocs.io/en/latest/api/toasty.tile_fits.html
[`toasty.fits_tiler`]: https://toasty.readthedocs.io/en/latest/api.html#module-toasty.fits_tiler
[`toasty.collection`]: https://toasty.readthedocs.io/en/latest/api.html#module-toasty.collection
[DASCH]: http://dasch.rc.fas.harvard.edu/project.php


# toasty 0.13.0 (2021-11-17)

- Add an automagical all-in-one API, `toasty.tile_fits`, that takes FITS input
  and tiles it (#68, @imbasimba). The goal here is to do the right thing with
  any kind of non-ridiculous input you can throw at it.
- Turn `reproject` and `shapely` into hard dependencies to enable the above
  API to work reliably (#68, @imbasimba).


# toasty 0.12.0 (2021-11-01)

- Both toasty's AstroPix/Djangoplicity pipeline and the `wwt_data_formats`
  module had WCS handling bugs that canceled each other out. The data-formats
  bug was fixed in release 0.10.2 of that package, which caused the Toasty bug
  to become apparent. Fix that (reported by @astrodavid10, #65; fixed by @pkgw,
  #66).
- Fixed and features needed to process the SELENE Kaguya TC dataset (@pkgw,
  #63). Unfortunately these changes are lacking corresponding documentation:
  - Add a U8 image mode.
  - Add APIs to filter out out subtrees when sampling TOAST pyramids.
  - Add proper support for the planetary TOAST coordinate system, which is
    rotated 180 degrees in longitude from the celestial one.
  - Add support for JPEG2000 images.
  - Add support for chunked TOAST tiling.
  - Add a chunked plate-carree TOAST sampler.
  - Fix out-of-date data when updating PIL-based images.
  - Improve multiprocessing implementations to avoid race conditions on exit and
    operate more robustly in multi-node (HPC) contexts.
  - Add the ability for `toasty transform` (and underlying APIs) to emit the
    transformed data into a separate pyramid; i.e. create a tree of only JPG
    files from a tree of NPY files.
  - Add `toasty transform u8-to-rgb`
  - Don't create every directory when removing lockfiles
- Fix FITS file update on Windows (#67, @imbasimba)
- Improve FITS heuristics to ignore binary tables and other HDUs without a
  defined shape (#62, @imbasimba).


# toasty 0.11.0 (2021-09-17)

- Fix up `toasty tile-study` to handle FITS files properly (@pkgw, #61). The
  input must be in a tangential projection, and only some basic data layouts
  within the FITS container are supported. The `--placeholder-thumbnail` option
  also must be used.
- Fix an off-by-one error in the computations used by `toasty tile-multi-tan`
  (@pkgw, #61)
- Improve some internal APIs for processing studies.


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
