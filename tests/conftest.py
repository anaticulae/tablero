# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import gennex
import hoverpower
import pytest
import utilotest
from utilotest import mp  # pylint:disable=W0611
from utilotest import td  # pylint:disable=W0611

import tablero

pytest_plugins = ['pytester', 'xdist']  # pylint: disable=invalid-name

PACKAGE = tablero.PROCESS

hoverpower.setup(tablero.ROOT)

RESOURCES = [
    hoverpower.BACHELOR109_PDF,
    hoverpower.DOCU007_PDF,
    hoverpower.DOCU013_PDF,
    hoverpower.MASTER110_PDF,
    hoverpower.ORDER050_PDF,
    (hoverpower.BACHELOR051_PDF, '20:35'),
    (hoverpower.BACHELOR056_PDF, '0:34'),
    (hoverpower.BACHELOR063_PDF, '24:28'),
    (hoverpower.BACHELOR090_PDF, '76:81'),
    (hoverpower.DISS205_PDF, '130:145'),
    (hoverpower.MASTER075_PDF, '10:20'),
    (hoverpower.MASTER098_PDF, '53:61'),
    (hoverpower.MASTER099_PDF, '5:15,45:65'),
    (hoverpower.MASTER112_PDF, '110'),
]

WORKER = utilotest.worker_count(
    number=6,
    onci=len(RESOURCES),
)

RESOURCES_NOTABLE = [
    hoverpower.HOME043_PDF,
    hoverpower.HOME025_PDF,
    hoverpower.BOOK007_PDF,
]


@pytest.mark.usefixtures('session')
def pytest_sessionstart():
    hoverpower.run()


def extract(resources):
    gennex.extract(
        files=resources,
        pagenumber=True,
        footnote=True,
        groupme='--content',
        oneline=None,
        worker=WORKER,
        pages=':',
    )


def extract_notable(resources):
    gennex.extract(
        files=resources,
        dest=hoverpower.generated('notable'),
        pagenumber=True,
        footnote=True,
        groupme='--content',
        oneline=None,
        worker=len(RESOURCES_NOTABLE),
        pages=':',
    )
