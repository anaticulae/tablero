# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import iamraw
import power
import pytest
import serializeraw
import utila
import utilatest

import tablero
import tests

ARCHIVE = utila.join(tablero.ROOT, 'tests/expected', exist=True)


@pytest.mark.parametrize('source, expected', [
    pytest.param(power.BACHELOR090_PDF, 'bachelor090', id='bachelor090'),
])
@utilatest.longrun
def test_validate(source, expected, testdir, monkeypatch):
    utilatest.fixture_requires(source)
    Evaluate(
        source=source,
        pages=':',
        expected=expected,
        workdir=testdir.tmpdir,
        monkeypatch=monkeypatch,
    ).evaluate()


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, pages, expected, workdir, monkeypatch):
        super().__init__(
            program=functools.partial(
                tests.run,
                monkeypatch=monkeypatch,
            ),
            step=None,
            pages=pages,
            source=power.link(source),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.frompath,
            convert_source=False,
            index=expected,
        )
        self.headlines = power.link(source)

    def frompath(self, path):  # pylint:disable=R0201
        path = iamraw.path.tablero_result(path)
        return serializeraw.load_tables(path)

    def raw(self, value) -> str:
        collected = []
        for content in value:
            page, tables = content.page, content.content
            for table in tables:
                collected.append(rawline(page, table))
        result = utila.NEWLINE.join(collected)
        return result


def rawline(page: int, table) -> str:
    pages = str(page).zfill(3)
    table = str(table.bounding)
    return f'{pages} {table}'
