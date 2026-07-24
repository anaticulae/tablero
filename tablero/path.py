# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo

import tablero


def decide(path: str, prefix: str = '') -> str:
    """Path to extraction result of tablero --decide step.
    >>> decide('/data/resources')
    '/data/resources/tablero__decide_decide.yaml'
    """
    return utilo.pathconnector(path, tablero.PROCESS, 'decide_decide', prefix)


def figure(path: str, prefix: str = '') -> str:
    """Path to extraction result of tablero --figure step.
    >>> figure('/data/resources')
    '/data/resources/tablero__figure_figure.yaml'
    """
    return utilo.pathconnector(path, tablero.PROCESS, 'figure_figure', prefix)
