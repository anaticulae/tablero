# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utila
import utilatest

import tablero.camelox.fork
import tablero.features.camelox


def test_camelot_run():
    source = power.DOCU13_PDF
    parsed = tablero.features.camelox.run(source, pages=2)
    assert len(parsed) == 1


@utilatest.nightly
def test_camelot_forked(testdir):
    source = power.DOCU13_PDF
    content = power.link(source)
    parsed = tablero.camelox.fork.run(source, content=content, worker=4)
    flatten = utila.flatten_content(parsed)
    # The purpose of this test is to run in forked mode, not to check the
    # correct result.
    assert 20 <= len(flatten) <= 40


def test_camelot_latex():
    source = power.BACHELOR090_PDF
    parsed = tablero.features.camelox.run(source, pages=76)
    assert len(parsed) == 1
