# Copyright Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

import json
import logging
import uuid

from odoo.http import MISSING_CSRF_WARNING, request

from ..exceptions import BadCSRF


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


def validate_csrf(request):
    post = request.get_json_data()
    token = post.pop('csrf_token', None)
    if not request.validate_csrf(token):
        if token is not None:
            _logger.warning("CSRF validation failed on path '%s'", request.httprequest.path)
        else:
            _logger.warning(MISSING_CSRF_WARNING, request.httprequest.path)
        raise BadCSRF('Session expired (invalid CSRF token)')
