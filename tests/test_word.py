# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import pytest
import serializeraw
import utilatest

import tablero.features.word


@pytest.mark.xfail(reason='improve word parser')
@utilatest.requires(power.DOCU013_PDF)
def test_dump_and_load():
    source = iamraw.path.line(power.link(power.DOCU013_PDF))
    loaded = serializeraw.load_lines(source, pages=(0, 1, 2))
    grouped = tablero.features.word.locate_tables(loaded)
    tables = tablero.features.word.judge_tables(grouped)

    dumped = serializeraw.dump_tables(tables)
    loaded = serializeraw.load_tables(dumped)
    assert loaded == tables
