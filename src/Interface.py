from textual.binding import Binding
from textual.widgets import Welcome, Label, Button, Header, Footer

from textual import on
from TaskManager import TaskManager
from textual.app import App as TUI
from textual import events
from Vault import Vault
class TextualApp(TUI):
    CSS_PATH = "style/dom.css"
    TUI.NOTIFICATION_TIMEOUT = 2.5

    vault: Vault
    taskManager: TaskManager

    BINDINGS = [
        # Optional
        # Binding("ctrl+q", "none", "None", show=False, priority=True),
        # Binding("ctrl+c", "quit", "Quit", show=False, priority=True),

        ("c", "create_new_task()", "Create new task"),
        ("f", "search_menu()", "Search menu"),
        ("h", "home_page()", "Open home page"),
    ]
    def action_search_menu(self):
        self.notify("AYOOOOOOOO")
    def action_home_page(self):
        pass
    def action_create_new_task(self):
        pass


    def on_mount(self) -> None:
        self.screen.styles.background = "#333"
        TUI.title = f'Active vault: \'{self.vault.meta.name}\''
        TUI.sub_title = f'last update: {self.vault.meta.last_updated}'
        self.mount(Header())
        self.mount(Footer())

        for dis in self.taskManager.disciplines:
            self.mount(Button(dis, classes="discipline_btn", id=f'd_{self.taskManager.disciplines.index(dis)}'))

    def __init__(self, user_vault: Vault):
        super().__init__()
        self.vault = user_vault
        self.taskManager = self.vault.taskManager

    @on(Button.Pressed, ".discipline_btn")
    def exit_app(self):
        self.exit()

    def start(self):
        self.run()