# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utilatest

import tablero.path
import tests


@pytest.mark.parametrize('pdf', [
    pytest.param(power.BOOK007_PDF, id='book007'),
    pytest.param(power.HOME025_PDF, id='home025'),
    pytest.param(power.HOME040_PDF, id='home040'),
])
@utilatest.nightly
def test_table_extract_negative(pdf, testdir, monkeypatch):
    loaded = determine_tables(pdf, ':', testdir, monkeypatch)
    assert not loaded, str(loaded)


def test_master75page1718_notable(testdir, monkeypatch):
    source = power.MASTER075_PDF
    tables = determine_tables(source, '17,18', testdir, monkeypatch)
    assert not tables


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


def determine_tables(pdf, pages, testdir, monkeypatch, folder='notable'):
    utilatest.fixture_requires(pdf, folder=folder)
    source = power.link(pdf, folder=folder)
    tests.run(
        f'-i {source} -i {testdir.tmpdir} --table={pdf} --pages={pages}',
        monkeypatch=monkeypatch,
    )
    # load result
    tables = tablero.path.decide(testdir.tmpdir)
    loaded = serializeraw.load_tables(tables)
    loaded = [item for item in loaded if item.content]
    return loaded
