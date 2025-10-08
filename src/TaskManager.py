import datetime
import uuid
from enum import Enum

class Discipline:
    id: uuid.UUID
    name: str
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return {
            "id": self.id,
            "name": self.name
        }

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
    disciplines: list[Discipline]
    tasks : list[Task]
    def __init__(self, data):
        self.disciplines = data["disciplines"]
        self.tasks: list[Task] = data["tasks"]

    # Category: disciplines
    def addNewDiscipline(self, newDiscipline: Discipline):
        self.disciplines.append(newDiscipline)

    def deleteDiscipline(self, disciplineId):
        # filtered_d = [obj for obj in self.disciplines if obj["id"] == disciplineId]
        self.disciplines.remove(Discipline(disciplineId))

    # Category: tasks
    def addNewTask(self, discipline, name):
        self.tasks.append(Task(discipline, name))

    def setDescriptionToTask(self, task_id, task_description):
        self.tasks[task_id].description = task_description
    def markAsInProgressTask(self, task_id):
        self.tasks[task_id].status = Task.Status.IN_PROGRESS
    def markAsCompletedTask(self, task_id):
        self.tasks[task_id].status = Task.Status.COMPLETE