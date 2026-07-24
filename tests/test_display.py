# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import serializeraw
import utilo
import utilotest

import tablero.display
import tablero.features
import tests


def tables(source):
    source = hoverpower.link(source)
    loaded = serializeraw.load_lines(source)
    grouped = tablero.features.word.locate_tables(loaded)
    result = tablero.features.word.judge_tables(grouped)
    return result


@tests.ughost
@utilotest.nightly
def test_display_tables_docu013():
    source = hoverpower.DOCU013_PDF
    data = tables(source)
    outdir = tablero.display.render_tables(data, source)
    assert utilo.file_count(outdir) == 11
