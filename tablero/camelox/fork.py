# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import functools
import os
import sys

import pdfinfo.pages
import serializeraw
import utila

import tablero

RUNTIME = os.path.join(tablero.ROOT, 'tablero/camelox/runtime.py')
utila.exists_assert(RUNTIME)


def run(pdffile: str, content: str, pages: tuple = None, worker: int = 1):
    if not utila.exists(pdffile):
        return []
    pages = determine_pages(pdffile, pages)
    grouped = utila.xsome(pages, count=worker)
    if content and utila.exists(content):
        content = serializeraw.load_contentboundingbox(content, pages=pages)
        content = [f'0,{box.top},1024,{box.bottom}' for box in content]
        content: list = list(utila.xsome(content, count=worker))
        todo = [
            functools.partial(single, pdffile, page, area)
            for page, area in zip(grouped, content)
        ]
    else:
        content = None
        todo = [functools.partial(single, pdffile, page) for page in grouped]
    todo = utila.fork(*todo, worker=worker)
    if isinstance(todo, int):
        utila.error('error while running camelox')
        sys.exit(utila.FAILURE)
    # prepare result
    errors = [done.stderr.strip() for done in todo if done.stderr.strip()]
    if errors:
        utila.error(errors)
    dones = [done.stdout.strip() for done in todo]
    # skip empty result
    dones = [item for item in dones if item != '[]']
    raw = '\n'.join(dones)
    result = serializeraw.load_tables(raw)
    return result


def single(pdffile, page, area=None):
    page = utila.from_tuple(page, separator='_')
    area = utila.from_tuple(area, separator='*') if area else ''
    cmd = f'python {RUNTIME} {pdffile} {area} {page}'
    cmd = utila.forward_slash(cmd, newline=False)
    completed = utila.run(cmd)
    return completed


def determine_pages(pdffile, pages: tuple = None):
    pagesmax = pdfinfo.pages.determine(pdffile)
    if pages is None:
        return list(range(pagesmax))
    return [
        page for page in range(pagesmax) if not utila.should_skip(page, pages)
    ]
