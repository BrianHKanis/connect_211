from build_tables.tables import make_request, build_dict
import pytest

def test_make_request():
    response = make_request('organizations')
    assert response.status_code == 200
