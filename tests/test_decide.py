# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utila
import utilatest

import tablero.display
import tablero.path
import tablero.utils
import tests


@pytest.mark.parametrize('source, pages, expected', [
    pytest.param(
        power.BACHELOR090_PDF,
        '75:80',
        [1, 3, 3, 3],
        id='bachelor90',
    ),
    pytest.param(
        power.DOCU013_PDF,
        '2:7',
        [1, 3, 3, 5, 2],
        id='vimguide',
    ),
    pytest.param(
        power.DOCU013_PDF,
        '5',
        [5],
        id='vimguide_page5',
    ),
    pytest.param(
        power.BACHELOR056_PDF,
        '15,18',
        [1, 1],
        id='bachelor56_page15',
    ),
    pytest.param(
        power.BACHELOR056_PDF,
        '31',
        [2],
        id='bachelor56_page31',
    ),
    pytest.param(
        power.DOCU007_PDF,
        '0,1,2',
        [],
        id='notable_howto_pyporting',
    ),
    pytest.param(
        power.BACHELOR063_PDF,
        '25',
        [1],
        id='bachelor63_singletable',
    ),
    pytest.param(
        power.ORDER050_PDF,
        ':',
        [1],
        id='order50',
    ),
])
@utilatest.nightly
def test_detect_table_single(source, pages, expected, testdir, monkeypatch):
    utilatest.fixture_requires(source)
    pdf = source
    source = power.link(source)
    with monkeypatch.context() as context:
        # TODO: REMOVE AFTER UPGRADING CLUSTER STRATEGY
        context.setattr(tablero.utils, 'LINES_PER_PAGE_MAX', 180)
        tests.run(
            f'-i {source} -i {testdir.tmpdir} --table={pdf} --pages={pages}',
            monkeypatch=monkeypatch,
        )
    tables = tablero.path.decide(testdir.tmpdir)
    loaded = serializeraw.load_tables(tables)
    current = [len(item) for item in loaded]
    assert current == expected


@utilatest.requires(power.BACHELOR090_PDF)
def test_detect_table_bachelor90_page80(testdir, monkeypatch):
    """The table header contains only one connected textual string."""
    pdf = power.BACHELOR090_PDF
    source = power.link(pdf)
    pages = '80'
    tests.run(
        f'-i {source} --table={pdf} --pages={pages}',
        monkeypatch=monkeypatch,
    )
    tables = tablero.path.decide(testdir.tmpdir)
    loaded = serializeraw.load_tables(tables)[0].content
    assert len(loaded) == 1


@utilatest.nightly
@utilatest.requires(power.MASTER098_PDF)
def test_detect_table_master98_page54_60(testdir, monkeypatch):
    pdf = power.MASTER098_PDF
    source = power.link(pdf)
    pages = '54:62'
    tests.run(
        f'-i {source} --table={pdf} --pages={pages}',
        monkeypatch=monkeypatch,
    )
    tables = tablero.path.decide(testdir.tmpdir)
    loaded = serializeraw.load_tables(tables)
    # verify extracted tables
    assert len(utila.select_content(loaded, 54)) == 1
    assert len(utila.select_content(loaded, 55)) == 1
    assert len(utila.select_content(loaded, 58)) == 1
    assert len(utila.select_content(loaded, 59)) == 1


@utilatest.nightly
@utilatest.requires(power.BACHELOR056_PDF)
def test_detect_table_bachelor56(testdir, monkeypatch):
    pdf = power.BACHELOR056_PDF
    source = power.link(pdf)
    tests.run(
        f'-i {source} --table={pdf}',
        monkeypatch=monkeypatch,
    )
    loaded = serializeraw.load_tables(tablero.path.decide(testdir.tmpdir))
    tablero.display.render_tables(loaded, pdf)
    tables = utila.flatten_content(loaded)
    # 6 includes 1 figure which can be detected as table
    assert len(tables) in (5, 6)  # VALIDATED


@pytest.mark.timeout(30)
@utilatest.requires(power.MASTER112_PDF)
def test_master112_bachelor_timeout(testdir, monkeypatch):
    source = power.link(power.MASTER112_PDF)
    cmd = f'-i {source} --table={power.MASTER112_PDF} --pages=110'
    tests.run(cmd, monkeypatch=monkeypatch)
