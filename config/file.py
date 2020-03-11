# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, with_statement

import glob
import json
import logging

from yaml import safe_load, safe_dump

from config.base import BaseConfig
from config.defaults import settings as default_settings
from config.exceptions import NoConfigFilesFound, InvalidConfigFilePath


logger = logging.getLogger(__name__)


def _read_yaml_from_file(path=None):
    """
    Reads and validates a given file. If valid, returns a Python
    representation of the file's contents.
    """
    if not path:
        msg = 'Cannot read configuration file with invalid path: %s' % path
        raise InvalidConfigFilePath(msg)

    with open(path, 'r') as f:
        data = safe_load(f)
        logger.info('Successfully read configuration from: %s', path)

    return data


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
        if not path:
            if self._write_path:
                path = self._write_path  # fall-back to path set on __init__()
            else:
                msg = "Cannot write configuration. Invalid path: %s" % path
                raise InvalidConfigFilePath(msg)

        with open(path, 'w') as f:
            safe_dump(self._config, f)

        logger.info("Configuration saved to: %s", path)

    def load(self, path=None):
        """
        Reads the configuration from all files matching the given `path`
        pattern. By default, all files matching `config*.yaml` will be read in
        alphanumerical order.
        """
        # Container for configuration read from file(s)
        new_config = {}

        # Apply defaults to the new configuration
        new_config.update(default_settings)

        paths = self._list_files(path)
        if not paths:
            raise NoConfigFilesFound

        logger.debug('The following configuration files were found: %s', paths)

        for p in paths:
            data = _read_yaml_from_file(p)
            # TODO: Validate data before using it
            new_config.update(data)

        self._config = new_config

    def _list_files(self, path=None):
        """
        Lists all files which match the given `path`.
        """
        if not path:
            if self._read_path:
                path = self._read_path  # fall-back to path set on __init__()
            else:
                msg = 'Cannot list configuration files. Invalid path: %s' % path
                logger.warning(msg, path)
                return []

        paths = glob.glob(path)
        if len(paths) == 0:
            msg = 'No configuration files found which match the path: %s'
            logger.warning(msg, path)
            return []

        sorted_paths = sorted(paths)  # Ensure a consistent, deterministic order
        return sorted_paths
