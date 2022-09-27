# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import ghost
import power
import pytest
import serializeraw
import utilatest

import tablero
import tablero.cli

ghost = pytest.mark.skipif(not ghost.HAS_GHOST, reason='require ghost')

run = functools.partial(  # pylint:disable=C0103
    utilatest.run_command,
    main=tablero.cli.main,
    process=tablero.PROCESS,
    success=True,
)

failure = functools.partial(  # pylint:disable=C0103
    utilatest.run_command,
    main=tablero.cli.main,
    process=tablero.PROCESS,
    success=False,
)


def run_tables(pdf, pages, td, mp):
    utilatest.fixture_requires(pdf)
    source = power.link(pdf)
    cmd = f'-i {source} --table={pdf} --pages={pages}'
    run(cmd, mp=mp)
    loaded = serializeraw.load_tables(td.tmpdir)
    return loaded
