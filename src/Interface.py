from textual.widgets import Welcome, Label, Button

from textual import on
from TaskManager import TaskManager
from textual.app import App as TUI
from textual import events

class TextualApp(TUI):
    CSS_PATH = "style/dom.css"
    taskManager: TaskManager

    def on_mount(self) -> None:
        self.screen.styles.background = "#333"
        for dis in self.taskManager.disciplines:
            self.mount(Button(dis, classes="discipline_btn", id=f'd_{self.taskManager.disciplines.index(dis)}'))

    def __init__(self, task_manager: TaskManager):
        super().__init__()
        self.taskManager = task_manager

    def on_key(self, event: events.Key) -> None:
        if event.character == "p":
            self.mount(Welcome())

    @on(Button.Pressed, ".discipline_btn")
    def exit_app(self):
        self.exit()

    def start(self):
        self.run()