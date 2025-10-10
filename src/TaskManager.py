import datetime
import uuid
from enum import Enum

class Task:
    class Status(Enum):
        TODO = 0
        IN_PROGRESS = 1
        COMPLETE = 2
        ARCHIVED = 3


    id: str
    discipline: str
    name: str
    status: Status
    description: str
    deadline: datetime.date

    def __init__(self, name, discipline, description = None, deadline = None):
        self.id = uuid.uuid4().__str__()
        self.status = self.Status.TODO

        self.name = name
        self.discipline = discipline
        self.description = description
        self.deadline = deadline

    def __str__(self):
        return {
            "id": self.id,
            "discipline": self.discipline,
            "name": self.name,
            "status": self.status.value,
            "deadline": self.deadline.__str__()
        }

class TaskManager:
    disciplines: list[str]
    tasks : list[Task]
    def __init__(self, data):
        self.disciplines: list[str] = data["disciplines"]
        self.tasks: list[Task] = list[Task](data["tasks"])

    # Category: disciplines
    def addNewDiscipline(self, newDiscipline: str):
        self.disciplines.append(newDiscipline)

    def deleteDiscipline(self, discipline):
        # filtered_d = [obj for obj in self.disciplines if obj["id"] == disciplineId]
        self.disciplines.remove(discipline)

    # Category: tasks
    def createNewTask(self, task: Task):
        self.tasks.append(task.__str__())

    def setDescriptionToTask(self, task_id, task_description):
        self.tasks[task_id].description = task_description
    def markAsInProgressTask(self, task_id):
        self.tasks[task_id].status = Task.Status.IN_PROGRESS
    def markAsCompletedTask(self, task_id):
        self.tasks[task_id].status = Task.Status.COMPLETE