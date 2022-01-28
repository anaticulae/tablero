# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import power
import serializeraw
import utila
import utilatest

import tablero.display
import tablero.features


def tables(source):
    source = iamraw.path.line(power.link(source))
    loaded = serializeraw.load_lines(source)
    grouped = tablero.features.word.locate_tables(loaded)
    result = tablero.features.word.judge_tables(grouped)
    return result


@utilatest.nightly
def test_display_tables_docu013():
    source = power.DOCU013_PDF
    data = tables(source)
    outdir = tablero.display.render_tables(data, source)
    assert utila.file_count(outdir) == 11
