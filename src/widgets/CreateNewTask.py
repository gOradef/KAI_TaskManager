from textual import on
from textual.app import ComposeResult
from textual.containers import Grid
from textual.screen import ModalScreen
from textual.widgets import Button, Input, MaskedInput, Select
import datetime
from TaskManager import Task

class ModalScreenOfCreatingTask(ModalScreen[Task]):
    def __init__(self, disciplines: list[str], name=None, id=None, classes=None):
        super().__init__(name, id, classes)
        self.disciplines = disciplines
        self.task_name = ""
        self.task_discipline = ""
        self.task_description = ""
        self.task_deadline = datetime.date.today()  # Fixed: use actual date, not module

    def compose(self) -> ComposeResult:    
        yield Grid(
            Input(self.task_name, placeholder="Введите название задачи", id="task_name"),
            Select.from_values(self.disciplines, prompt="Выберите дисциплину"),
            Input(self.task_description, placeholder="Введите описание (опционально)", id="task_description"),
            MaskedInput("99.99.9999", placeholder="DD.MM.YY", value=self.task_deadline.strftime("%d-%m-%y")),
            Button("Сохранить", variant="primary", id="Save"),
            Button("Cancel", variant="error", id="cancel"),
            id="dialog"
        )

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        self.task_discipline = event.value

    @on(Input.Changed)
    def input_changed(self, event: Input.Changed) -> None:
        if event.input.id == "task_name":  # You'll need to add id to your Input widgets
            self.task_name = event.value
        elif event.input.id == "task_description":
            self.task_description = event.value

    @on(MaskedInput.Changed)
    def date_changed(self, event: MaskedInput.Changed) -> None:
        try:
            # Parse the date string from MaskedInput
            if event.value and len(event.value) == 10:  # YYYY-MM-DD format
                year, month, day = map(int, event.value.split('-'))
                self.task_deadline = datetime.date(year, month, day)
        except (ValueError, AttributeError):
            # Handle invalid date
            pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "Save":
            # Create and return the Task
            self.dismiss(Task(
                name=self.task_name,
                discipline=self.task_discipline,
                description=self.task_description,
                deadline=self.task_deadline
            ))
        elif event.button.id == "cancel":
            self.dismiss(None)