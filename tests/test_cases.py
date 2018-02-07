#! /usr/bin/env python3
"""
The main entry point for this flask app
"""

from routes import CasesApi, CaseApi

from .decorators import request_context
from .fixtures import demo_app as app


@request_context("/")
def test_get_case(app):
    """
    Test that a basic query of gets lots of cases
    """
    result = CaseApi().dispatch_request(1)
    assert(len(result.data['fields']) > 0)
    assert(result.data['id'] == 1)


@request_context("/case?per_page=1", method="GET")
def test_1_per_page(app):
    result = CasesApi().dispatch_request()
    assert(len(result.data) == 1)
    assert(result.data[0]['id'] == 1)
    assert(result.data[0].get('fields') is None)


@request_context("/case", method="GET")
def test_per_page(app):
    result = CasesApi().dispatch_request()
    assert(len(result.data) == 3)


@request_context("/case?per_page=1&page=2", method="GET")
def test_1_per_page_page_2(app):
    result = CasesApi().dispatch_request()
    assert(len(result.data) == 1)
    assert(result.data[0]['id'] == 2)
    assert(result.data[0].get('fields') is None)
