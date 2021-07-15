# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
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


def tables():
    source = iamraw.path.line(power.link(power.DOCU13_PDF))
    loaded = serializeraw.load_lines(source)
    grouped = tablero.features.word.locate_tables(loaded)
    result = tablero.features.word.judge_tables(grouped)
    return result


@utilatest.longrun
def test_display_tables(testdir):
    source = power.DOCU13_PDF
    data = tables()
    tablero.display.render_tables(data, source, testdir.tmpdir)
    assert utila.file_count(testdir.tmpdir) == 11


@utilatest.longrun
def test_ghost_small(testdir):
    source = power.DOCU13_PDF
    pages = (1, 2, 3)
    tablero.display.ghost_small(source, testdir.tmpdir, pages)
    assert utila.file_count(testdir.tmpdir) == 3
