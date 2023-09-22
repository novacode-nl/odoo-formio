# Copyright 2023 Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import logging
import uuid

from odoo.http import request

_logger = logging.getLogger(__name__)


def generate_uuid4():
    return str(uuid.uuid4())


def log_with_data(msg, data):
    msg = '[DEBUG data] {url}\n\n{msg}:\n{data}'.format(
        url=request.httprequest.url,
        msg=msg,
        data=data
    )
    _logger.info(msg)


def log_form_submisssion(form, debug_mode=True):
    log = False
    if debug_mode and form.debug_mode:
        log = True
    elif not debug_mode:
        log = True
    # log it
    if log:
        submission_data = json.loads(form.submission_data)
        log_with_data(
            'Submission data',
            json.dumps(submission_data, indent=4, sort_keys=True)
        )
