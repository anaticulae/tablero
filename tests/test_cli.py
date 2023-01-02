# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2019-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import utila
import utilatest

import tests


def test_cli_help(mp):
    """Run help to reach basic test coverage."""
    tests.run('--help', mp=mp)


@utilatest.nightly
@utilatest.requires(power.BOOK007_PDF)
def test_cli_run(td, mp):
    """Run tabelero with all steps."""
    source = power.link(power.BOOK007_PDF)
    tests.run(
        f'-i {source} -i {td.tmpdir} --table={power.BOOK007_PDF} -j8',
        mp=mp,
    )


@utilatest.longrun
@utilatest.requires(power.BACHELOR109_PDF)
def test_cli_internal_error(td, mp):
    """Run tablero with unsupported camelot file."""
    pdf = power.BACHELOR109_PDF
    source = power.link(pdf)
    completed = tests.run(
        f'-i {source} -i {td.tmpdir} --table={pdf} --camelox',
        mp=mp,
    )
    assert completed == utila.SUCCESS
