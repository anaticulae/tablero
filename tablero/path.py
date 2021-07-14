# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import tablero


def table(path: str, prefix: str = '') -> str:
    """Path to extraction result of tablero --table step.
    >>> table('/data/resources')
    '/data/resources/tablero__table_table.yaml'
    """
    return utila.pathconnector(path, tablero.PROCESS, 'table_table', prefix)


def figure(path: str, prefix: str = '') -> str:
    """Path to extraction result of tablero --figure step.
    >>> figure('/data/resources')
    '/data/resources/tablero__figure_figure.yaml'
    """
    return utila.pathconnector(path, tablero.PROCESS, 'figure_figure', prefix)
