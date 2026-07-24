# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import serializeraw
import utilo
import utilotest

import tests


@utilotest.nightly
def test_master75page1718_notable(td, mp):
    source = hoverpower.MASTER075_PDF
    tables = determine_tables(source, '17,18', td, mp)
    assert not tables


@utilotest.nightly
def test_master110page9092(td, mp):
    source = hoverpower.MASTER110_PDF
    tables = determine_tables(
        source,
        '29,90,92,94',
        td,
        mp,
        folder=None,
    )
    assert not tables


@utilotest.longrun
def test_diss205p135p138p140(td, mp):
    source = hoverpower.DISS205_PDF
    tables = determine_tables(
        source,
        '135,138,140',
        td,
        mp,
        folder=None,
    )
    assert not tables


def determine_tables(pdf, pages, td, mp, folder='notable'):
    utilotest.fixture_requires(pdf, folder=folder)
    source = hoverpower.link(pdf, folder=folder)
    tests.run(
        f'-i {source} -i {td.tmpdir} --table={pdf} --pages={pages}',
        mp=mp,
    )
    # load result
    loaded = serializeraw.load_tables(td.tmpdir)
    loaded = utilo.flatten_content(loaded)
    return loaded
