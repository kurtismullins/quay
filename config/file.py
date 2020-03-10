# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, with_statement

import glob
import json
import logging

from yaml import safe_load, safe_dump

from config.base import BaseConfig
from config.exceptions import NoConfigFilesFound


logger = logging.getLogger(__name__)


class FileConfig(BaseConfig):
    """
    A configuration object which uses files for persisting the configuration.
    """

    def save(self, path=None):
        """
        Writes the configuration to a file located at a given `location`. By
        default, the file `config.yaml` is used.

        location: The location, on disk, which will be overwritten with the
                  current configuration.
        """
        raise NotImplementedError

    def load(self, path=None):
        """
        Reads the configuration from all files matching the given `path`
        pattern. By default, all files matching `config*.yaml` will be read in
        alphanumerical order.
        """
        # Container for configuration read from file(s)
        new_config = {}

        paths = self._list_files(path)
        if not paths:
            raise NoConfigFilesFound

        logger.debug('The following configuration files were found: %s', paths)

        for p in paths:
            data = self._read_yaml_from_file(p)
            # TODO: Validate data
            new_config.update(data)

        print(json.dumps(new_config, indent=2, sort_keys=True))

    def _list_files(self, path=None):
        """
        Lists all files which match the given `path`.
        """
        if not path:
            if self._read_path:
                path = self._read_path  # fall-back to path set on __init__()
            else:
                logger.warning('Invalid configuration file path: %s', path)
                return []

        paths = glob.glob(path)
        if len(paths) == 0:
            msg = 'No configuration files found which match the path: %s'
            logger.warning(msg, path)
            return []

        sorted_paths = sorted(paths)  # Ensure a consistent, deterministic order
        return sorted_paths

    def _read_yaml_from_file(self, path=None):
        """
        Reads and validates a given file. If valid, returns a Python
        representation of the file's contents.
        """
        if not path:
            msg = 'Attempted to read YAML File with invalid path: %s' % path
            raise Exception(msg)  # TODO: Use specific exception type

        with open(path, 'r') as f:
            data = safe_load(f)
            logger.info('Read configuration from: %s', path)

        return data
