# =============================================================================
# C O P Y R I G H T
# -----------------------------------------------------------------------------
# Copyright (c) 2021 by Helmut Konrad Fahrendholz. All rights reserved.
# This file is property of Helmut Konrad Fahrendholz. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
# =============================================================================

import iamraw
import serializeraw

LINES_PER_PAGE_MAX = 1000


def load_data(text, textposition, lines, pages=None):
    navigators = serializeraw.create_pagetextnavigators_fromfile(
        text,
        textposition,
        pages=pages,
    )
    lines = serializeraw.load_lines(lines, pages=pages)
    lines = limit_lines(lines)
    return navigators, lines


def limit_lines(lines):
    # TODO: DISABLE AFTER HAVING BETTER CLUSTER STRATEGY
    result = []
    for page in lines:
        content = page.content
        if len(page.content) > LINES_PER_PAGE_MAX:
            # too many lines on this page
            content = []
        result.append(iamraw.PageContentLine(page=page.page, content=content))
    return result
