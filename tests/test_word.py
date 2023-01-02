# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import serializeraw
import utilatest

import tablero.features.word


@utilatest.requires(power.DOCU013_PDF)
def test_dump_and_load():
    source = power.link(power.DOCU013_PDF)
    loaded = serializeraw.load_lines(source, pages=(0, 1, 2))
    grouped = tablero.features.word.locate_tables(loaded)
    tables = tablero.features.word.judge_tables(grouped)
    # dump and load
    dumped = serializeraw.dump_tables(tables)
    loaded = serializeraw.load_tables(dumped)
    # VERIFY THAT CLUSTERING IS SOLVED BEFORE DUMPING DATA, IF ERROR OCCURS
    assert loaded == tables
