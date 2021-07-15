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
import utilatest

import tablero.path
import tests


@utilatest.longrun
@utilatest.requires(power.BOOK007_PDF)
def test_table_extract_negative(testdir, monkeypatch):
    book = power.BOOK007_PDF
    # copy pdffile
    tests.copy_pdf(power.BOOK007_PDF, testdir.tmpdir)
    # run cli
    source = power.link(book)
    tests.run(f'-i {source} -i {testdir.tmpdir}', monkeypatch=monkeypatch)
    # load result
    tables = tablero.path.decide(testdir.tmpdir)
    loaded = serializeraw.load_tables(tables)
    loaded = [item for item in loaded if item.content]
    assert not loaded, str(loaded)
