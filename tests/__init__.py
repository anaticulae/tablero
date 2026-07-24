# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import hoverpower
import pytest
import serializeraw
import ughost
import utilotest

import tablero
import tablero.cli

ughost = pytest.mark.skipif(not ughost.HAS_GHOST, reason='require ughost')

run = functools.partial(  # pylint:disable=C0103
    utilotest.run_command,
    main=tablero.cli.main,
    process=tablero.PROCESS,
    expect=True,
)

failure = functools.partial(  # pylint:disable=C0103
    utilotest.run_command,
    main=tablero.cli.main,
    process=tablero.PROCESS,
    expect=False,
)


def run_tables(pdf, pages, td, mp):
    utilotest.fixture_requires(pdf)
    source = hoverpower.link(pdf)
    cmd = f'-i {source} --table={pdf} --pages={pages}'
    run(cmd, mp=mp)
    loaded = serializeraw.load_tables(td.tmpdir)
    return loaded
