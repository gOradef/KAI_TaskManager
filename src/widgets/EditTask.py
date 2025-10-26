from textual import on
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Input, MaskedInput, Select, Label
import datetime
from TaskManager import Task

class ModalScreenOfEditingTask(ModalScreen[Task]):

    BINDINGS = [
        ("escape", "dismiss()", "Вернуться")
    ]

    def __init__(self, disciplines: list[str], task_to_edit: Task, name=None, id=None, classes=None):
        super().__init__(name, id, classes)
        self.disciplines = disciplines

        self.task_id = task_to_edit.id
        self.task_name = task_to_edit.name
        self.task_discipline = task_to_edit.discipline
        self.task_isArchived = task_to_edit.isArchived
        self.task_description = task_to_edit.description
        self.task_deadline = task_to_edit.deadline
        self.task_priority = task_to_edit.priority

    def compose(self) -> ComposeResult:  

        if self.task_discipline == "":
            self.task_discipline = Select.BLANK  
        elif self.task_discipline not in self.disciplines:
            self.task_discipline = Select.BLANK

        if self.task_priority == "":
            self.task_priority = Select.BLANK
        
        yield Grid(
            Input(self.task_name, placeholder="Название задачи", id="task_name"),
            Select.from_values(self.disciplines, prompt="Дисциплина", value=self.task_discipline),
            Select.from_values([1, 2, 3, 4], prompt="Выберите приоритет", id="task_priority", value=self.task_priority),
            Input(self.task_description, placeholder="Описание (опционально)", id="task_description"),
            MaskedInput("99.99.99", placeholder="DD.MM.YY", value=self.task_deadline, id="task_deadline"),
            Button("Сохранить", variant="primary", id="Save"),
            Button("Cancel", variant="error", id="cancel"),
            id="dialog"
        )

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        self.task_discipline = event.value

    @on(Input.Changed, "#task_deadline")
    def select_changed(self, event: Select.Changed) -> None:
        self.task_deadline = event.value

    @on(MaskedInput.Changed, "#task_name")
    def input_changed(self, event: Input.Changed) -> None:
        self.task_name = event.value

    @on(Input.Changed, "#task_description")
    def input_changed(self, event: Input.Changed) -> None:
        self.task_description = event.value

    def on_button_pressed(self, event: Button.Pressed) -> None:
        def is_name_valid():
            return self.task_name != ""
        
        if event.button.id == "Save":
            if not is_name_valid():
                self.notify('Имя задачи является обязательным')
            else:
            # Create and return the Task
                self.dismiss(Task(
                    id=self.task_id,
                    name=self.task_name,
                    discipline=self.task_discipline,
                    isArchived=self.task_isArchived,
                    description=self.task_description,
                    deadline=self.task_deadline,
                    priority=self.task_priority
                ))
        elif event.button.id == "cancel":
            self.dismiss(None)
    
    def exit(self):
        self.dismiss(None)