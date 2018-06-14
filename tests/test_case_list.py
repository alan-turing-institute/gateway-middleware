"""
Tests for the case api
"""

# pylint: disable=I0011, W0611, W0621, W0613

from pytest import raises
from werkzeug.exceptions import HTTPException, NotFound

from routes import CaseApi, CasesApi
from .decorators import request_context
from .fixtures import demo_app as app


@request_context('/case/1')
def test_get_case_routing(app):
    """
    Test that a basic query of gets the specific case
    """
    result = app.dispatch_request()
    assert result.status_code == 200
    # Data here is the JSON string
    assert result.data is not None
    assert len(result.data) > 0


@request_context('/case/5')
def test_get_no_such_case(app):
    """
    Test that it fails to get a case that doesn't exist
    """
    with raises(NotFound):
        app.dispatch_request()


@request_context('/case/dog')
def test_get_string_casename(app):
    """
    Test that getting a case that isn't a number fails
    """
    with raises(NotFound):
        app.dispatch_request()


@request_context('/')
def test_get_case_1(app):
    """
    Get get case 1 and make sure you get something
    sensible back
    """
    result = CaseApi().dispatch_request(1)
    assert len(result.data['fields']) > 0
    assert result.data['id'] == 1


@request_context('/case?per_page=1', method='GET')
def test_1_per_page(app):
    """
    Make sure that asking for one thing only gives you the first
    """
    result = CasesApi().dispatch_request()
    assert len(result.data) == 1
    assert result.data[0]['id'] == 3
    assert result.data[0].get('fields') is None


@request_context('/case?per_page=dog')
def test_per_page_string(app):
    """
    Test that giving a string to per page fails
    """
    with raises(HTTPException):
        CasesApi().dispatch_request()


@request_context('/case?page=5')
def test_per_page_end(app):
    """
    Test that going of the end of pages still works
    """
    result = CasesApi().dispatch_request()
    assert len(result.data) == 0


@request_context('/case', method='GET')
def test_per_page(app):
    """
    Make sure you get multiple cases if you ask without limiting
    """
    result = CasesApi().dispatch_request()
    # print(result.data)
    assert len(result.data) == 1


@request_context('/case?per_page=1&page=1', method='GET')
def test_1_per_page_page_1(app):
    """
    Make sure that if you ask for the first page of 1 per page
    results you get the first case
    """
    result = CasesApi().dispatch_request()
    assert len(result.data) == 1
    assert result.data[0]['id'] == 3
    assert result.data[0].get('fields') is None
