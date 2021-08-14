# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import collections
import warnings

import camelot
import camelot.core
import iamraw
import pdfinfo.pages
import rawmaker.features.border
import serializeraw
import utila

import tablero.__patch__
import tablero.camelox.fork


def work(content: str, lines: str, table: str, pages: tuple = None) -> str:
    if not utila.exists(table):
        utila.error(f'skip camelox, missing: {table}')
        return '[]'
    if not utila.exists(lines):
        lines = None
    else:
        lines = serializeraw.load_lines(lines, pages=pages)
        pages = shrink_pages(lines, pages)
    if pages != []:
        worker: int = 6
        extracted = tablero.camelox.fork.run(
            pdffile=table,
            content=content,
            pages=pages,
            worker=worker,
        )
    else:
        utila.debug('no pages with lines selected, skip camelox')
        extracted = []
    dumped = serializeraw.dump_tables(extracted)
    return dumped


def shrink_pages(lines, pages):
    """Use line pages to reduce amount of generated pages. In the
    current state, camelox detect tables constructing out of lines. If
    we do not have any lines, we can save this generation time."""
    if not lines:
        return pages
    line_pages = [item.page for item in lines if len(item.content) >= 3]
    if not line_pages:
        return []
    result = [
        item for item in line_pages if not utila.should_skip(line_pages, pages)
    ]
    return result


@utila.profile('strategy:camelot')
def run(
    pdffile: str,
    boundings: list = None,
    pages: tuple = None,
    verbose: bool = False,
) -> iamraw.PageContentTableBoundings:
    if pdffile is None:
        # no pdffile given
        utila.error('no camelot pdf file given')
        return []
    utila.exists_assert(pdffile)
    parsed = parse_tables(pdffile, boundings, pages, verbose=verbose)
    # group by page number
    result = group_result(parsed, pdffile, pages)
    return result


def parse_tables(
    pdffile: str,
    boundings: list,
    pages: tuple = None,
    verbose: bool = False,
):
    # convert internal page definition to camelot definition
    pagesmax = pdfinfo.pages.determine(pdffile)
    pages = camelot_pages(pages, pagesmax)
    result = parse_page(pdffile, boundings, pages, verbose=verbose)
    return result


def parse_page(
    pdffile: str,
    boundings: list,
    page: str,
    verbose: bool = False,
) -> list:
    boundings = list(boundings) if boundings else None
    # HACK:
    tablero.__patch__.TODO = boundings
    catch_warnings = warnings.catch_warnings if verbose else utila.nothing
    with catch_warnings():
        parsed: camelot.core.TableList = camelot.read_pdf(
            filepath=pdffile,
            pages=page,
        )
    # if not parsed:
    #     parsed: camelot.core.TableList = camelot.read_pdf(
    #         pdffile,
    #         pages=page,
    #         flavor="stream",
    #     )
    return parsed


TABLE_ACCURACY_MIN = 75.0  # TODO: HOLY VALUE
TABLE_WHITESPACE_MAX = 40.0  # TODO: HOLY VALUE
TABLE_WIDTH_MIN = 100
TABLE_HEIGHT_MIN = 30


def group_result(parsed, pdffile, pages) -> iamraw.PageContentTableBoundings:
    # Determine pdf page size to convert to rawmaker bounding definiton.
    sizes = pagesizes(pdffile, pages)
    collected = collections.defaultdict(list)
    for table in parsed:
        if invalid_table(table):
            utila.debug(f'skip table: {table}')
            utila.debug(table.parsing_report)
            continue
        utila.debug(table.parsing_report)
        pagenumber = zero_based(table.page)
        # Hint: We flip top/down
        bounding = flip_bounding(table._bbox, sizes[pagenumber])  # pylint:disable=W0212
        collected[pagenumber].append(iamraw.TableBounding(bounding=bounding))
    result = [
        iamraw.PageContentTableBounding(page=page, content=content)
        for page, content in collected.items()
    ]
    return result


def invalid_table(table) -> bool:
    if table.parsing_report['accuracy'] < TABLE_ACCURACY_MIN:
        return True
    if table.parsing_report['whitespace'] > TABLE_WHITESPACE_MAX:
        return True
    cells = utila.flatten(table.cells)
    cells = [
        (item.x1, item.y1, item.x2, item.y2)
        for item in cells
        if item._text.strip()  # pylint:disable=W0212
    ]
    rectangle = utila.rectangle_max(cells)
    if utila.rectangle_width(rectangle) < TABLE_WIDTH_MIN:
        return True
    if utila.rectangle_height(rectangle) < TABLE_HEIGHT_MIN:
        return True
    return False


def flip_bounding(bounding, pagesize) -> iamraw.BoundingBox:
    pageheight = pagesize[1]
    result = (
        bounding[0],
        pageheight - bounding[3],
        bounding[2],
        pageheight - bounding[1],
    )
    return result


def zero_based(pagenumber: int) -> int:
    return pagenumber - 1


def camelot_pages(pages: tuple, pagesmax: int) -> str:
    """\
    >>> camelot_pages((1, 2, 3, 4, 5), pagesmax=20)
    '2,3,4,5,6'
    >>> camelot_pages((8, 9, 10, 11), 13)
    '9,10,11,12'
    """
    if isinstance(pages, list):
        pages = tuple(pages)  # TODO: REMOVE AFTER UPGRADING UTILA
    pages = [
        str(page + 1)
        for page in range(pagesmax)
        if not utila.should_skip(page, pages)
    ]
    result = ','.join(pages)
    return result


def pagesizes(path: str, pages: tuple = None):
    with rawmaker.reader.read(path) as doc:
        sizes = rawmaker.features.border.pagesizes(doc, pages=pages)
    sizes: dict = {size.page: size.size for size in sizes}
    return sizes
