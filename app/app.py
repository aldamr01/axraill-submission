from .commands.ckstop import CKStopCommand

class App:
    def __init__(self):
        ckstop_instance = CKStopCommand()
        
        self.instance_commands = {
            ckstop_instance.COMMAND: ckstop_instance,
        }
        
        self.default_commands = {
            "exit": exit,
            "q": exit,
        }
        
    def route(self, command: str) -> None:
        commands = self.instance_commands.keys() | self.default_commands.keys()
        if command in commands:
            if command in self.instance_commands:
                self.instance_commands[command].start()
            else:
                match command:
                    case "exit":
                        exit()
                    case "q":
                        exit()
                    case _:
                        print("Command not found")
        else:
            print("Command not found")
            return None
        
    def list_commands(self) -> None:
        commands = self.instance_commands.keys()
        print("Available Commands:")
        for command in commands:
            print(f" > {command}\n")
        
    def start(self) -> None:
        
        self.list_commands()
        
        while True:
            command = input("command: ")
            self.route(command)
            