import os
import sys
import subprocess

class Shell:
    BUILTIN_COMMANDS = ["type", "exit", "echo", "pwd", "cd", "ls", "clear", "history"]

    def __init__(self):
        self.command_history = []

    def run(self):
        self.clear_screen()
        path = os.environ.get("PATH", "")
        while True:
            try:
                self.prompt()
                command = self.get_command()

                if command == "exit 0":
                    self.handle_exit()
                elif command.startswith("echo "):
                    self.handle_echo(command)
                elif command.startswith("type "):
                    self.handle_type(command, path)
                elif command == "pwd":
                    self.handle_pwd()
                elif command.startswith("cd "):
                    self.handle_cd(command)
                elif command == "ls":
                    self.handle_ls()
                elif command == "clear":
                    self.clear_screen()
                elif command == "history":
                    self.handle_history()
                elif command == "":
                    pass
                else:
                    self.execute_command(command)
            except KeyboardInterrupt:
                sys.stdout.write("\nExiting...\n")
                sys.exit(0)

    def prompt(self):
        sys.stdout.write("\033[92m$\033[0m ")
        sys.stdout.flush()

    def get_command(self):
        command = input().strip()
        self.command_history.append(command)
        return command

    def handle_exit(self):
        sys.exit(0)

    def handle_echo(self, command):
        sys.stdout.write(command[len("echo "):] + "\n")

    def handle_type(self, command, path):
        command_name = command[len("type "):]
        if command_name in self.BUILTIN_COMMANDS:
            sys.stdout.write(f"{command_name} is a shell builtin\n")
        else:
            found = False
            for directory in path.split(":"):
                command_path = os.path.join(directory, command_name)
                if os.path.exists(command_path):
                    sys.stdout.write(f"{command_name} is {command_path}\n")
                    found = True
                    break
            if not found:
                sys.stdout.write(f"{command_name}: not found\n")

    def handle_pwd(self):
        sys.stdout.write(os.getcwd() + "\n")

    def handle_cd(self, command):
        directory = command[len("cd "):].strip()
        try:
            if directory == "":
                os.chdir(os.path.expanduser("~"))
            else:
                os.chdir(directory)
        except FileNotFoundError:
            sys.stdout.write(f"cd: {directory}: No such file or directory\n")

    def handle_ls(self):
        files = os.listdir()
        for file in files:
            sys.stdout.write(f"{file}\n")

    def clear_screen(self):
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()

    def handle_history(self):
        for idx, cmd in enumerate(self.command_history, start=1):
            sys.stdout.write(f"{idx}: {cmd}\n")

    def execute_command(self, command):
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError:
            sys.stdout.write(f"{command}: command not found\n")

if __name__ == "__main__":
    shell = Shell()
    shell.run()
