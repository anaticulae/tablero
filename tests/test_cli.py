# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import power
import utila
import utilatest

import tests


def test_tablero_cli_help(monkeypatch):
    """Run help and version and format command to reach basic test coverage."""
    tests.run('--help', monkeypatch=monkeypatch)


@utilatest.longrun
@utilatest.requires(power.BOOK007_PDF)
def test_tablero_cli_run(testdir, monkeypatch):
    """Run tabelero with all steps."""
    utila.file_copy(power.BOOK007_PDF, os.path.join(testdir.tmpdir, 'table'))
    source = power.link(power.BOOK007_PDF)
    tests.run(f'-i {source} -i {testdir.tmpdir} -j8', monkeypatch=monkeypatch)
