import pytest
from unittest.mock import patch, MagicMock
from io import StringIO
from .app import App
from .commands.ckstop import CKStopCommand

class TestApp:
    @pytest.fixture
    def app(self):
        return App()
    
    def test_valid_initialization(self, app):        
        assert 'ckstop' in app.instance_commands
        assert isinstance(app.instance_commands['ckstop'], CKStopCommand)
        assert 'exit' in app.default_commands
        assert 'q' in app.default_commands
        
    def test_route(self, app):        
        app.instance_commands['ckstop'].start = MagicMock()
        app.route('ckstop')
        app.instance_commands['ckstop'].start.assert_called_once()
        
    def test_invalid_command(self, app):
        with patch('sys.stdout', new=StringIO()) as fake_output:
            app.route('invalid_command')
            assert fake_output.getvalue().strip() == "Command not found"
            
    def test_list_commands(self, app):        
        with patch('sys.stdout', new=StringIO()) as fake_output:
            app.list_commands()
            output = fake_output.getvalue()
            assert "Available Commands:" in output
            assert "ckstop" in output
        
    def test_exit_command(self, app):
        with pytest.raises(SystemExit):
            app.route('exit')
            
    def test_q_command(self, app):
        with pytest.raises(SystemExit):
            app.route('q') 