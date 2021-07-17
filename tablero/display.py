# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import iamraw
import PIL.Image
import PIL.ImageDraw
import utila

GHOST = 'gswin64c' if os.name == 'nt' else 'gs'


def render_tables(
    tables: iamraw.PageContentTableBoundings,
    pdf: str,
    outdir: str,
):
    pages = [item.page for item in tables if item.content]
    if not pages:
        # do not render all pages
        return
    ghost_small(pdf, outdir, pages=pages)
    index = 1
    for tablepage in tables:
        if not tablepage.content:
            continue
        filepath = os.path.join(outdir, f'tables{index}.png')
        with PIL.Image.open(filepath) as images:
            renderer = PIL.ImageDraw.Draw(images)
            for item in tablepage.content:
                scale = 300 / 72
                bounding = utila.rectangle_scale(
                    item.bounding,
                    scale=(scale, scale, scale, scale),
                )
                renderer.rectangle(bounding, outline='red', width=5)
            images.save(filepath, 'PNG')
        index += 1


def ghost_small(source: str, destination: str, pages: str = ''):
    destination = os.path.join(destination, 'tables%d.png')
    if pages:
        # -sPageList=1,3,5
        pages = '-sPageList=' + (','.join([str(page + 1) for page in pages]))
    else:
        pages = ''
    config = '-sDEVICE=png16m -r300  -dBATCH -dNOPAUSE -SAFE'
    cmd = f'{GHOST} {config} {pages} -sOutputFile={destination} {source}'
    utila.run(cmd)
