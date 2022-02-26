# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import pytest
import serializeraw
import utilatest

import tablero.display
import tablero.features.horizontal


def extract_tables(source, page):
    ptn = serializeraw.create_pagetextnavigators_frompath(
        source,
        pages=(page,),
    )[0]
    lines = serializeraw.load_lines(
        iamraw.path.line(source),
        pages=(page,),
    )
    lines = lines[0].content
    tables = tablero.features.horizontal.cluster_page(ptn, lines)
    return tables


@utilatest.requires(power.BACHELOR090_PDF)
def test_bachelor90p76_extract_table():
    source = power.link(power.BACHELOR090_PDF)
    page = 76
    tables = extract_tables(source, page)
    assert len(tables) == 1


@utilatest.requires(power.BACHELOR090_PDF)
def test_bachelor90p77_extract_table(testdir):
    source = power.link(power.BACHELOR090_PDF)
    page = 77
    tables = extract_tables(source, page)
    assert len(tables) == 3
    tables = [iamraw.PageContentTableBounding(page=page, content=tables)]
    tablero.display.render_tables(tables, power.BACHELOR090_PDF)


@pytest.mark.parametrize(
    'text, line, bounding',
    [
        ((0, 15), (0, 5), (203.96, 114.83, 388.33, 214.1)),
        ((14, 28), (4, 7), (213.93, 295.89, 378.36, 394.89)),
        ((28, -1), (7, -1), (173.43, 561.47, 418.86, 631.58)),
    ],
)
@utilatest.requires(power.BACHELOR090_PDF)
def test_bachelor90p77_first_table(text, line, bounding):
    source = power.link(power.BACHELOR090_PDF)
    page = 77
    ptn = serializeraw.create_pagetextnavigators_frompath(
        source,
        pages=(page,),
    )[0]
    # shrink navigator data which belongs to the first table
    ptn.data = ptn.data[text[0]:text[1]]
    lines = serializeraw.load_lines(
        iamraw.path.line(source),
        pages=(page,),
    )
    lines = lines[0]
    lines = lines.content[line[0]:line[1]]
    tables = tablero.features.horizontal.cluster_page(ptn, lines)
    tables_bounding = [table.bounding for table in tables]
    assert tables_bounding == [bounding]
    tables = [iamraw.PageContentTableBounding(page=page, content=tables)]
    tablero.display.render_tables(tables, power.BACHELOR090_PDF)
