# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2022 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import configo

TABLE_MIN_HEIGHT = configo.HV_FLOAT_PLUS(default=50.0)
# TODO: USE TABLE APROACH
MAX_SINGLE_LINE_QUOTE = configo.HV_FLOAT_PLUS(default=0.4)

TABLE_MERGE_DISTANCE = configo.HV_FLOAT_PLUS(default=20.0)

TABLE_HORIZONTAL_MAX_DIFF = configo.HV_FLOAT_PLUS(default=4.0)

TABLE_VERTICAL_MAX_DIFF = configo.HV_FLOAT_PLUS(default=4.0)

# tables are buld ouf long lines. The average line length is used to
# exclude figures etc.
TABLE_MIN_AVG_LINE_LENGTH = configo.HV_FLOAT_PLUS(default=40.0)
