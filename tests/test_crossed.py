# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw.path
import power
import pytest
import serializeraw
import utilatest

import tablero.features.crossed


@pytest.mark.parametrize('source, expected', [
    pytest.param(
        power.DOCU013_PDF,
        [1, 3, 3, 5, 2, 5, 6, 4, 5, 3, 1],
        id='vim',
    ),
])
@utilatest.requires(power.DOCU013_PDF)
def test_table_extract(source, expected):
    source = power.link(source)
    source = iamraw.path.line(source)
    loaded = serializeraw.load_lines(source)
    # add empty lines, cause pages without lines will be ignored, we
    # require this to check extraction result properly.
    loaded.insert(0, iamraw.PageContentLine(page=0, content=[]))
    tables = tablero.features.crossed.run(loaded)

    flat = [len(item.content) for item in tables]
    assert flat == expected
