# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import sys

import camelot.backends.ghostscript_backend
import camelot.handlers
import camelot.parsers.lattice
import PIL
import PIL.ImageDraw
import utila


def __init__(self, filepath, pages="1", password=None):
    self.filepath = filepath
    if password is None:
        self.password = ""  # nosec
    else:
        self.password = password
        if sys.version_info[0] < 3:
            self.password = self.password.encode("ascii")
    self.pages = self._get_pages(pages)  # pylint:disable=W0212


# disable path check, we know what we do.
camelot.handlers.PDFHandler.__init__ = __init__

BEFORE = camelot.parsers.lattice.Lattice._generate_table_bbox  # pylint:disable=W0212

TODO = None


def _generate_table_bbox(self):
    BEFORE(self)
    if not TODO:
        return
    current = TODO.pop()
    _, top, __, bottom = [float(item) for item in current.split(',')]
    top = top * 300 / 72 + 45
    bottom = bottom * 300 / 72 - 45
    with PIL.Image.open(self.imagename) as image:
        draw = PIL.ImageDraw.Draw(image)
        width, height = image.width + 1, image.height + 1
        draw.rectangle((0, 0, width, top), fill='white')
        draw.rectangle((0, bottom, width, height), fill='white')
        image.save(self.imagename)


camelot.parsers.lattice.Lattice._generate_table_bbox = _generate_table_bbox  # pylint:disable=W0212


def convert(self, pdf_path, png_path, resolution=300):
    if not self.installed():
        raise OSError(
            "Ghostscript is not installed. You can install it using the instructions"
            " here: https://camelot-py.readthedocs.io/en/master/user/install-deps.html"
        )
    gs_command = [
        "gswin64c",
        "-q",
        "-sDEVICE=png16m",
        "-o",
        png_path,
        f"-r{resolution}",
        pdf_path,
    ]
    cmd = ' '.join(gs_command)
    utila.run(cmd)


camelot.backends.ghostscript_backend.GhostscriptBackend.convert = convert
