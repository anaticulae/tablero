# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2020-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import utilo

import tablero

WORKPLAN = [
    utilo.create_step(
        'camelox',
        [
            utilo.ResultFile('groupme', 'content_content'),
            utilo.ResultFile('rawmaker', 'line_line', optional=True),
            utilo.Value('table', typ=None, defaultvar=None),
        ],
        ('camelox',),
    ),
    utilo.create_step(
        'crossed',
        [
            utilo.ResultFile('rawmaker', 'line_line'),
            utilo.ResultFile('groupme', 'content_content'),
        ],
        ('crossed',),
    ),
    utilo.create_step(
        'word',
        [
            utilo.ResultFile('rawmaker', 'line_line'),
            utilo.ResultFile('groupme', 'content_content'),
        ],
        ('word',),
    ),
    utilo.create_step(
        'horizontal',
        [
            utilo.ResultFile('rawmaker', 'text_text'),
            utilo.ResultFile('rawmaker', 'text_positions'),
            utilo.ResultFile('rawmaker', 'border_pages'),
            utilo.ResultFile('groupme', 'footer_footerheader'),
            utilo.ResultFile('rawmaker', 'line_line'),
            utilo.ResultFile('groupme', 'content_content'),
        ],
        ('horizontal',),
    ),
    utilo.create_step(
        'result',
        [
            utilo.ResultFile('tablero', 'camelox_camelox'),
            utilo.ResultFile('tablero', 'crossed_crossed'),
            utilo.ResultFile('tablero', 'horizontal_horizontal'),
            utilo.ResultFile('tablero', 'word_word'),
        ],
        ('result',),
    ),
    utilo.create_step(
        'decide',
        [
            utilo.ResultFile('tablero', 'result_result'),
        ],
        ('decide',),
    ),
]


def main():
    utilo.featurepack(
        workplan=WORKPLAN,
        root=tablero.ROOT,
        featurepackage='tablero.features',
        config=utilo.FeaturePackConfig(
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
