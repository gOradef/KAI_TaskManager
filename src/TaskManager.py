import datetime
import uuid
from enum import Enum

class Task:    
    class Status(Enum):
        TODO = "TODO"
        IN_PROGRESS = "IN_PROGRESS"
        COMPLETED = "COMPLETED"
        ARCHIVED = "ARCHIVED"


    id: str
    discipline: str
    name: str
    status: Status
    description: str
    deadline: str

    def __init__(self, name, discipline, description = None, deadline = None, id = None):
        if id is not None:
            self.id = id
        else:
            self.id = uuid.uuid4().__str__()
        self.status = self.Status.TODO

        self.name = name
        self.discipline = discipline
        self.description = description
        self.deadline = deadline

    # def __str__(self):
    #     return {
    #         "id": self.id,
    #         "discipline": self.discipline,
    #         "name": self.name,
    #         "desciption": self.description,
    #         "status": self.status.value,
    #         "deadline": self.deadline
    #     }

class TaskManager:
    disciplines: list[str]
    tasks : list[Task]
    
    def tasks_filter_expired(self):
        def isValid(task: Task):
            return datetime.datetime.strptime(task["deadline"], "%Y-%m-%d") < datetime.datetime.today()
        
        filtered_tasks = list(filter(isValid, self.tasks))

        return filtered_tasks
        
    def tasks_filter_week(self):
        def isValid():
            pass
        pass
    def tasks_filter_weekPlus(self):
        def isValid():
            pass
        pass

    def __init__(self, data):
        self.disciplines: list[str] = data["disciplines"]
        # self.tasks: list[Task] = list[Task](data["tasks"]) # Is it uses

        self.tasks = list()
        for task in data["tasks"]:
            self.tasks.append(Task(id=task["id"],
                                   name= task["name"],
                                   discipline=task["discipline"],
                                   description=task["description"],
                                   deadline=task["deadline"]))
            

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