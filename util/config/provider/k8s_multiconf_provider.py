# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os

from util.config.provider.baseprovider import BaseProvider, get_yaml


# Barrowed from `k8sprovider.py`.
# TODO(kmullins): This should not be hard-coded here. If anything, perhaps a config default.
# TODO(kmullins): Determine if this is always available, and if there's a better way to handle this.
SERVICE_ACCOUNT_TOKEN_PATH = "/var/run/secrets/kubernetes.io/serviceaccount/token"

# The namespace to search for the Secret.
# TODO(kmullins): The fallback/default should not be hard-coded here. Perhaps a config default.
QE_NAMESPACE = os.environ.get("QE_K8S_NAMESPACE", "quay-enterprise")

# The name of the secret to use.
# TODO(kmullins): The fallback/default should not be hard-coded here. Perhaps a config default.
QE_CONFIG_SECRET = os.environ.get("QE_K8S_CONFIG_SECRET", "quay-enterprise-config-secret")


class KubernetesMultiConfProvider(BaseProvider):
    """
    Kubernetes Config Provider which can also read from all files matching a particular glob pattern.
    """
    def __init__(self, config_volume, yaml_filename, py_filename, api_host=None,
                 service_account_token_path=None, additional_config_pattern="config*.yaml"):
        
        # Load the Kubernetes Service Account Token
        service_account_token_path = service_account_token_path or SERVICE_ACCOUNT_TOKEN_PATH
        if not os.path.exists(service_account_token_path):
            raise Exception("Cannot load Kubernetes service account token")
        with open(service_account_token_path, 'r') as f:
            self._service_token = f.read()
        
