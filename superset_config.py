# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

#
# This file is included in the final Docker image and SHOULD be overridden when
# deploying the image to prod. Settings configured here are intended for use in local
# development environments. Also note that superset_config_docker.py is imported
# as a final step as a means to override "defaults" configured here
#

import logging
import os

from cachelib.file import FileSystemCache
from celery.schedules import crontab

logger = logging.getLogger()


def get_env_variable(var_name, default=None):
    """Get the environment variable or raise exception."""
    try:
        return os.environ[var_name]
    except KeyError:
        if default is not None:
            return default
        else:
            error_msg = "The environment variable {} was missing, abort...".format(
                var_name
            )
            raise EnvironmentError(error_msg)

AUTH_TYPE = 1
SQLALCHEMY_DATABASE_URI = "postgresql://graph:graph@23.251.145.120:5432/superset"

BABEL_DEFAULT_LOCALE = "en"

LANGUAGES = {
    "en": {"flag": "us", "name": "English"},
    "ru": {"flag": "ru", "name": "Russian"},
}

EXCEL_EXTENSIONS = {"xlsx", "xls"}
CSV_EXTENSIONS = {"csv", "tsv", "txt"}
ALLOWED_EXTENSIONS = {*CSV_EXTENSIONS, *EXCEL_EXTENSIONS}

CSV_EXPORT = {"encoding": "utf-8"}

LOGO_TARGET_PATH = "/welcome"
WEBDRIVER_TYPE = "chrome"

CACHE_CONFIG = {
    'CACHE_TYPE': 'redis',
    'CACHE_DEFAULT_TIMEOUT': 60 * 60 * 12,
    'CACHE_KEY_PREFIX': 'superset_results',
    'CACHE_REDIS_URL': 'redis://localhost:9999/0',
}

CELERYBEAT_SCHEDULE = {
    'cache-warmup-hourly': {
        'task': 'cache-warmup',
        'schedule': crontab(minute=0, hour='*'),
        'kwargs': {
            'strategy_name': 'top_n_dashboards',
            'top_n': 5,
            'since': '7 days ago',
        },
    },
}
