import argparse
from Vault import *
from TaskManager import TaskManager
from Interface import TextualApp


class App:
    Vault: Vault
    taskManager: TaskManager
    interface: TextualApp

    def __init__(self):
        self.Vault = Vault()
        self.taskManager = self.Vault.taskManager #todo is it nescecary?
        self.interface = TextualApp(self.Vault.taskManager)

    def run(self):
        self.interface.start()
    def dump(self):
        Vault.save()

def setup():
    parser = argparse.ArgumentParser(description="App for tracking your tasks :)")
    parser.add_argument("--vault_path", type=str, help="The path of vault to load")

    args = parser.parse_args()

    if args.vault_path:
        Vault.VAULT_PATH = args.vault_path
        print(f'Using custom location for vault: {Vault.VAULT_PATH}')
    else:
        print(f'Using default location for vault: {Vault.VAULT_PATH}')



def init():
    app = App()
    app.run()
    return app

def dump(app: App):
    app.dump()