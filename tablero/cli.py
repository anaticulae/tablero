# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utila

import tablero

WORKPLAN = [
    utila.create_step(
        'camelox',
        [
            utila.ResultFile('table', name=None, ext=None, optional=True),
        ],
        ('camelox',),
    ),
    utila.create_step(
        'crossed',
        [
            utila.ResultFile('rawmaker', 'line_line'),
            utila.ResultFile('groupme', 'content_content'),
        ],
        ('crossed',),
    ),
    utila.create_step(
        'word',
        [
            utila.ResultFile('rawmaker', 'line_line'),
            utila.ResultFile('groupme', 'content_content'),
        ],
        ('word',),
    ),
    utila.create_step(
        'horizontal',
        [
            utila.ResultFile('rawmaker', 'text_text'),
            utila.ResultFile('rawmaker', 'text_positions'),
            utila.ResultFile('rawmaker', 'border_pages'),
            utila.ResultFile('groupme', 'footer_footerheader'),
            utila.ResultFile('rawmaker', 'line_line'),
            utila.ResultFile('groupme', 'content_content'),
        ],
        ('horizontal',),
    ),
    utila.create_step(
        'decide',
        [
            utila.ResultFile('tablero', 'camelox_camelox'),
            utila.ResultFile('tablero', 'crossed_crossed'),
            utila.ResultFile('tablero', 'horizontal_horizontal'),
            utila.ResultFile('tablero', 'word_word'),
        ],
        ('decide',),
    ),
]


def main():
    utila.featurepack(
        workplan=WORKPLAN,
        root=tablero.ROOT,
        featurepackage='tablero.features',
        config=utila.FeaturePackConfig(
            description=tablero.DESCRIPTION,
            multiprocessed=True,
            name=tablero.PROCESS,
            pages=True,
            profileflag=True,
            singleinput=True,
            verboseflag=True,
            version=tablero.__version__,
        ),
    )
