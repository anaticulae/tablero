# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Table Extractor
===============

TODO: MOVE TO LINTER

Some tables contains double lines which indicates that is something wrong.

Example:

    If you add in word a table line and do not add any content add minize the
    height of the line with your cursor.
    Indicates that table are styled different.

"""

import serializeraw

import tablero.table.strategy


def work(
    camelox: str,
    crossed: str,
    horizontal: str,
    word: str,
    pages: tuple = None,
) -> str:
    # prepare data
    camelox = serializeraw.load_tables(camelox, pages=pages)
    crossed = serializeraw.load_tables(crossed, pages=pages)
    horizontal = serializeraw.load_tables(horizontal, pages=pages)
    word = serializeraw.load_tables(word, pages=pages)
    # decide
    result = tablero.table.strategy.select_best(
        horizontal,
        word,
        crossed,
        camelox,
    )
    # prepare result
    # remove empty pages
    result = [item for item in result if item.content]
    dumped = serializeraw.dump_tables(result)
    return dumped
