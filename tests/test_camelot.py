# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import power
import pytest
import utila
import utilatest

import tablero.camelox.fork
import tablero.features.camelox
import tests


@tests.ghost
def test_camelot_run():
    source = power.DOCU013_PDF
    parsed = tablero.features.camelox.run(source, pages=2)
    assert len(parsed) == 1


@tests.ghost
@utilatest.nightly
def test_camelot_forked():
    source = power.DOCU013_PDF
    content = power.link(source)
    parsed = tablero.camelox.fork.run(source, content=content, worker=4)
    flatten = utila.flatten_content(parsed)
    # The purpose of this test is to run in forked mode, not to check the
    # correct result.
    assert 20 <= len(flatten) <= 40


@pytest.mark.xfail(reason='improve stream')
def test_camelot_latex():
    source = power.BACHELOR090_PDF
    parsed = tablero.features.camelox.run(source, pages=76)
    assert len(parsed) == 1


@tests.ghost
@pytest.mark.parametrize('verbose', [True, False])
def test_camelot_verbose_flag(verbose):
    # TODO: REMOVE WARNING LATER
    source = power.MASTER116_PDF
    with pytest.warns(match='page-3 is image-based'):
        tablero.features.camelox.run(
            source,
            pages=(2, 3),
            verbose=verbose,
        )


@tests.ghost
@utilatest.longrun
def test_camelot_master116_error():
    """Do not detect `Maximum, Minimum, Durchschnitt` as table."""
    source = power.MASTER116_PDF
    parsed = tablero.features.camelox.run(
        source,
        pages=(20,),
        verbose=True,
    )
    assert not parsed


@tests.ghost
def test_camelot_master110page89():
    source = power.MASTER110_PDF
    parsed = tablero.features.camelox.run(
        source,
        pages=(89,),
        verbose=True,
    )
    assert len(utila.flatten_content(parsed)) == 1


@pytest.mark.xfail(reason='could not detect image tables')
def test_camelot_bachelor76_error():
    """\
    TODO: INVESTIGATE:
    UserWarning: (479.5, 482.5) does not lie in column range
    (116.13284084038696, 478.9434582829505) [utils.py:650]
    """
    source = power.BACHELOR076_PDF
    parsed = tablero.features.camelox.run(
        source,
        verbose=True,
        pages=(13,),
    )
    assert parsed


@tests.ghost
def test_camelot_internal_error(capsys):
    source = power.BACHELOR109_PDF
    parsed = tablero.features.camelox.run(source)
    assert not parsed
    error = utilatest.stderr(capsys)
    assert 'internal camelot error' in error
