# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import os

import iamraw
import PIL.Image
import PIL.ImageDraw
import ughost
import utilo

SCALE = 300 / 72
SCALES = (SCALE, SCALE, SCALE, SCALE)


def render_tables(
    tables: iamraw.PageContentTableBoundings,
    pdf: str,
):
    pages = [item.page for item in tables if item.content]
    if not pages:
        # do not render all pages
        return None
    outdir = ughost.pdfwrite(pdf, pages=pages)
    index = 1
    for tablepage in tables:
        if not tablepage.content:
            continue
        filepath = os.path.join(outdir, f'{index}.png')
        with PIL.Image.open(filepath) as images:
            renderer = PIL.ImageDraw.Draw(images)
            for item in tablepage.content:
                bounding = utilo.rect_scale(
                    item.bounding,
                    scale=SCALES,
                )
                renderer.rectangle(bounding, outline='red', width=5)
                lines = item.lines
                if lines:
                    for line in lines:
                        line = utilo.rect_scale(
                            line,
                            scale=SCALES,
                        )
                        renderer.rectangle(line, outline='blue', width=2)
            images.save(filepath, 'PNG')
        index += 1
    outdir: str = utilo.forward_slash(outdir)
    return outdir
