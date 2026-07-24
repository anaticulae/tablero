# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import hoverpower
import pytest
import utilo
import utilotest

import tablero.camelox.fork
import tablero.features.camelox
import tests


@tests.ughost
def test_camelot_run():
    source = hoverpower.DOCU013_PDF
    parsed = tablero.features.camelox.run(source, pages=2)
    assert len(parsed) == 1


@tests.ughost
@utilotest.nightly
def test_camelot_forked():
    source = hoverpower.DOCU013_PDF
    content = hoverpower.link(source)
    parsed = tablero.camelox.fork.run(source, content=content, worker=4)
    flatten = utilo.flatten_content(parsed)
    # The purpose of this test is to run in forked mode, not to check the
    # correct result.
    assert 20 <= len(flatten) <= 40


@pytest.mark.xfail(reason='improve stream')
def test_camelot_latex():
    source = hoverpower.BACHELOR090_PDF
    parsed = tablero.features.camelox.run(source, pages=76)
    assert len(parsed) == 1


@tests.ughost
@pytest.mark.parametrize('verbose', [True, False])
def test_camelot_verbose_flag(verbose):
    # TODO: REMOVE WARNING LATER
    source = hoverpower.MASTER116_PDF
    with pytest.warns(match='page-3 is image-based'):
        tablero.features.camelox.run(
            source,
            pages=(2, 3),
            verbose=verbose,
        )


@tests.ughost
@utilotest.longrun
def test_camelot_master116_error():
    """Do not detect `Maximum, Minimum, Durchschnitt` as table."""
    source = hoverpower.MASTER116_PDF
    parsed = tablero.features.camelox.run(
        source,
        pages=(20,),
        verbose=True,
    )
    assert not parsed


@tests.ughost
def test_camelot_master110page89():
    source = hoverpower.MASTER110_PDF
    parsed = tablero.features.camelox.run(
        source,
        pages=(89,),
        verbose=True,
    )
    assert len(utilo.flatten_content(parsed)) == 1


@pytest.mark.xfail(reason='could not detect image tables')
def test_camelot_bachelor76_error():
    """\
    TODO: INVESTIGATE:
    UserWarning: (479.5, 482.5) does not lie in column range
    (116.13284084038696, 478.9434582829505) [utils.py:650]
    """
    source = hoverpower.BACHELOR076_PDF
    parsed = tablero.features.camelox.run(
        source,
        verbose=True,
        pages=(13,),
    )
    assert parsed


@utilotest.nightly
@tests.ughost
def test_camelot_internal_error(capsys):
    """Before upgrading camelot, camelot produces an error cause it was
    not able to extract table.

    After upgrading this error does not occur
    anymore.
    """
    source = hoverpower.BACHELOR109_PDF
    parsed = tablero.features.camelox.run(source)
    assert parsed
    error = utilotest.stderr(capsys)
    assert not error, str(error)
    # assert 'internal camelot error' in error
