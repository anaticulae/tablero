# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Table Extraction Strategy: Crossed:
===================================

Detect tables which are build out of horizontal lines which are
connected due vertical lines.

Strategy:
    1. Add buckets with horizontal lines
    2. Iter thru vertical lines and add boundings in every hitted bucket
    3. Select connected buckets
    4. Connect small table fragments which are next and close to each other
"""

import operator
import statistics

import iamraw
import serializeraw
import utila

import tablero.lines
import tablero.utils


def work(lines: str, content: str, pages: tuple = None) -> str:
    # prepare data
    content = serializeraw.load_contentboundingbox(content, pages=pages)
    lines = serializeraw.load_lines(lines, pages=pages)
    lines = tablero.utils.limit_lines(lines, content)
    # run strategy
    result = run(lines)
    dumped = serializeraw.dump_tables(result)
    return dumped


@utila.profile('strategy:crossed')
def run(lines):
    result = []
    for page in lines:
        extracted = cluster_page(page.content)
        result.append(
            iamraw.PageContentTableBounding(
                page=page.page,
                content=extracted,
            ))
    # remove empty pages
    result = [item for item in result if item.content]
    return result


TABLE_ROW_HEIGHT_MEAN = 12.0
TABLE_COLUMN_COUNT_MAX = 10


def cluster_page(lines) -> iamraw.TableBoundings:
    horizontals = tablero.utils.determine_horizontals(lines)
    verticals = tablero.utils.determine_verticals(lines)
    result = extract_potential_table(verticals, horizontals)
    result = [
        iamraw.TableBounding(
            bounding=item,
            lines=tablero.utils.between(
                lines=verticals + horizontals,
                bounding=item,
            ),
        ) for item in result
    ]
    # exclude bounding box, which has two vertical lines
    result = [
        item for item in result
        if len(tablero.utils.determine_verticals(item.lines)) >= 3
    ]
    result = [
        item for item in result if tablero.lines.length_avg(item.lines) >=
        tablero.config.TABLE_MIN_AVG_LINE_LENGTH
    ]
    result = [
        item for item in result
        if table_row_height_mean(item.lines) > TABLE_ROW_HEIGHT_MEAN
    ]
    result = [
        item for item in result if column_count(item) <= TABLE_COLUMN_COUNT_MAX
    ]
    return result


def table_row_height_mean(lines) -> float:
    hori = tablero.utils.determine_horizontals(lines)
    hori = [item[1] for item in utila.sort_leftright_topdown(hori)]
    grouped = [item[0] for item in utila.groupby_diff(hori, maxdiff=5.0)]
    if len(grouped) < 2:
        return 0.0
    diff = utila.diffs(grouped)
    result = statistics.mean(diff)
    return result


def columns(lines):
    vertical = tablero.utils.determine_verticals(lines)
    vertical = [item[0] for item in utila.sort_leftright_topdown(vertical)]
    grouped = [item[0] for item in utila.groupby_diff(vertical, maxdiff=5)]
    return grouped


def column_count(lines):
    return len(columns(lines))


def extract_potential_table(verticals, horizontals):
    if not horizontals:
        utila.debug('skip crossed, no horizontals, extract_potential_table')
        return []
    buckets = utila.Buckets(
        horizontals,
        selector=operator.itemgetter(3),  # y1
    )
    for vertical in verticals:
        x0, top, x1, bottom = vertical
        for item in utila.ranges(top, bottom, 10):
            buckets.add((x0, item, x1, item))
    merged = [index if item else None for index, item in enumerate(buckets)]
    merged = utila.groupby_none(merged)
    # single line carnt build a table
    merged = [item for item in merged if len(item) > 1]
    tables = []
    for group in merged:
        topline = horizontals[group[0] - 1]
        # double content below table?
        bottomline = horizontals[min((group[-1], len(horizontals) - 1))]
        table = utila.rectangle_max((topline, bottomline))
        tables.append(table)
    tables = tablero.utils.merge_tables(tables)
    # merge overlapping table again
    # TODO: REMOVE AFTER FIXING
    tables = utila.intersecting_rectangle_cluster(tables)
    tables = [
        item[0] if len(item) == 1 else utila.rectangle_max(item)
        for item in tables
    ]
    return tables
