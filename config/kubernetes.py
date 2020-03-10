# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals, with_statement

from config.base import BaseConfig


class KubernetesSecretConfig(BaseConfig):
    """
    A configuration object which uses a kubernetes secret for persisting the
    configuration.
    """

    def save(self, location='config.yaml'):
        """
        Writes the configuration to the configured kubernetes "secret" where
        the key equals the `location` and the value is the base64-encoded
        contents of the YAML configuration data.

        location: The key within the kubernetes secret to write the YAML
                  file contents using base64 encoding.
        """
        raise NotImplementedError

    def load(self, location_glob="config*.yaml"):
        """
        Reads the configuration from the kubernetes "secret" by finding all
        keys which match the `location_glob` pattern. It is expected that these
        values are all base64-encoded YAML.

        location_glob: The pattern used to determine which keys to read.
        """
        raise NotImplementedError