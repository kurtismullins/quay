# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

try:
    from collections.abc import MutableMapping  # Python 3
except ImportError:
    from collections import MutableMapping  # Python 2.7


logger = logging.getLogger(__name__)


class BaseConfig(MutableMapping):
    """
    Base class for all configuration managers.
    """

    # The container for the configuration data.
    _config = None

    # The location to write the config when save() is called unless the
    # value of `location` is overridden.
    _write_path = None

    # The pattern of configuration files to read from when load() is called
    # unless the `location_glob` is overridden.
    _read_path = None

    def __init__(self, write_path=None, read_path=None):
        """
        On initialization, the BaseConfig will read the existing configuration
        from the persistence layer.
        """
        logger.debug('Initializing empty configuration.')
        self._config = {}

        # Store the read and write locations for later.
        self._write_path = write_path
        self._read_path = read_path

        # Initial load of configuration data.
        if read_path:
            logger.debug('Loading configuration data from path: %s', read_path)
            self.load(path=read_path)
        else:
            msg = (
              'Falling back to default configuration values. '
              'No configuration file(s) specified.'
            )
            logger.warning(msg)

    def save(self, path=None):
        """
        Writes the current configuration to a persistent location. This may
        be a file, a kubernetes secret, or any other persistence mechanism.
        NOTE: The `location` will be overwritten with the current configuration.

        path: The filename or other reference to where the configuration should
              be stored.
        """
        raise NotImplementedError

    def load(self, path=None):
        """
        Reads the configuration from persistent storage and updates this
        instance's `dict` values accordingly.

        path: A pattern which may match one or more filenames. When read, the
              file(s) should be loaded in alphanumerical order to ensure
              consistent and deterministic order for the purpose of overriding a
              base configuration in the correct order.
        """
        raise NotImplementedError

    def to_yaml(self):
        """
        Converts the contents of the current configuration to a YAML string.
        """
        raise NotImplementedError("TODO: Implement me")

    def to_json(self):
        """
        Returns a JSON representation of the configuration.
        """
        raise NotImplementedError("TODO: Implement me")

    def __delitem__(self, key):
        del self._config[key]

    def __getitem__(self, key):
        return self._config.get(key)

    def __iter__(self):
        return iter(self._config)

    def __len__(self):
        return len(self._config)

    def __setitem__(self, key, value):
        self._config[key] = value