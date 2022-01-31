# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import statistics

import configo
import utila

import tablero.config
import tablero.utils

# TODO: MAKE PAGE SIZE DEPENDENT?
TABLE_ROW_HEIGHT_MEAN = configo.HV_FLOAT_PLUS(default=12.0)

TABLE_COLUMN_COUNT_MAX = configo.HV_INT_PLUS(default=10)

TABLE_HEADER_HEIGHT_MAX = configo.HV_FLOAT_PLUS(default=65)


@utila.empty_replace(
    column_count_max=TABLE_COLUMN_COUNT_MAX,
    header_height_max=TABLE_HEADER_HEIGHT_MAX,
    line_length_avg_min=tablero.config.TABLE_LINE_LENGTH_AVG_MIN,
    row_height_mean_min=TABLE_ROW_HEIGHT_MEAN,
)
def isvalid(
    table,
    *,
    verticals_count_min: int = 3,
    column_count_max: int = utila.EMPTY,
    header_height_max: float = utila.EMPTY,
    line_length_avg_min: float = utila.EMPTY,
    row_height_mean_min: float = utila.EMPTY,
) -> bool:
    lines = table.lines
    # exclude bounding box, which has two vertical lines
    if len(tablero.utils.determine_verticals(lines)) < verticals_count_min:
        utila.debug(f'no enough lines: {table}')
        utila.debug(table)
        return False
    if tablero.lines.length_avg(lines) < line_length_avg_min:
        utila.debug(f'line length avg small: {tablero.lines.length_avg(lines)}')
        utila.debug(table)
        return False
    if table_row_height_mean(lines) < row_height_mean_min:
        utila.debug(f'row height too small: {table_row_height_mean(lines)}')
        utila.debug(table)
        return False
    if column_count(table) > column_count_max:
        utila.debug(f'too many columns: {column_count(table)}')
        utila.debug(table)
        return False
    if table_header_height(table) > header_height_max:
        utila.debug(f'header too height: {table_header_height(table)}')
        utila.debug(table)
        return False
    return True


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


def table_header_height(lines) -> float:
    hori = tablero.utils.determine_horizontals(lines)
    hori = [item[1] for item in utila.sort_leftright_topdown(hori)]
    grouped = [item[0] for item in utila.groupby_diff(hori, maxdiff=5.0)]
    if len(grouped) < 2:
        return 0.0
    diff = utila.diffs(grouped)
    return diff[0]
