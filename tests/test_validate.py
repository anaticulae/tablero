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
import tests.conftest

ARCHIVE = utila.join(tablero.ROOT, 'tests/expected', exist=True)

TODO = [
    item if isinstance(item, str) else item[0]
    for item in tests.conftest.RESOURCES
]
TODO = [pytest.param(item, id=utila.file_name(item)) for item in TODO]


@pytest.mark.parametrize('source', TODO)
@utilatest.longrun
def test_validate(source, testdir, monkeypatch):
    utilatest.fixture_requires(source)
    Evaluate(
        source=source,
        folder=None,
        workdir=testdir.tmpdir,
        monkeypatch=monkeypatch,
    ).evaluate()


NOTABLE = [
    item if isinstance(item, str) else item[0]
    for item in tests.conftest.RESOURCES_NOTABLE
]
NOTABLE = [pytest.param(item, id=utila.file_name(item)) for item in NOTABLE]


@pytest.mark.parametrize('source', NOTABLE)
@utilatest.longrun
def test_notable_validate(source, testdir, monkeypatch):
    folder = 'notable'
    utilatest.fixture_requires(source, folder=folder)
    Evaluate(
        source=source,
        folder=folder,
        workdir=testdir.tmpdir,
        monkeypatch=monkeypatch,
    ).evaluate()


class Evaluate(utilatest.BaseLiner):

    def __init__(self, source, folder, workdir, monkeypatch):
        super().__init__(
            program=functools.partial(
                tests.run,
                monkeypatch=monkeypatch,
            ),
            step=f'all --table {source}',
            pages=':',
            source=power.link(source, folder=folder),
            workdir=workdir,
            archive=ARCHIVE,
            loader=self.frompath,
            convert_source=False,
            onfailure=self.tables_show,
        )
        self.pdf = source

    def tables_show(self, tables):
        outdir = tablero.display.render_tables(
            tables,
            pdf=self.pdf,
        )
        utila.log(outdir)
        utila.copy_content(outdir, self.workdir)

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
