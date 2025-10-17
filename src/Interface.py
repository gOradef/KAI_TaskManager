from textual.binding import Binding
from textual.widgets import Label, Header, Footer, ListView, ListItem

from textual import on
from TaskManager import TaskManager
from textual.app import App as TUI, ComposeResult
from Vault import Vault
from widgets.CreateNewTask import ModalScreenOfCreatingTask
from widgets.EditTask import ModalScreenOfEditingTask
from widgets.editDisciplines import DisciplineEditor
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
        ("Enter", "", "Edit selected task"),
        ("m", "mark_as_completed()", "Mark as completed"),
        ("e", "edit_disciplines()", "Edit list of disciplines"),
        ("f", "search_menu()", "filter by .."),
        ("h", "home_page()", "Open home page"),
    ]

    selected_task: Task

    def action_search_menu(self):
        self.notify(self.taskManager.tasks_filter_expired)
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

    def action_mark_as_completed(self):
        list_view = self.query_one("#list_view_all", ListView)  # Replace with your ListView ID
        if list_view.has_focus:
            # ListView is focused
            selected_index = list_view.index
            if selected_index is not None:
                # Mark the selected task as completed
                task = self.taskManager.tasks[selected_index]
                self.taskManager.markAsCompletedTask(task.id)
                self.update_task_list()
                self.notify(f"Задача '{task.name}' отмечена как выполненная")
        else:
            self.notify("Сначала выберите задачу из списка")
    def action_edit_disciplines(self):
        def handle_disciplines_result(result: list[str]) -> None:
            if result is not None:
                # User pressed Save - update disciplines
                self.taskManager.disciplines = result
                self.notify("Дисциплины обновлены", severity="success")
        # else: User pressed Cancel - do nothing
    
        self.push_screen(
            DisciplineEditor(self.taskManager.disciplines.copy()),
            handle_disciplines_result
        )

    def update_task_list(self):
        """Update the ListView with current tasks"""
        list_view = self.query_one("#list_view_all")
        list_view.clear()
        
        # Add all current tasks to the ListView
        for task in self.taskManager.tasks:
            task_name = task.name if hasattr(task, 'name') else task.get("name", "Unnamed Task")
            
            # Get task status
            if hasattr(task, 'status'):
                task_status = task.status
            else:
                task_status = task.get("status", "TODO")
            
            # Add appropriate icon based on status
            if task_status == Task.Status.COMPLETED or task_status == "COMPLETED":
                display_text = f"✅ {task_name}"
            elif task_status == Task.Status.IN_PROGRESS or task_status == "IN_PROGRESS":
                display_text = f"🔄 {task_name}"
            elif task_status == Task.Status.TODO or task_status == "TODO":
                display_text = f"📝 {task_name}"
            else:
                display_text = f"❓ {task_name}"
            
            list_view.append(ListItem(Label(display_text)))

    def compose(self) -> ComposeResult:
        # Yield other main widgets
        yield Header()
        yield Footer()

        # Create list items with completion hints
        list_items = []
        for task in self.taskManager.tasks:
            # Get task status
            if hasattr(task, 'status'):
                task_status = task.status
            else:
                task_status = task.get("status", "TODO")
            
            # Add completion hint
            if task_status == Task.Status.COMPLETED or task_status == "COMPLETED":
                display_text = f"✅Y {task.name}"
            else:
                display_text = f"📝 {task.name}"
            
            list_items.append(ListItem(Label(display_text)))

        list_view_all = ListView(*list_items, id="list_view_all")
        yield list_view_all

    def on_mount(self) -> None:
        self.screen.styles.background = "#333"
        TUI.title = f"Active vault: '{self.vault.meta.name}'"
        TUI.sub_title = f'last update: {self.vault.meta.last_updated}'

    @on(ListView.Selected, "#list_view_all")
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        def insertTask(task: Task):
            if task is not None:
                for i, existing_task in enumerate(self.taskManager.tasks):
                    if existing_task.id == task.id:
                        self.taskManager.tasks[i] = task
                        break
                else:
                    self.taskManager.tasks.append(task)
                
                self.update_task_list()
    
        selected_index = event.list_view.index    
        self.selected_task: Task = self.taskManager.tasks[selected_index]
        self.push_screen(ModalScreenOfEditingTask(self.taskManager.disciplines, self.selected_task), insertTask)

    def __init__(self, user_vault: Vault):
        super().__init__()
        self.vault = user_vault
        self.taskManager = self.vault.taskManager

    def start(self):
        self.run()