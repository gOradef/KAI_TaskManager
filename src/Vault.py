from dataclasses import dataclass
from pathlib import Path
from datetime import datetime
import json

from TaskManager import TaskManager


class Vault:
    VAULT_PATH = './vault.json'

    @dataclass
    class MetaData:
        name: str
        version: str
        last_updated: str

    taskManager: TaskManager
    meta: MetaData

    def __init__(self):
        if not Path(self.VAULT_PATH).is_file():
            self.createNewVault()

        with open(self.VAULT_PATH, 'r', encoding='utf-8-sig') as file:
            self.VAULT_J = json.load(file)

        self.meta = self.MetaData(
            name=self.VAULT_J['meta']['name'],
            version=self.VAULT_J['meta']['version'],
            last_updated=self.VAULT_J['meta']['last_updated']
        )
        self.taskManager = TaskManager(self.VAULT_J["data"])

    def createNewVault(self):
        default_data = {
            "meta": {
                "name": "My Task Vault",
                "version": "1.0",
                "last_updated": datetime.now().isoformat()
            },
            "data": {
                "disciplines": ["Math", "Physics", "Programming"],
                "tasks": []
            }
        }
        with open(self.VAULT_PATH, 'w') as f:
            json.dump(default_data, f, indent=2)

    def save(self):
        # Update metadata
        self.meta.last_updated = datetime.now().isoformat()

        # Prepare data for saving
        save_data = {
            "meta": {
                "name": self.meta.name,
                "version": self.meta.version,
                "last_updated": self.meta.last_updated
            },
            "data": {
                "disciplines": self.taskManager.disciplines,
                "tasks": [task.to_dict() for task in self.taskManager.tasks]
            }
        }

        with open(self.VAULT_PATH, 'w') as f:
            json.dump(save_data, f, indent=2)
        print(f"Vault saved to {self.VAULT_PATH}")