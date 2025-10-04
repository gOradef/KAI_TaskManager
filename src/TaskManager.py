import datetime
import uuid
from enum import Enum


class Task:
    class Status(Enum):
        TODO = 0
        IN_PROGRESS = 1
        COMPLETE = 2
        ARCHIVED = 3

    id: uuid.UUID
    discipline: str
    name: str
    status: Status
    description: str
    deadline: datetime.date
    def __init__(self, discipline, name):
        self.id = uuid.uuid4()
        self.discipline = discipline
        self.name = name
        self.status = self.Status.TODO

class TaskManager:
    disciplines: list[str]
    tasks : list[Task]
    def __init__(self, data):
        self.disciplines = data["disciplines"]
        self.tasks: list[Task] = []

    def addNewTask(self, discipline, name):
        self.tasks.append(Task(discipline, name))

