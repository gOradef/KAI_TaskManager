import datetime
from datetime import date
import uuid
from enum import Enum

class Task:    
    class Status(Enum):
        TODO = "TODO"
        IN_PROGRESS = "IN_PROGRESS"
        COMPLETED = "COMPLETED"
        ARCHIVED = "ARCHIVED"


    id: str
    name: str
    discipline: str
    status: Status # Uses Status Enum
    isArchived: bool
    description: str
    priority: int # 1 - is higher, 4 - is lowest prio
    deadline: str

    def __init__(self, name, discipline, 
                isArchived = False,
                 description = None,
                  status = None, 
                  priority = None, 
                  deadline = None, 
                  id = None):
        if id is not None:
            self.id = id
        else:
            self.id = uuid.uuid4().__str__()
        if status == None:
            self.status = Task.Status.TODO
        else:
            self.status = status

        self.name = name
        self.discipline = discipline
        self.description = description
        self.priority = priority
        self.deadline = deadline
        self.isArchived = isArchived

class TaskManager:
    disciplines: list[str]
    tasks: list[Task]
    current_tasks: list[Task]
    class Filter:
        class FilterTypes(Enum): #provides tuple(index, display_name)
            ARCHIVED =  (-1, "Архив")
            EXPIRED =   (0, "Просрочено")
            TODAY =     (1, "Сегодня")
            WEEK =      (2, "В течение недели")
            ALL =       (3, "Все")

        parent_ref: super = None #ref to taskManager object

        @classmethod
        def get_next_filter(cls, current_filter):
            filters = list(cls.FilterTypes)
            current_index = filters.index(current_filter)
            next_index = (current_index + 1) % len(filters)
            return filters[next_index]

        def get_tasks_with_filter(self, filterType: FilterTypes) -> list[Task]:
            def getDayOfTask(task: Task) -> date:
                if task.deadline == "":
                    return date.max
                return datetime.datetime.strptime(task.deadline, "%d.%m.%y").date()
            today = date.today()
            
            match filterType:
                case self.FilterTypes.ARCHIVED:
                    def filter_task(task: Task):
                        return task.isArchived
                case self.FilterTypes.EXPIRED:
                    def filter_task(task: Task):
                        return task.deadline != "" and getDayOfTask(task) < today and not task.isArchived
                case self.FilterTypes.TODAY:
                    def filter_task(task: Task):
                        return task.deadline != "" and getDayOfTask(task) == today and not task.isArchived
                case self.FilterTypes.WEEK:
                    next_week = today + datetime.timedelta(days=7)
                    def filter_task(task: Task):
                        task_date = getDayOfTask(task)
                        return (task.deadline != "" and 
                            today <= task_date <= next_week and not task.isArchived)
                case self.FilterTypes.ALL:
                    def filter_task(task: Task):
                        return not task.isArchived
            
            filtered_by_period = list(filter(filter_task, self._get_tasks_list()))
            return filtered_by_period
        def __init__(self, Parent):
            self.parent_ref = Parent

        def _get_tasks_list(self) -> list[Task]:
            return self.parent_ref.tasks

        def _get_current_tasks(self) -> list[Task]:
            return self.parent_ref.current_tasks
        def _set_current_tasks(self, tasks: list[Task]) -> None:
            self.parent_ref.current_tasks = tasks

    def __init__(self, data):
        def setStatusAsEnum(task):
            match task["status"]:
                case "TODO":
                    return Task.Status.TODO
                case "IN_PROGRESS":
                    return Task.Status.IN_PROGRESS
                case "COMPLETED":
                    return Task.Status.COMPLETED

        self.disciplines: list[str] = data["disciplines"]
        self.filters = self.Filter(self)
        self.tasks = list()
        for task in data["tasks"]:
            self.tasks.append(Task(id=task["id"],
                                   name= task["name"],
                                   discipline=task["discipline"],
                                   isArchived=task["isArchived"],
                                   description=task["description"],
                                   status=setStatusAsEnum(task),
                                   priority=task["priority"],
                                   deadline=task["deadline"]))
            

    # Category: disciplines
    def addNewDiscipline(self, newDiscipline: str):
        self.disciplines.append(newDiscipline)

    def deleteDiscipline(self, discipline):
        self.disciplines.remove(discipline)

    # Category: tasks
    def createNewTask(self, task: Task):
        self.tasks.append(task)
        
    def markAsTask(self, task_id, task_status: Task.Status):
        for task in self.tasks:
            if task.id == task_id:
                task.status = task_status 
    def moveToArchiveTask(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.isArchived = True 
    def removeFromArchiveTask(self, task_id):
        for task in self.tasks:
            if task.id == task_id:
                task.isArchived = False 
