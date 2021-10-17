# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import serializeraw
import utila

import tablero.features.crossed
import tablero.lines
import tablero.utils

# a table must have at least this amount of lines
TABLE_MIN_LINE_COUNT = configo.HV_INT_PLUS(default=10)

# tables are build out of vertical and horizontal lines, but only a few
# cross lines.
TABLE_MIN_HORIZONTAL_VERTICAL_LINE = configo.HV_PERCENT_PLUS(default=90)


def work(lines: str, content: str, pages: tuple = None) -> str:
    # content
    content = serializeraw.load_contentboundingbox(content, pages=pages)
    # prepare data
    lines = serializeraw.load_lines(lines, pages=pages)
    lines = tablero.utils.limit_lines(lines, contentbox=content)
    # run strategy
    result = run(lines)
    dumped = serializeraw.dump_tables(result)
    return dumped


@utila.profile('strategy:word')
def run(lines):
    grouped = locate_tables(lines)
    result = judge_tables(grouped)
    return result


def locate_tables(lines):
    result = []
    for page in lines:
        content = page.content
        # TODO: profile only on --profile
        # with utila.profile():
        clustered = utila.intersecting_line_cluster(
            content,
            max_diff=5.0,
            min_elements=3,
        )
        # convert cluster to list
        clustered = list(clustered)
        result.append((page.page, clustered))
    return result


TABLE_ROW_HEIGHT_MEAN = 12.0
TABLE_COLUMN_COUNT_MAX = 10
TABLE_HEADER_HEIGHT_MAX = 45


def judge_tables(grouped):
    """This approach handles only very simple word tables, beautiful
    "latex" tables are not supported because there are build out of
    single horizontal lines."""
    result = []
    for page, clusters in grouped:
        pageresult = iamraw.PageContentTableBounding(page=page)
        for item in clusters:
            if len(item) < TABLE_MIN_LINE_COUNT:
                continue
            percentage = tablero.lines.horiverti_percentage(item)
            if percentage < TABLE_MIN_HORIZONTAL_VERTICAL_LINE:
                continue
            avg = tablero.lines.length_avg(item)
            if avg < tablero.config.TABLE_MIN_AVG_LINE_LENGTH:
                continue
            rowheight_mean = tablero.features.crossed.table_row_height_mean(item)  # yapf:disable
            if rowheight_mean < TABLE_ROW_HEIGHT_MEAN:
                continue
            column_count = tablero.features.crossed.column_count(item)
            if column_count > TABLE_COLUMN_COUNT_MAX:
                continue
            header_height = table_header_height(item)
            if header_height > TABLE_HEADER_HEIGHT_MAX:
                continue
            bounding = utila.rectangle_max(item)
            # convert cluster to list
            pageresult.append(
                iamraw.TableBounding(
                    bounding=bounding,
                    lines=item,
                ))
        result.append(pageresult)
    # remove empty pages
    result = [item for item in result if item.content]
    return result


def table_header_height(lines) -> float:
    hori = tablero.utils.determine_horizontals(lines)
    hori = [item[1] for item in utila.sort_leftright_topdown(hori)]
    grouped = [item[0] for item in utila.groupby_diff(hori, maxdiff=5.0)]
    if len(grouped) < 2:
        return 0.0
    diff = utila.diffs(grouped)
    return diff[0]
