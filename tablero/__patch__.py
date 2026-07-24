# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import camelot.backends.ghostscript_backend
import playa.security
import utilo

# BEFORE = camelot.parsers.lattice.Lattice._generate_table_bbox  # pylint:disable=W0212

TODO = None

# def _generate_table_bbox(self):
#     BEFORE(self)
#     if not TODO:
#         return
#     current = TODO.pop()
#     _, top, __, bottom = [float(item) for item in current.split(',')]
#     top = top * 300 / 72 + 45
#     bottom = bottom * 300 / 72 - 45
#     print(self)
#     with PIL.Image.open(self.imagename) as image:
#         draw = PIL.ImageDraw.Draw(image)
#         width, height = image.width + 1, image.height + 1
#         draw.rectangle((0, 0, width, top), fill='white')
#         draw.rectangle((0, bottom, width, height), fill='white')
#         image.save(self.imagename)

# camelot.parsers.lattice.Lattice._generate_table_bbox = _generate_table_bbox  # pylint:disable=W0212


def convert(self, pdf_path, png_path, resolution=300):
    if not self.installed():
        raise OSError(
            "ghostscript is not installed. You can install it using the instructions"
            " here: https://camelot-py.readthedocs.io/en/master/user/install-deps.html"
        )
    gs_command = [
        "gswin64c" if utilo.iswin() else 'gs',
        "-q",
        "-sDEVICE=png16m",
        "-o",
        png_path,
        f"-r{resolution}",
        pdf_path,
    ]
    cmd = ' '.join(gs_command)
    utilo.run(cmd)


camelot.backends.ghostscript_backend.GhostscriptBackend.convert = convert


@property
def is_extractable(self):  # pylint:disable=W0613
    return True


playa.security.PDFStandardSecurityHandler.is_extractable = is_extractable  # pylint:disable=I1101
