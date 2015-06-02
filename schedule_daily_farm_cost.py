#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
"""

__author__ = "pure"

import os
import json
import re
import sys
import fileinput
from datetime import datetime, timedelta, date
import struct

def farm_cost():
    """update user's balance for each farm who owned.
    """
    logger.debug('update_farm_cost: begin...')
    try:
        update_farm_cost()
    except Exception, e:
        logger.error("===update_farm_cost: " + str(e))
    logger.debug('update_farm_cost: end...')

if __name__ == "__main__":

    setting_module = "farm.settings"
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", setting_module)

    from django.conf import settings
    import logging
    from apps.helper import update_farm_cost
    logger = logging.getLogger("apps")
    farm_cost()
        


