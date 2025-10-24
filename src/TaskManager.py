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
    priority: int # 1 - is higher, 4 - is lowest prio
    deadline: str

    def __init__(self, name, discipline, description = None, status = None, priority = None, deadline = None, id = None):
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

class TaskManager:
    disciplines: list[str]
    tasks : list[Task]

    class Filter:
        class FilterTypes(Enum):
            EXPIRED = (-1, "Просрочено")
            TODAY = (0, "Сегодня")
            WEEK = (1, "В течение недели")
            FUTURE = (2, "В будущем")
            ALL = (3, "Все")

        @classmethod
        def get_next_filter(cls, current_filter):
            filters = list(cls.FilterTypes)
            current_index = filters.index(current_filter)
            next_index = (current_index + 1) % len(filters)
            return filters[next_index]

        def get_tasks_with_filter(self, filterType: FilterTypes):
            def getTimeOfTask(task: Task) -> datetime.datetime:
                return datetime.datetime.strptime(task.deadline, "%d.%m.%y")

            def filter_task(task: Task) -> bool:
                pass
            def isValid(task: Task): # foo prototype for filtering tasks
                if task.deadline == "":
                    return True
                return filter_task(task)

            match filterType:
                case self.FilterTypes.EXPIRED:
                    def isExpired(task: Task):
                        return getTimeOfTask(task) < datetime.datetime.today()
                    filter_task = isExpired
                case self.FilterTypes.TODAY:
                    def isToday(task: Task):
                        return getTimeOfTask(task) == datetime.datetime.today()
                    filter_task = isToday
                case self.FilterTypes.WEEK:
                    pass # TODO
                case self.FilterTypes.FUTURE:
                    pass
                case self.FilterTypes.ALL:
                    pass

            return list(filter(isValid, self._get_tasks_list())) # filtered tasks

        def get_tasks_filter_expired(self):
            def isValid(task: Task):
                return datetime.datetime.strptime(task["deadline"], "%Y-%m-%d") < datetime.datetime.today()
            
            filtered_tasks = list(filter(isValid, self._get_tasks_list()))

            return filtered_tasks

        def get_tasks_filter_expired(self):
            def isValid(task: Task):
                return datetime.datetime.strptime(task["deadline"], "%Y-%m-%d") < datetime.datetime.today()
            
            filtered_tasks = list(filter(isValid, self._get_tasks_list()))

            return filtered_tasks



        def __init__(self, Parent):
            self.parent_ref = Parent

        def _get_tasks_list(self) -> list[Task]:
            return self.parent_ref.tasks

        def get_tasks_filter_week(self):
            def isValid():
                pass
            pass
        def get_tasks_filter_weekPlus(self):
            def isValid():
                pass
            pass

    def __init__(self, data):
        self.disciplines: list[str] = data["disciplines"]
        self.filters = self.Filter(self)
        self.tasks = list()
        for task in data["tasks"]:
            self.tasks.append(Task(id=task["id"],
                                   name= task["name"],
                                   discipline=task["discipline"],
                                   description=task["description"],
                                   status=task["status"],
                                   priority=task["priority"],
                                   deadline=task["deadline"]))
            

    # Category: disciplines
    def addNewDiscipline(self, newDiscipline: str):
        self.disciplines.append(newDiscipline)

    def deleteDiscipline(self, discipline):
        # filtered_d = [obj for obj in self.disciplines if obj["id"] == disciplineId]
        self.disciplines.remove(discipline)

    # Category: tasks
    def createNewTask(self, task: Task):
        self.tasks.append(task)

    def setDescriptionToTask(self, task_id, task_description):
        self.tasks[task_id].description = task_description
    def markAsInProgressTask(self, task_id):
        self.tasks[task_id].status = Task.Status.IN_PROGRESS
    def markAsCompletedTask(self, task_id):
        """Mark a task as completed by its ID"""
        for task in self.tasks:
            # Handle both Task objects and dictionaries
            task_id_to_check = task.id if hasattr(task, 'id') else task.get('id')
            if task_id_to_check == task_id:
                if hasattr(task, 'status'):
                    task.status = task.Status.COMPLETED  # or Task.Status.COMPLETED depending on your import
                break
        else:
            # Task not found
            print(f"Task with ID {task_id} not found")