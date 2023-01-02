# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo
import iamraw
import serializeraw
import utila

import tablero.features.crossed
import tablero.judge
import tablero.lines
import tablero.utils

# a table must have at least this amount of lines
TABLE_LINE_COUNT_MIN = configo.HV_INT_PLUS(default=10)

# tables are build out of vertical and horizontal lines, but only a few
# cross lines.
TABLE_HORIZONTAL_VERTICAL_LINE_MIN = configo.HV_PERCENT_PLUS(default=90)


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


def judge_tables(grouped):
    """This approach handles only very simple word tables.

    Beautiful "latex" tables are not supported because there are build
    out of single horizontal lines.
    """
    result = []
    for page, clusters in grouped:
        pageresult = iamraw.PageContentTableBounding(page=page)
        for item in clusters:
            if not isvalid(item):
                continue
            item = list(item)
            table = iamraw.TableBounding(
                bounding=utila.rect_max(item),
                lines=item,
                page=page,
            )
            if not tablero.judge.isvalid(table):
                continue
            # convert cluster to list
            pageresult.append(table)
        result.append(pageresult)
    # remove empty pages
    result = [item for item in result if item.content]
    return result


def isvalid(cluster) -> bool:
    if len(cluster) < TABLE_LINE_COUNT_MIN:
        utila.debug(f'too few lines: {len(cluster)}')
        utila.debug(cluster)
        return False
    percentage = tablero.lines.horiverti_percentage(cluster)
    if percentage < TABLE_HORIZONTAL_VERTICAL_LINE_MIN:
        utila.debug(f'too few vertical lines: {percentage}')
        utila.debug(cluster)
        return False
    return True
