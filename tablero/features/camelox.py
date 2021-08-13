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


def work(content: str, table: str, pages: tuple = None) -> str:
    if not utila.exists(table):
        utila.error(f'skip camelox, missing: {table}')
        return '[]'
    worker: int = 6
    extracted = tablero.camelox.fork.run(
        pdffile=table,
        content=content,
        pages=pages,
        worker=worker,
    )
    dumped = serializeraw.dump_tables(extracted)
    return dumped


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


def group_result(parsed, pdffile, pages) -> iamraw.PageContentTableBoundings:
    # Determine pdf page size to convert to rawmaker bounding definiton.
    sizes = pagesizes(pdffile, pages)
    collected = collections.defaultdict(list)
    for table in parsed:
        if table.parsing_report['accuracy'] < TABLE_ACCURACY_MIN:
            utila.debug(f'skip table: {table}')
            utila.debug(table.parsing_report)
            continue
        utila.error(table.parsing_report)
        pagenumber = zero_based(table.page)
        # Hint: We flip top/down
        bounding = flip_bounding(table._bbox, sizes[pagenumber])  # pylint:disable=W0212
        collected[pagenumber].append(iamraw.TableBounding(bounding=bounding))
    result = [
        iamraw.PageContentTableBounding(page=page, content=content)
        for page, content in collected.items()
    ]
    return result


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
