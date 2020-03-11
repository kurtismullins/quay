# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


class NoConfigFilesFound(Exception):
    """
    Raised when no configuration files were found.
    """


class InvalidConfigFilePath(Exception):
    """
    Raised when an invalid path is attempted to use when reading or writing
    configuration files.
    """
