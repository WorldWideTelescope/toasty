# -*- mode: python; coding: utf-8 -*-
# Copyright 2013-2021 Chris Beaumont and the AAS WorldWide Telescope project
# Licensed under the MIT License.

from astropy.coordinates import Angle
from astropy.io import fits
from astropy.utils.data import download_file
from astropy.wcs import WCS
import os.path
import reproject
from shutil import copyfile
from subprocess import Popen, PIPE, STDOUT, run
import tempfile

from toasty import builder, collection, pyramid, multi_tan, multi_wcs
from wwt_data_formats.enums import ProjectionType


class FitsTiler:
    def tile_tan(self, fits, out_dir, hdu_index, cli_progress, **kwargs):
        pio = pyramid.PyramidIO(out_dir, default_format="fits")
        bld = builder.Builder(pio)
        coll = collection.SimpleFitsCollection(fits, hdu_index=hdu_index, **kwargs)

        if coll._is_multi_tan():
            if cli_progress:
                print("Tiling base layer in multi-TAN mode (step 1 of 2)")
            tile_processor = multi_tan.MultiTanProcessor(coll)
            tile_processor.compute_global_pixelization(bld)
            tile_processor.tile(pio, cli_progress=cli_progress, **kwargs)
        else:
            if cli_progress:
                print("Tiling base layer in multi-WCS mode (step 1 of 2)")

            tile_processor = multi_wcs.MultiWcsProcessor(coll)
            tile_processor.compute_global_pixelization(bld)
            tile_processor.tile(
                pio, reproject.reproject_interp, cli_progress=cli_progress, **kwargs
            )

        if cli_progress:
            print("Downsampling (step 2 of 2)")
        bld.cascade(cli_progress=cli_progress, **kwargs)

        # Using the file name of the first FITS file as the image collection name
        bld.set_name(out_dir.split("/")[-1])
        bld.write_index_rel_wtml()

        return out_dir, bld

    def tile_hips(self, fits, out_dir, hdu_index, cli_progress):
        hipsgen_path = download_file(
            "https://aladin.unistra.fr/java/Hipsgen.jar",
            show_progress=cli_progress,
            cache=True,
            package="toasty",
        )

        if hdu_index is None:
            hdu_index_args = []
        else:
            if isinstance(hdu_index, int):
                arg = "hdu=" + ",".join([str(hdu_index)] * len(fits))
            else:
                arg = "hdu=" + ",".join(str(i) for i in hdu_index)
            hdu_index_args = [arg]

        # If we give hipsgen a relative output directory it will end up
        # inside `in_dir`
        abs_out_dir = os.path.abspath(out_dir)

        with self._create_hipsgen_input_dir(fits) as in_dir_path:
            argv = [
                "java",
                "-jar",
                "{0}".format(hipsgen_path),
                "in={0}".format(in_dir_path),
                "out={0}".format(abs_out_dir),
                "creator_did=ivo://aas.wwt.toasty/{0}".format(out_dir),
            ]
            argv += hdu_index_args
            argv += ["INDEX", "TILES"]

            p = Popen(
                argv,
                stdout=PIPE,
                stderr=STDOUT,
                shell=False,
            )

            # Even if we don't want to print the output, this loop is still useful since it waits until the HiPSgen process
            # is completed.
            for line in p.stdout:
                if cli_progress:
                    print(line.decode("UTF-8"))

            if p.wait() != 0:
                if cli_progress:
                    m = "see its output printed above"
                else:
                    m = "set `cli_progress=True` to see its output"
                raise Exception(f"an error occurred running hipsgen; {m}")

        if not os.path.isdir(out_dir):
            if cli_progress:
                m = "see its output printed above"
            else:
                m = "set `cli_progress=True` to see its output"
            raise Exception(
                f"output directory `{out_dir}` does not exist, meaning `hipsgen` probably failed; {m}"
            )

        pio = pyramid.PyramidIO(out_dir, default_format="fits")
        bld = builder.Builder(pio)
        bld = self.copy_hips_properties_to_builder(bld, out_dir)
        bld.write_index_rel_wtml()
        return out_dir, bld

    def fits_covers_large_area(self, fits_list, hdu_index=None):
        corners = []

        for fits_path in fits_list:
            with fits.open(fits_path) as hdul:
                hdu = None
                if hdu_index is None:
                    for hdu in hdul:
                        if (
                            hasattr(hdu, "shape")
                            and len(hdu.shape) > 1
                            and type(hdu) is not fits.hdu.table.BinTableHDU
                        ):
                            break
                elif isinstance(hdu_index, int):
                    hdu = hdul[hdu_index]
                else:
                    hdu = hdul[hdu_index[fits_list.index(fits_path)]]

                wcs = WCS(hdu.header)
                corners.append(wcs.pixel_to_world(0, 0))
                corners.append(wcs.pixel_to_world(hdu.shape[0], 0))
                corners.append(wcs.pixel_to_world(hdu.shape[0], hdu.shape[1]))
                corners.append(wcs.pixel_to_world(0, hdu.shape[1]))

        max_distance = Angle("0d")
        for compare_index in range(len(corners)):
            for index in range(compare_index + 1, len(corners)):
                distance = corners[compare_index].separation(corners[index])
                if distance > max_distance:
                    max_distance = distance

        return max_distance > Angle("20d")

    def is_java_installed(self):
        java_version = run(
            ["java", "-version"], capture_output=True, text=True, check=True
        )
        return (
            "version" in java_version.stdout.lower()
            or "version" in java_version.stderr.lower()
        )

    def _create_hipsgen_input_dir(self, fits_list):
        dir = tempfile.TemporaryDirectory()

        for fits_file in fits_list:
            link_name = os.path.basename(fits_file)
            absolute_path = os.path.abspath(fits_file)
            link_path = os.path.join(dir.name, link_name)
            os.symlink(src=absolute_path, dst=link_path)

        return dir

    def copy_hips_properties_to_builder(self, bld, out_dir):
        hips_properties = dict()
        with open("{0}/properties".format(out_dir)) as prop:
            for line in prop:
                if line[0] != "#":
                    key_value_pair = line.split("=")
                    hips_properties[key_value_pair[0].strip()] = key_value_pair[
                        1
                    ].strip()
        bld.set_name(out_dir.split("/")[-1])
        bld.imgset.projection = ProjectionType.HEALPIX
        bld.imgset.file_type = "fits"
        bld.imgset.tile_levels = int(hips_properties["hips_order"])
        bld.place.dec_deg = float(hips_properties["hips_initial_dec"])
        bld.place.ra_hr = float(hips_properties["hips_initial_ra"]) / 15.0
        bld.place.zoom_level = float(hips_properties["hips_initial_fov"])
        bld.imgset.center_x = float(hips_properties["hips_initial_ra"])
        bld.imgset.center_y = float(hips_properties["hips_initial_dec"])
        bld.imgset.base_degrees_per_tile = float(hips_properties["hips_initial_fov"])
        bld.imgset.url = "Norder{0}/Dir{1}/Npix{2}"
        return bld
