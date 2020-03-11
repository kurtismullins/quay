# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from random import SystemRandom
from uuid import uuid4


def generate_secret_key():
    """
    Generates a strong, pseudo-random secret key that can be used for encryption
    purposes. The keys created here should only be generated once, as needed,
    and then stored and read from the configuration file afterwards.
    """
    cryptogen = SystemRandom()
    return str(cryptogen.getrandbits(256))


settings = {

    # Site Settings
    'TESTING': False,
    'USE_CDN': False,
    'REGISTRY_TITLE': 'ProjectQuay',
    'REGISTRY_TITLE_SHORT': 'ProjectQuay',

    # Feature Flags
    'FEATURE_USER_LOG_ACCESS': True,
    'FEATURE_USER_CREATION': True,
    'FEATURE_ANONYMOUS_ACCESS': True,
    'FEATURE_REQUIRE_TEAM_INVITE': True,
    'FEATURE_CHANGE_TAG_EXPIRATION': True,
    'FEATURE_DIRECT_LOGIN': True,
    'FEATURE_APP_SPECIFIC_TOKENS': True,
    'FEATURE_PARTIAL_USER_AUTOCOMPLETE': True,
    'FEATURE_USERNAME_CONFIRMATION': True,
    'FEATURE_RESTRICTED_V1_PUSH': True,
    'FEATURE_MAILING': False,
    'FEATURE_BUILD_SUPPORT': False,
    'FEATURE_ACI_CONVERSION': False,
    'FEATURE_APP_REGISTRY': False,
    'FEATURE_REPO_MIRROR': False,
    'FEATURE_SECURITY_NOTIFICATIONS': True,
    'FEATURE_SECURITY_SCANNER': False,

    'REPO_MIRROR_TLS_VERIFY': True,
    'REPO_MIRROR_SERVER_HOSTNAME': True,
    'DEFAULT_TAG_EXPIRATION': '2w',
    'MAIL_USE_TLS': True,
    'MAIL_PORT': 587,
    'MAIL_DEFAULT_SENDER': 'support@quay.io',
    'AUTHENTICATION_TYPE': 'Database',
    'SECRET_KEY': generate_secret_key(),
    'DATABASE_SECRET_KEY': generate_secret_key(),
    'BITTORRENT_FILENAME_PEPPER': str(uuid4()),
    'DISTRIBUTED_STORAGE_PREFERENCE': ['default'],
    'DISTRIBUTED_STORAGE_CONFIG': {
        'default': [
            'LocalStorage',
            {
                'storage_path': '/datastorage/registry'
            }
        ]
    },
    'USERFILES_LOCATION': 'default',
    'USERFILES_PATH': 'userfiles/',
    'LOG_ARCHIVE_LOCATION': 'default',
    'PREFERRED_URL_SCHEME': 'http',
    'ENTERPRISE_LOGO_URL': '/static/img/quay-horizontal-color.svg',
    'TEAM_RESYNC_STALE_TIME': '60m',

}
