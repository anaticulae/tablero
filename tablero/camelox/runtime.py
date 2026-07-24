# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import sys

import serializeraw
import utilo

import tablero.features.camelox

if __name__ == "__main__":
    FILE, CONTENT, PAGES = sys.argv[1], sys.argv[2], sys.argv[3]
    # TODO: REPLACE AFTER UPGRADING UTILA
    PAGES = utilo.parse_ints(PAGES.replace('_', ' '))
    CONTENT = CONTENT.split('*')
    result = tablero.features.camelox.run(FILE, CONTENT, PAGES)
    dumped = serializeraw.dump_tables(result)
    utilo.log(dumped)
