"""
This module stores common args definitions
"""

from webargs import fields

pagination_args = {
    'page': fields.Int(missing=1, strict=True, validate=lambda p: p > 0),
    'per_page': fields.Int(missing=10, strict=True, validate=lambda p: p > 0)
}
