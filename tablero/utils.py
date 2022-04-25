# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import math

import configo
import elements
import iamraw
import texmex
import utila

import tablero.config
import tablero.lines

LINES_PER_PAGE_MAX = 1000

GROUP_HORIZONTALS_XDIFF_MAX = configo.HV_FLOAT_PLUS(default=30.0)


def limit_lines(lines, contentbox=None, line_length_min: float = 10.0):
    # TODO: DISABLE AFTER HAVING BETTER CLUSTER STRATEGY
    if contentbox:
        contentbox = {
            item.page: (-1024, item.top, 1024 * 2, item.bottom)
            for item in contentbox
        }
    result = []
    for page in lines:
        content = page.content
        if len(page.content) > LINES_PER_PAGE_MAX:
            # too many lines on this page
            content = []
        content = [
            item for item in content if utila.length(*item) > line_length_min
        ]
        if contentbox:
            content = [
                item for item in content
                if utila.rectangle_inside(contentbox[page.page], item)
            ]
        result.append(iamraw.PageContentLine(page=page.page, content=content))
    return result


def valid_table(bounding, navigator: texmex.PageTextContentNavigator) -> bool:
    top, bottom = bounding[1], bounding[3]
    utila.debug(f'validate table: {bounding} on page {navigator.page}')
    height = utila.roundme(bottom - top)
    if height < tablero.config.TABLE_HEIGHT_MIN:
        # remove to small tables
        utila.debug(f'table on page: {navigator.page} too small: {height}')
        return False
    table_content = navigator.between(
        top / navigator.pagesize[1],
        bottom / navigator.pagesize[1],
    )
    if not table_content:
        # no content in table
        utila.debug('no table content')
        return False
    if peace_of_code(table_content):
        # do not detect peace of code as table
        return False
    # table seems to be valid
    return True


def peace_of_code(table_content) -> bool:
    start = table_content[0:3]
    if any(elements.iscaption_code(item.text) for item in start):
        return True
    end = table_content[-3:0]
    if any(elements.iscaption_code(item.text) for item in end):
        return True
    return False


def merge_tables(boundings):
    if not boundings:
        return []
    result = [boundings[0]]
    for bounding in boundings[1:]:
        tabledistance = utila.roundme(math.fabs(result[-1][3] - bounding[1]))
        utila.debug(tabledistance)
        if tabledistance < tablero.config.TABLE_MERGE_DISTANCE:
            result[-1] = utila.rectangle_max((result[-1], bounding))
        else:
            result.append(bounding)
    return result


def group_horizontals(items, xdiff: float = GROUP_HORIZONTALS_XDIFF_MAX):
    """\
    >>> group_horizontals([(100, 50, 500, 50),
    ...                    (98, 150, 510, 150),
    ...                    (50, 200, 205, 200),
    ...                    (50, 250, 195, 250)])
    [[(100, 50, 500, 50), (98, 150, 510, 150)], [(50, 200, 205, 200), (50, 250, 195, 250)]]
    """
    if not items:
        return []
    result = [[items[0]]]
    for item in items[1:]:
        x0, _, x1, __ = result[-1][-1]
        x00, _, x11, __ = item
        if utila.near(x0, x00, xdiff) and utila.near(x1, x11, xdiff):
            result[-1].append(item)
        else:
            result.append([item])
    return result


def between(lines, bounding):
    result = [
        item for item in lines
        if bounding[1] <= item[1] <= item[3] <= bounding[3]
    ]
    return result


def determine_verticals(lines):
    result = [
        item for item in lines if tablero.lines.vertical(
            item,
            maxdiff=tablero.config.TABLE_VERTICAL_DIFF_MAX,
        )
    ]
    return result


def determine_horizontals(lines):
    result = [
        item for item in lines if tablero.lines.horizontal(
            item,
            maxdiff=tablero.config.TABLE_HORIZONTAL_DIFF_MAX,
        )
    ]
    return result
