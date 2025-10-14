import argparse
from Vault import *
from Interface import TextualApp


class App:
    vault: Vault
    interface: TextualApp

    def __init__(self):
        self.vault = Vault()
        self.interface = TextualApp(self.vault)

    def run(self):
        self.interface.start()

    def dump(self):
        self.vault.save()


def setup():
    parser = argparse.ArgumentParser(description="App for tracking your tasks :)")
    parser.add_argument("--vault_path", type=str, help="The path of vault to load")

    args = parser.parse_args()

    if args.vault_path:
        Config.VAULT_PATH = args.vault_path
        print(f'Using custom location for vault: {Config.VAULT_PATH}')
    else:
        print(f'Using default location for vault: {Config.VAULT_PATH}')


def init():
    app = App()
    app.run()
    return app


def dump(app: App):
    app.dump()