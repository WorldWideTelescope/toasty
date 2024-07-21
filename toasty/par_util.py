# -*- mode: python; coding: utf-8 -*-
# Copyright 2020-2024 the WorldWide Telescope project
# Licensed under the MIT License.

"""Utilities for parallel processing

"""

__all__ = """
SHOW_INFORMATIONAL_MESSAGES
resolve_parallelism
""".split()

import multiprocessing as mp
import os
import sys

SHOW_INFORMATIONAL_MESSAGES = True


def resolve_parallelism(parallel):
    """Decide what level of parallelism to use.

    Parameters
    ----------
    parallel : integer or None
        The user's specification

    Returns
    -------
    A positive integer giving the parallelization level.

    """
    if parallel is None:
        if mp.get_start_method() == "fork":
            parallel = None

            # If we seem to be an HPC job, try to guess the number of CPUs based
            # on the job allocation of CPUs/cores, which might be much lower
            # than the number of CPUs on the system. Slurm sets many variables
            # related to this stuff; I *think* the one we're using here is the
            # most appropriate?

            slurm_alloc = os.environ.get("SLURM_NPROCS")
            if slurm_alloc:
                try:
                    parallel = int(slurm_alloc)
                except ValueError:
                    pass

            # If we're still not sure, go with the system CPU count

            if parallel is None:
                parallel = os.cpu_count()

            if SHOW_INFORMATIONAL_MESSAGES and parallel > 1:
                print(f"info: parallelizing processing over {parallel} CPUs")
        else:
            parallel = 1

    if parallel > 1 and mp.get_start_method() != "fork":
        print(
            """warning: parallel processing was requested but is not possible
    because this operating system is not using `fork`-based multiprocessing.
    On macOS a bug prevents forking: https://bugs.python.org/issue33725""",
            file=sys.stderr,
        )
        parallel = 1

    if parallel > 1:
        return parallel

    return 1
