# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import configo
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
    content: str,
    pages: tuple = None,
) -> str:
    content = serializeraw.load_contentboundingbox(content, pages=pages)
    lines = serializeraw.load_lines(lines, pages=pages)
    lines = tablero.utils.limit_lines(lines, contentbox=content)
    navigators = serializeraw.ptcn_fromfile(
        text,
        textposition,
        sizeandborder=sizeandborder,
        headerfooter=headerfooter,
        pages=pages,
    )
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


def done():
    return []


LINE_COUNT_MAX = configo.HV_INT_PLUS(default=15)


def cluster_page(navigator, lines) -> iamraw.TableBoundings:
    """\
    1. Group horizontals by x-displacement
    """
    horizontals = [
        item for item in lines if tablero.lines.horizontal(
            item,
            maxdiff=tablero.config.TABLE_HORIZONTAL_DIFF_MAX,
        )
    ]
    if len(horizontals) <= 2:
        # TODO: SINGLE LINE TABLE?
        return []
    boundings = [item.bounding for item in navigator]
    boundings = utila.sort_leftright_topdown(boundings)
    grouped_horizontals = tablero.utils.group_horizontals(horizontals, xdiff=5)
    result = []
    for group in grouped_horizontals:
        if len(group) <= 1:
            continue
        if len(group) > LINE_COUNT_MAX:
            # this group can not be a table, latex tables have only few
            # lines.
            continue
        double_table = extract_potential_table(
            boundings,
            group,
            navigator=navigator,
            min_elements=2,
        )
        single_table = extract_potential_table(
            boundings,
            group,
            navigator=navigator,
            min_elements=1,
        )
        tables = double_table
        if len(single_table) >= len(double_table):
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


def extract_potential_table(
    boundings,
    horizontals,
    min_elements=2,
    navigator=None,
):
    boundings = inside_horizontals(boundings, horizontals)
    # TODO: singlequote is not possible for min_elements more than one
    groups = boundings_to_buckets(boundings, horizontals, min_elements)
    if not groups:
        return []
    # singles = [item for item in clustered if len(item) == 1]
    # singlequote = len(singles) / len(boundings)
    # if singlequote > 0.4:  # TODO: HOLY VALUE
    #     return []
    tables = []
    for group in groups:
        if len(group) < 2:
            # TODO: MULTIPLE ITEMS IN ONLY ONE GROUP BETWEEN HORIZONTAL LINES
            # table requires a least 3 horizontal lines
            continue
        bottom_horizontal_index = group[-1] + 1
        # +1 to include horizontal cause of python indexing
        group_horizontals = horizontals[group[0]:bottom_horizontal_index + 1]
        if not valid_distances(group_horizontals):
            continue
        header = set(inside_horizontals(boundings, group_horizontals[0:2]))
        header = [item for item in navigator if item.bounding in header]
        if not valid_header(header):
            continue
        topline = group_horizontals[0]
        # content below last horizontal raises out of IndexError in
        # `horizontals`.
        bottomline = group_horizontals[-1]
        tablebounding = utila.rectangle_max((topline, bottomline))
        tables.append(tablebounding)
    return tables


def inside_horizontals(boundings, horizontals) -> list:
    # determine most left and right x-coordinate of potential table
    inside_table = tuple(utila.rectangle_max(horizontals))
    boundings = [
        rectangle for rectangle in boundings if utila.dot_in_rectangle(
            inside_table,
            utila.rectangle_center(rectangle),
        )
    ]
    return boundings


def boundings_to_buckets(boundings, horizontals, min_elements):
    # cluster potential table elements on the same line
    clustered = utila.same_line_cluster(
        boundings,
        min_elements=min_elements,
    )
    if not clustered:
        return []
    buckets = utila.Buckets(
        horizontals,
        selector=lambda bounding: (bounding[1] + bounding[3]) / 2,
    )
    for cluster in clustered:
        for item in cluster:
            buckets.add(item)
    # remove content before and after horizontals which are not part of
    # the table.
    buckets = buckets[1:-1]
    merged = [
        index if rectangle else None
        for index, rectangle in enumerate(buckets, start=0)
    ]
    merged = utila.groupby_none(merged)
    return merged


HEADER_HEIGHT_MAX = configo.HV_FLOAT_PLUS(default=50.0)


def valid_distances(horizontals) -> bool:
    if len(horizontals) < 3:
        return True
    headerheight = horizontals[1][1] - horizontals[0][1]
    if headerheight > HEADER_HEIGHT_MAX:
        utila.debug(f'header too hight: {headerheight}')
        utila.debug(horizontals)
        return False
    return True


HEADER_WIDTH_MIN = configo.HV_FLOAT_PLUS(default=100.0)


def valid_header(content) -> bool:
    boundings = [item.bounding for item in content]
    left = min([item[0] for item in boundings])
    right = max([item[2] for item in boundings])
    width = right - left
    if width < HEADER_WIDTH_MIN:
        return False
    return True
