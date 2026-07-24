# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2022-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools

import hoverpower
import iamraw
import pytest
import serializeraw
import utilo
import utilotest

import tablero
import tests
import tests.conftest

ARCHIVE = utilo.join(tablero.ROOT, 'tests/expected', exist=True)
ARCHIVE_NOTABLE = utilo.join(tablero.ROOT, 'tests/notable', exist=True)

TODO = utilotest.test_resources(tests.conftest.RESOURCES)


@tests.ughost
@pytest.mark.parametrize('source', TODO)
@utilotest.longrun
def test_validate(source, td, mp):
    utilotest.fixture_requires(source)
    Evaluate(
        source=source,
        folder=None,
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


NOTABLE = [
    item if isinstance(item, str) else item[0]
    for item in tests.conftest.RESOURCES_NOTABLE
]
NOTABLE = [pytest.param(item, id=utilo.file_name(item)) for item in NOTABLE]


@pytest.mark.parametrize('source', NOTABLE)
@utilotest.longrun
def test_notable_validate(source, td, mp):
    folder = 'notable'
    utilotest.fixture_requires(source, folder=folder)
    Evaluate(
        source=source,
        folder=folder,
        archive=ARCHIVE_NOTABLE,
        workdir=td.tmpdir,
        mp=mp,
    ).evaluate()


class Evaluate(utilotest.BaseLiner):

    def __init__(self, source, folder, workdir, mp, archive=ARCHIVE):
        super().__init__(
            program=functools.partial(
                tests.run,
                mp=mp,
            ),
            step=f'all --table {source}',
            pages=':',
            source=hoverpower.link(source, folder=folder),
            workdir=workdir,
            archive=archive,
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
        utilo.log(outdir)
        if outdir:
            utilo.copy_content(outdir, self.workdir)

    def frompath(self, path):  # pylint:disable=R0201
        path = iamraw.path.tablero_result(path)
        return serializeraw.load_tables(path)

    def raw(self, value) -> str:
        collected = []
        for content in value:
            page, tables = content.page, content.content
            for table in tables:
                collected.append(rawline(page, table))
        result = utilo.NEWLINE.join(collected)
        return result


def rawline(page: int, table) -> str:
    pages = str(page).zfill(3)
    # TODO: USE ROUNDME AFTER UPGRADING UTILO
    # use int's for a more robust verification.
    table = str(tuple(int(item) for item in table.bounding))
    return f'{pages} {table}'
