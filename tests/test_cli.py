# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utila
import utilatest

import tests


def test_cli_help(monkeypatch):
    """Run help and version and format command to reach basic test coverage."""
    tests.run('--help', monkeypatch=monkeypatch)


@utilatest.nightly
@utilatest.requires(power.BOOK007_PDF)
def test_cli_run(testdir, monkeypatch):
    """Run tabelero with all steps."""
    source = power.link(power.BOOK007_PDF)
    tests.run(
        f'-i {source} -i {testdir.tmpdir} --table={power.BOOK007_PDF} -j8',
        monkeypatch=monkeypatch,
    )


@utilatest.longrun
@utilatest.requires(power.BACHELOR109_PDF)
def test_cli_internal_error(testdir, monkeypatch):
    """Run tablero with unsupported camelot file."""
    pdf = power.BACHELOR109_PDF
    source = power.link(pdf)
    completed = tests.run(
        f'-i {source} -i {testdir.tmpdir} --table={pdf} --camelox',
        monkeypatch=monkeypatch,
    )
    assert completed == utila.SUCCESS
