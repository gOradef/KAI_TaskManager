from textual.binding import Binding
from textual.widgets import Label, Header, Footer, ListView, ListItem

from textual import on
from TaskManager import TaskManager
from textual.app import App as TUI, ComposeResult
from Vault import Vault
from widgets.CreateNewTask import ModalScreenOfCreatingTask
from TaskManager import Task

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
        def check_task(task: Task | None) -> None:
            if task is not None:
                self.taskManager.createNewTask(task)
                self.update_task_list()  # Call a method to update the list
    
        self.push_screen(ModalScreenOfCreatingTask(self.taskManager.disciplines), check_task)

    def action_exit_app(self):
        self.vault.save()
        self.exit()

    def update_task_list(self):
        """Update the ListView with current tasks"""
        list_view = self.query_one("#list_view_all")
        list_view.clear()
        
        # Add all current tasks to the ListView
        for task in self.taskManager.tasks:
            # Use task.name if task is an object, or task["name"] if it's a dict
            task_name = task.name if hasattr(task, 'name') else task.get("name", "Unnamed Task")
            list_view.append(ListItem(Label(task_name)))

    def compose(self) -> ComposeResult:
        # Yield other main widgets
        yield Header()
        yield Footer()

        # list_view_disciplines = ListView(*[ListItem(Label(task["name"])) for task in self.taskManager.disciplines])
        list_view_all = ListView(*[ListItem(Label(task["name"])) for task in self.taskManager.tasks], id = "list_view_all")

        yield list_view_all

        for value in self.taskManager.disciplines:
            yield Label(value)

    def on_mount(self) -> None:
        self.screen.styles.background = "#333"
        TUI.title = f"Active vault: '{self.vault.meta.name}'"
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

    def start(self):
        self.run()