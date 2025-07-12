import pytest
from .ckstop import CKStopCommand
from app.models.ckstop import CKStop as CKStopModel
from pydantic import ValidationError
from unittest.mock import MagicMock

class TestCKStopCommand:
    COMMAND: str = "mock-command"    
    file_structure_mock: CKStopModel = CKStopModel(
        node=3,
        paths=[[1, 2, 1]],
        start=1,
        end=3,
        max_steps=5
    )    
        
    def test_valid_initialization(self):
        ckstop_command = CKStopCommand()
        ckstop_command.COMMAND = MagicMock(return_value=self.COMMAND)
        assert ckstop_command.COMMAND() == self.COMMAND
        
        ckstop_command.file_structure = MagicMock(return_value=self.file_structure_mock)
        assert ckstop_command.file_structure() == self.file_structure_mock
        
        ckstop_command.paths_found = []
        assert ckstop_command.paths_found == []
        
    def test_invalid_initialization(self):
        ckstop_command = CKStopCommand()
        mock_file_structure = {
            "node": "test",
            "paths": [[1, 2, 1]],
            "start": 1,
            "end": 10,
            "max_steps": 5
        }
        
        with pytest.raises(ValidationError) as e:
            file_structure = CKStopModel(**mock_file_structure)
            ckstop_command.file_structure = file_structure
                    
        assert str(e.value) == "1 validation error for CKStop\nnode\n  Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='test', input_type=str]\n    For further information visit https://errors.pydantic.dev/2.11/v/int_parsing"
            

    def test_find(self):
        ckstop_command = CKStopCommand()
        ckstop_command.file_structure = self.file_structure_mock
        assert ckstop_command.find() == []
        
    def test_find_shortest_path_with_distance(self):
        ckstop_command = CKStopCommand()
        ckstop_command.file_structure = self.file_structure_mock
        result_mock = [['1 -> 2', 1, 1], ['1 -> 3', 2, 2]]
        assert ckstop_command.find_shortest_path_with_distance(result_mock) == result_mock[0]
        
    def test_find_shortest_distance(self):
        ckstop_command = CKStopCommand()
        ckstop_command.file_structure = self.file_structure_mock
        result_mock = [['1 -> 2', 1, 1], ['1 -> 3', 2, 2]]
        assert ckstop_command.find_shortest_distance(result_mock) == result_mock[0]
        
    def test_start(self):
        ckstop_command = CKStopCommand()
        ckstop_command.file_structure = self.file_structure_mock
        ckstop_command.find_shortest_path_with_distance = MagicMock(return_value=['1 -> 2', 1, 1])
        ckstop_command.find_shortest_distance = MagicMock(return_value=['1 -> 2', 1, 1])
        assert ckstop_command.start() == None
        
    def test_path_finder(self):
        ckstop_command = CKStopCommand()
        ckstop_command.file_structure = self.file_structure_mock
        ckstop_command.path_finder(1, 3, [], [[1, 2, 1]], '1 -> 2', 1, 1)        
        assert True
        
    def test_path_findet_done(self):
        ckstop_command = CKStopCommand()
        ckstop_command.file_structure = self.file_structure_mock
        ckstop_command.path_finder(3, 3, [], [[1, 2, 1]], '1 -> 2', 1, 1)
        assert True
        
    def test_find_shortest_path_with_max_steps(self):
        ckstop_command = CKStopCommand()
        ckstop_command.file_structure = self.file_structure_mock
        result_mock = [['1 -> 2', 1, 1], ['1 -> 3', 2, 2]]
        assert ckstop_command.find_shortest_path_with_max_steps(result_mock) == result_mock[0]