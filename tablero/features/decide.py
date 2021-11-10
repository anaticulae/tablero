# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================
"""Table Extraction Strategy
=========================

TODO: Add optimal table extraction selector for every single page, cause
table style can change in document.

Table Extractor
---------------

TODO: MOVE TO LINTER

Some tables contains double lines which indicates that is something wrong.

Example:

    If you add in word a table line and do not add any content add minize the
    height of the line with your cursor.
    Indicates that table are styled different.
"""

import iamraw
import serializeraw
import utila


def work(
    rcamelox: str,
    rcrossed: str,
    rhorizontal: str,
    rword: str,
    pages: tuple = None,
) -> str:
    # prepare data
    camelox = serializeraw.load_tables(rcamelox, pages=pages)
    crossed = serializeraw.load_tables(rcrossed, pages=pages)
    horizontal = serializeraw.load_tables(rhorizontal, pages=pages)
    word = serializeraw.load_tables(rword, pages=pages)
    # decide
    result = select_best(
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


def select_best(
    latexs,
    words,
    crosseds,
    camelots,
) -> iamraw.PageContentTableBoundings:
    present(latexs, words, crosseds, camelots)
    result = []
    synced = utila.sync_pages(
        [
            latexs,
            words,
            crosseds,
            camelots,
        ],
        numbers=False,
    )
    for latex, word, crossed, camelot in synced:
        selected = select_page(latex, word, crossed, camelot)
        if not selected:
            continue
        result.append(selected)
    return result


def select_page(latex, word, crossed, camelot):
    latex = latex or []
    word = word or []
    crossed = crossed or []
    camelot = camelot or []

    latex_detected = len(latex)
    word_detected = len(word)
    crossed_detected = len(crossed)
    camelot_detected = len(camelot)

    result = crossed
    if word_detected > crossed_detected:
        result = word
    if latex_detected > word_detected and latex_detected > crossed_detected:
        result = latex
    if camelot_detected > len(result):
        result = camelot
    return result


def present(latex, word, crossed, camelot):
    latex_detected = sum([len(item.content) for item in latex])
    word_detected = sum([len(item.content) for item in word])
    crossed_detected = sum([len(item.content) for item in crossed])
    camelot_detected = sum([len(item.content) for item in camelot])

    utila.log(f'latex:   {latex_detected}')
    utila.log(f'word:    {word_detected}')
    utila.log(f'crossed: {crossed_detected}')
    utila.log(f'camelot: {camelot_detected}')
