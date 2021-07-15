# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import operator

import iamraw
import serializeraw
import utila

import tablero.lines
import tablero.utils


def work(
    text: str,
    textposition: str,
    sizeandborder: str,
    headerfooter: str,
    lines: str,
    pages: tuple = None,
) -> str:
    lines = serializeraw.load_lines(lines, pages=pages)
    lines = tablero.utils.limit_lines(lines)
    navigators = serializeraw.create_pagetextcontentnavigators_fromfile(
        text,
        textposition,
        sizeandborderpath=sizeandborder,
        headerfooterpath=headerfooter,
        pages=pages,
    )
    lines = contentlines(lines, navigators)
    # run strategy
    result = run(lines, navigators)
    dumped = serializeraw.dump_tables(result)
    return dumped


@utila.profile('strategy:horizontal')
def run(lines, navigators):
    todo = []
    for navigator in navigators:
        pagelines = utila.select_page(lines, page=navigator.page)
        if pagelines:
            todo.append(
                functools.partial(
                    cluster_page,
                    navigator,
                    pagelines.content,
                ))
        else:
            todo.append(functools.partial(done))
    extracted = utila.fork(*todo, worker=10, process=True)
    result = [
        iamraw.PageContentTableBounding(
            page=navigator.page,
            content=content,
        ) for content, navigator in zip(extracted, navigators)
    ]
    # remove empty pages
    result = [item for item in result if item.content]
    return result


def contentlines(lines, navigators) -> list:
    result = []
    for lino, navi in utila.sync_pages((lines, navigators), numbers=False):
        if not lino:
            continue
        top, bottom = navi.content.top, navi.content.bottom
        # y0 is inside pagetextcontentnavigator
        line = [
            item for item in lino.content
            if utila.isinside(item[1], top, bottom) and
            utila.isinside(item[3], top, bottom)
        ]
        result.append(iamraw.PageContentLine(page=navi.page, content=line))
    return result


def done():
    return []


def cluster_page(navigator, lines) -> iamraw.TableBoundings:
    horizontals = [
        item for item in lines if tablero.lines.horizontal(
            item,
            maxdiff=tablero.config.TABLE_HORIZONTAL_MAX_DIFF,
        )
    ]
    if len(horizontals) <= 2:
        # TODO: SINGLE LINE TABLE?
        return []
    boundings = [item.bounding for item in navigator]
    boundings = utila.sort_leftright_topdown(boundings)
    result = []
    grouped_horizontals = tablero.utils.group_horizontals(horizontals)
    for group in grouped_horizontals:
        if len(group) <= 1:
            continue
        double_table = extract_potential_table(
            boundings,
            group,
            min_elements=2,
        )
        single_table = extract_potential_table(
            boundings,
            group,
            min_elements=1,
        )
        tables = double_table
        if len(single_table) > len(double_table):
            tables = single_table
        tables = [
            # judge tables
            item
            for item in tables
            if tablero.utils.valid_table(item, navigator)
        ]
        # merge connected tables
        tables = tablero.utils.merge_tables(tables)
        result.extend(tables)
    # TODO: ADD LINES
    result = [iamraw.TableBounding(bounding=item) for item in result]
    return result


def extract_potential_table(boundings, horizontals, min_elements=2):
    clustered = utila.same_line_cluster(
        boundings,
        min_elements=min_elements,
    )

    if not clustered:
        return []

    singles = [item for item in clustered if len(item) == 1]
    singlequote = len(singles) / len(boundings)

    if singlequote > 0.4:  # TODO: HOLY VALUE
        return []

    buckets = utila.Buckets(
        horizontals,
        selector=operator.itemgetter(3),  # y1
    )
    for cluster in clustered:
        for item in cluster:
            buckets.add(item)

    merged = [index if item else None for index, item in enumerate(buckets)]
    merged = utila.groupby_none(merged)

    tables = []
    for group in merged:
        if len(group) < 2:
            # TODO: MULTIPLE ITEMS IN ONLY ONE GROUP BETWEEN HORIZONTAL LINES
            continue
        topline = horizontals[group[0]]
        # double content below table?
        bottomline = horizontals[min((group[-1], len(horizontals) - 1))]
        table = utila.rectangle_max((topline, bottomline))
        tables.append(table)
    return tables
