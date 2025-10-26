from textual import on
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Input, MaskedInput, Select
import datetime
from TaskManager import Task

class ModalScreenOfCreatingTask(ModalScreen[Task]):

    BINDINGS = [
        ("escape", "dismiss()", "Вернуться")
    ]

    def __init__(self, disciplines: list[str], name=None, id=None, classes=None):
        super().__init__(name, id, classes)
        self.disciplines = disciplines
        self.task_name = ""
        self.task_discipline = ""
        self.task_description = ""
        self.task_deadline = ""
        self.task_priority = ""

    def compose(self) -> ComposeResult:    
        yield Grid(
            Input(self.task_name, placeholder="Введите название задачи", id="task_name"),
            Select.from_values(self.disciplines, prompt="Выберите дисциплину", id="task_discipline"),
            Select.from_values([1, 2, 3, 4], prompt="Выберите приоритет", id="task_priority"),
            Input(self.task_description, placeholder="Введите описание (опционально)", id="task_description"),
            MaskedInput("99.99.99", placeholder="DD.MM.YY", value=self.task_deadline, id="task_date"),
            Button("Сохранить", variant="primary", id="Save"),
            Button("Cancel", variant="error", id="cancel"), id="dialog"
        )

    @on(Select.Changed, "#task_discipline")
    def select_changed(self, event: Select.Changed) -> None:
        self.task_discipline = event.value
        
    @on(Select.Changed, "#task_priority")
    def select_changed(self, event: Select.Changed) -> None:
        self.task_priority = event.value

    @on(Input.Changed)
    def input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "task_name":  # You'll need to add id to your Input widgets
            self.task_name = event.value
        elif event.input.id == "task_description":
            self.task_description = event.value

    @on(MaskedInput.Changed, "#task_date")
    def date_changed(self, event: MaskedInput.Changed) -> None:
        self.task_deadline = event.value

    def on_button_pressed(self, event: Button.Pressed) -> None:
        def is_name_valid():
            return self.task_name != ""
        
        if event.button.id == "Save":
            if (not is_name_valid()):
                self.notify('Имя задачи является обязательным')
            else:
            # Create and return the Task
                self.dismiss(Task(
                    name=self.task_name,
                    discipline=self.task_discipline,
                    description=self.task_description,
                    deadline=self.task_deadline,
                    priority=self.task_priority
                ))
        elif event.button.id == "cancel":
            self.dismiss(None)

    def exit(self):
        self.dismiss(None)