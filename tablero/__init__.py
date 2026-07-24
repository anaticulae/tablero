#==============================================================================
# C O P Y R I G H T
#------------------------------------------------------------------------------
# Copyright (c) 2021-2023 by Helmut Konrad Schewe. All rights reserved.
# This file is property of Helmut Konrad Schewe. Any unauthorized copy,
# use or distribution is an offensive act against international law and may
# be prosecuted under federal law. Its content is company confidential.
#==============================================================================

import importlib.metadata
import os

import tablero.__patch__

PROCESS = 'tablero'
__version__ = importlib.metadata.version(PROCESS)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

DESCRIPTION = """\
tablero converts a bunch of lines to the following possible features:

* tables
"""
