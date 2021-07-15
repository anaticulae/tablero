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

import tablero.cluster
import tablero.lines

# a table must have at least this amount of lines
TABLE_MIN_LINE_COUNT = configo.HV_INT_PLUS(10)

# tables are build out of vertical and horizontal lines, but only a few
# cross lines.
TABLE_MIN_HORIZONTAL_VERTICAL_LINE = configo.HV_PERCENT_PLUS(0.9)


def work(lines: str, pages: tuple = None) -> str:
    # prepare data
    lines = serializeraw.load_lines(lines, pages=pages)
    lines = tablero.utils.limit_lines(lines)
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
        clustered = tablero.cluster.run(content)
        result.append((page.page, clustered))
    return result


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
            bounding = utila.rectangle_max(item)
            # convert cluster to list
            item = list(item)
            pageresult.append(
                iamraw.TableBounding(
                    bounding=bounding,
                    lines=item,
                ))
        result.append(pageresult)
    # remove empty pages
    result = [item for item in result if item.content]
    return result
