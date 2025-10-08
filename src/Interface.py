import textual.widgets
from textual.binding import Binding
from textual.layouts.horizontal import HorizontalLayout
from textual.layouts.vertical import VerticalLayout
from textual.widgets import Welcome, Label, Button, Header, Footer, ListView, ListItem

from textual import on
from TaskManager import TaskManager
from textual.app import App as TUI, ComposeResult
from textual import events
from Vault import Vault
class TextualApp(TUI):
    CSS_PATH = "style/dom.css"
    TUI.NOTIFICATION_TIMEOUT = 2.5

    vault: Vault
    taskManager: TaskManager

    BINDINGS = [
        # Optional
        Binding("ctrl+q", "exit_app", "Save & Quit", show=False, priority=True),

        ("c", "create_new_task()", "Create new task"),
        ("e", "edit_task()", "Edit selected task"),
        ("f", "search_menu()", "Search menu"),
        ("h", "home_page()", "Open home page"),
    ]
    def action_search_menu(self):
        self.notify("AYOOOOOOOO")
    def action_home_page(self):
        self.refresh()
    def action_create_new_task(self):
        for obj in self.taskManager.disciplines:
            self.mount(Label(obj["id"]))
            self.mount(Label(obj["name"]))

    def action_exit_app(self):
        self.vault.save()
        self.exit()

    def compose(self) -> ComposeResult:
        # Yield other main widgets
        yield Header()
        yield Footer()

        list_view_all = ListView(*[ListItem(Label(task["name"])) for task in self.taskManager.tasks])

        # with HorizontalLayout():
        #     with VerticalLayout():
        #         yield list_view_all
        #     with VerticalLayout():
        yield list_view_al    def on_mount(self) -> None:
        # Set up styles and titles here
        self.screen.styles.background = "#333"
        TUI.title = f'Active vault: \'{self.vault.meta.name}\''
        TUI.sub_title = f'last update: {self.vault.meta.last_updated}'

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        # Get the selected item
        selected_item = event.item
        # Get the index
        selected_index = event.list_view.index
        # Do something with the selection
        self.notify(f"Selected: {self.taskManager.tasks[selected_index]['name']}")

    def __init__(self, user_vault: Vault):
        super().__init__()
        self.vault = user_vault
        self.taskManager = self.vault.taskManager

    @on(Button.Pressed, ".discipline_btn")
    def exit_app(self):
        pass
    def start(self):
        self.run()