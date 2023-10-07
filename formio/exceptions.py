# Copyright 2023 Nova Code (https://www.novacode.nl)
# See LICENSE file for full licensing details.

from werkzeug.exceptions import BadRequest


class BadCSRF(BadRequest):
    pass
