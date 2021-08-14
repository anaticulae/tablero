# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import genex
import power
import pytest

import tablero

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = tablero.PROCESS
WORKER = 6

power.setup(tablero.ROOT)

RESOURCES = [
    power.ORDER050_PDF,
    (power.BACHELOR056_PDF, '0:34'),
    power.DOCU013_PDF,
    (power.MASTER098_PDF, '53:61'),
    (power.BACHELOR090_PDF, '76:81'),
    power.BOOK007_PDF,
    power.DOCU007_PDF,
    (power.BACHELOR063_PDF, '24:28'),
    (power.MASTER112_PDF, '110'),
]

RESOURCES_NOTABLE = [
    power.HOME040_PDF,
    power.HOME025_PDF,
    power.BOOK007_PDF,
]


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    power.run()


def extract(resources):
    genex.extract(
        files=resources,
        destination=power.generated(),
        groupme='--pagenumbers --footer --content',
        tablero=False,
        oneline=None,
        pdfinfo=False,
        worker=WORKER,
        base=power.REPOSITORY,
        pages=':',
    )


def extract_notable(resources):
    genex.extract(
        files=resources,
        destination=power.generated('notable'),
        groupme='--pagenumbers --footer --content',
        tablero=False,
        oneline=None,
        pdfinfo=False,
        worker=WORKER,
        base=power.REPOSITORY,
        pages=':',
    )
