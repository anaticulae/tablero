# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import serializeraw
import utila
import utilatest

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
        id='docu013',
    ),
    pytest.param(
        power.DOCU013_PDF,
        '5',
        [5],
        id='docu013p5',
    ),
    pytest.param(
        power.BACHELOR056_PDF,
        '15,18',
        [1],
        id='bachelor56p15',
    ),
    pytest.param(
        power.BACHELOR056_PDF,
        '31',
        [2],
        id='bachelor56p31',
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
    pytest.param(
        power.MASTER099_PDF,
        '11,48,49',
        [1, 1, 1],
        id='master099p48p49',
    ),
])
@tests.ghost
@utilatest.nightly
def test_detect_table_single(source, pages, expected, td, mp):
    """\
    # bachelor56page18: figure is not detected as table anymore.
    """
    utilatest.fixture_requires(source)
    pdf = source
    source = power.link(source)
    with mp.context() as context:
        # TODO: REMOVE AFTER UPGRADING CLUSTER STRATEGY
        context.setattr(tablero.utils, 'LINES_PER_PAGE_MAX', 180)
        tests.run(
            f'-i {source} -i {td.tmpdir} --table={pdf} --pages={pages}',
            mp=mp,
        )
    tables = tablero.path.decide(td.tmpdir)
    loaded = serializeraw.load_tables(tables)
    current = [len(item) for item in loaded]
    assert current == expected


@pytest.mark.xfail(reason='table is too small')
@utilatest.longrun
def test_bachelor56p31(td, mp):
    loaded = tests.run_tables(power.BACHELOR056_PDF, '31', td, mp)
    loaded = utila.flatten_content(loaded)
    loaded = sorted([item.bounding for item in loaded])
    expected = [
        (64.58, 97.6, 410.78, 162.15),
        (65.33, 550.78, 524.93, 694.58),
    ]
    assert utila.nears(loaded[0], expected[0])
    assert utila.nears(loaded[1], expected[1])
    assert 0
    loaded = tests.run_tables(power.BACHELOR056_PDF, '31', td, mp)


@utilatest.longrun
@utilatest.requires(power.BACHELOR090_PDF)
def test_detect_table_bachelor90p80(td, mp):
    """The table header contains only one connected textual string."""
    pdf = power.BACHELOR090_PDF
    source = power.link(pdf)
    pages = '80'
    tests.run(
        f'-i {source} --table={pdf} --pages={pages}',
        mp=mp,
    )
    tables = tablero.path.decide(td.tmpdir)
    loaded = serializeraw.load_tables(tables)[0].content
    assert len(loaded) == 1


@utilatest.nightly
@utilatest.requires(power.MASTER098_PDF)
def test_detect_table_master98p54_60(td, mp):
    loaded = tests.run_tables(power.MASTER098_PDF, '54:62', td, mp)
    # verify extracted tables
    assert len(utila.select_content(loaded, 54)) == 1
    assert len(utila.select_content(loaded, 55)) == 1
    assert len(utila.select_content(loaded, 58)) == 1
    assert len(utila.select_content(loaded, 59)) == 1


@utilatest.nightly
@utilatest.requires(power.BACHELOR056_PDF)
def test_detect_table_bachelor56(td, mp):
    loaded = tests.run_tables(power.BACHELOR056_PDF, ':', td, mp)
    tables = utila.flatten_content(loaded)
    # 6 includes 1 figure which can be detected as table
    assert len(tables) in {5, 6}  # VALIDATED


@pytest.mark.timeout(30)
@utilatest.longrun
@utilatest.requires(power.MASTER112_PDF)
def test_master112_bachelor_timeout(td, mp):
    tests.run_tables(power.MASTER112_PDF, '110', td, mp)


@utilatest.longrun
def test_bachelor51page29(td, mp):
    loaded = tests.run_tables(power.BACHELOR051_PDF, '29', td, mp)
    page29content = utila.select_page(loaded, page=29).content
    assert len(page29content) == 1
    assert page29content[0].bounding == (81.84, 645.6, 513.6, 697.92)


@utilatest.longrun
def test_bachelor51page30(td, mp):
    loaded = tests.run_tables(power.BACHELOR051_PDF, '30', td, mp)
    page30content = utila.select_page(loaded, page=30).content
    assert len(page30content) == 1
    expected = (81.84, 647.88, 513.6, 700.32)
    assert page30content[0].bounding == expected
