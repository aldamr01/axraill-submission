import pytest
from pydantic import ValidationError

from .ckstop import CKStop

def test_valid_ckstop_model():
    data = {
        "node": 1,
        "paths": [[1, 2, 3], [4, 5, 6]],
        "start": 1,
        "end": 10,
        "max_steps": 5
    }
    ckstop = CKStop(**data)
    assert ckstop.node == 1
    assert ckstop.paths == [[1, 2, 3], [4, 5, 6]]
    assert ckstop.start == 1
    assert ckstop.end == 10
    assert ckstop.max_steps == 5

def test_invalid_node_type():
    data = {
        "node": "test",
        "paths": [[1, 2, 3]],
        "start": 1,
        "end": 10,
        "max_steps": 5
    }
    with pytest.raises(ValidationError):
        CKStop(**data)

def test_invalid_paths_type():
    data = {
        "node": 1,
        "paths": "string",
        "start": 1,
        "end": 10,
        "max_steps": 5
    }
    with pytest.raises(ValidationError):
        CKStop(**data)

def test_invalid_paths_attributes_type():
    data = {
        "node": 1,
        "paths": [[1, "tets", 3]],
        "start": 1,
        "end": 10,
        "max_steps": 5
    }
    with pytest.raises(ValidationError):
        CKStop(**data)

def test_negative_values():
    data = {
        "node": -1,
        "paths": [[-1, -2, -3]],
        "start": -5,
        "end": -1,
        "max_steps": -10
    }
    with pytest.raises(ValidationError):
        CKStop(**data)