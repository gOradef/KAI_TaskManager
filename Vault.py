import datetime
from dataclasses import dataclass
from doctest import debug
from io import TextIOWrapper
from pathlib import Path

from TaskManager import TaskManager
import json

class Vault:
    VAULT_PATH = './vault.json'

    @dataclass
    class MetaData:
        name: str
        version: str
        last_updated: str

    taskManager: TaskManager

    def __init__(self):
        if not(Path(self.VAULT_PATH).is_file()):
            raise FileNotFoundError(f'No vault found for path: {self.VAULT_PATH}')

        with open(self.VAULT_PATH, 'r', encoding='utf-8-sig') as file:
            self.VAULT_J = json.load(file)

        self.meta = self.MetaData(
            name=self.VAULT_J['meta']['name'],
            version = self.VAULT_J['meta']['version'],
            last_updated = self.VAULT_J['meta']['last_updated']
        )
        self.taskManager = TaskManager(self.VAULT_J["data"])

    def createNewVault(self):
        pass

    def Save(self):
        pass
