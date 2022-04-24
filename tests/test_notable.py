# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utila
import utilatest

import tests


@utilatest.nightly
def test_master75page1718_notable(testdir, monkeypatch):
    source = power.MASTER075_PDF
    tables = determine_tables(source, '17,18', testdir, monkeypatch)
    assert not tables


@utilatest.nightly
def test_master110page9092(testdir, monkeypatch):
    source = power.MASTER110_PDF
    tables = determine_tables(
        source,
        '29,90,92,94',
        testdir,
        monkeypatch,
        folder=None,
    )
    assert not tables


def test_diss205p135p138p140(testdir, monkeypatch):
    source = power.DISS205_PDF
    tables = determine_tables(
        source,
        '135,138,140',
        testdir,
        monkeypatch,
        folder=None,
    )
    assert not tables


def determine_tables(pdf, pages, testdir, monkeypatch, folder='notable'):
    utilatest.fixture_requires(pdf, folder=folder)
    source = power.link(pdf, folder=folder)
    tests.run(
        f'-i {source} -i {testdir.tmpdir} --table={pdf} --pages={pages}',
        monkeypatch=monkeypatch,
    )
    # load result
    loaded = serializeraw.load_tables(testdir.tmpdir)
    loaded = utila.flatten_content(loaded)
    return loaded
