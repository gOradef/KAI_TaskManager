from textual.binding import Binding
from textual.widgets import Label, Header, Footer, ListView, ListItem, Static, Tabs, Tab

from textual import on
from TaskManager import TaskManager
from textual.app import App as TUI, ComposeResult
from Vault import Vault
from widgets.CreateNewTask import ModalScreenOfCreatingTask
from widgets.EditTask import ModalScreenOfEditingTask
from widgets.editDisciplines import DisciplineEditor
from TaskManager import Task
from datetime import date, datetime

class TextualApp(TUI):
    CSS_PATH = "style/dom.css"
    TUI.NOTIFICATION_TIMEOUT = 3

    vault: Vault
    taskManager: TaskManager

    BINDINGS = [
        # Optional
        Binding("ctrl+q", "exit_app", "Save & Quit", show=False, priority=True),

        ("c", "create_new_task()", "Create new task"),
        ("Enter", "", "Edit selected task"),
        ("a", "archive_task()", "[de]archive task"),
        ("m", "mark_as()", "Mark as ..."),
        ("f", "filter_by_discipline()", "filter by discipline"),
        # ("shift+f", "previous_tab()", "filter by .."),
        ("e", "edit_disciplines()", "Edit list of disciplines"),
        ("h", "home_page()", "Open home page")
        # ("Esc", "exit_app()", "Exit") #TODO Remove from prod
    ]

    selected_task: Task
    current_filter: TaskManager.Filter.FilterTypes

    def renderTasks(self):
        def get_sorted_task_list(tasks: list[Task]) -> list[Task]:
            """Updated listview with provided tasks"""            
            def sort_key(task: Task):
                # TODO > IN_PROGRESS > COMPLETED > ARCHIVED
                status_order = {
                    Task.Status.TODO: 0,
                    Task.Status.IN_PROGRESS: 1,
                    Task.Status.COMPLETED: 2,
                    Task.Status.ARCHIVED: 3
                }
                
                try:
                    deadline_date = datetime.strptime(task.deadline, "%d.%m.%y").date() if task.deadline else datetime.max.date()
                except (ValueError, AttributeError):
                    deadline_date = datetime.max.date()
                
                return (
                    status_order[task.status],  # Primary: status
                    task.priority if task.priority != "" else 5, # Secondary: priority (1=highest)
                    deadline_date               # Tertiary: deadline (earliest first)
                )
                
            return sorted(tasks, key=sort_key)
        
        def get_task_class(task: Task):
            """Determine CSS class based on days until deadline"""
            if not task.deadline or not task.deadline.strip():
                return "chill"  # No deadline set
            
            try:
                deadline_date = datetime.strptime(task.deadline, "%d.%m.%y").date()
                today = date.today()
                days_until_deadline = (deadline_date - today).days
                
                if days_until_deadline < 0:
                    return "danger"  # Overdue
                elif days_until_deadline == 0:
                    return "danger"  # Due today
                elif days_until_deadline <= 2:
                    return "danger"  # 1-2 days left
                elif days_until_deadline <= 7:
                    return "warning"  # 3-7 days left
                elif days_until_deadline <= 14:
                    return "okey"  # 8-14 days left
                else:
                    return "chill"  # More than 14 days left
                    
            except (ValueError, AttributeError):
                return "chill"  # Invalid date format

        def get_days_text(task):
            """Get formatted text showing days until deadline"""
            if not task.deadline or not task.deadline.strip():
                return "Срока нет"
            
            deadline_date = datetime.strptime(task.deadline, "%d.%m.%y").date()
            today = date.today()
            days_until_deadline = (deadline_date - today).days
            
            if days_until_deadline < 0:
                return f"Просрочено на {-days_until_deadline}д"
            elif days_until_deadline == 0:
                return "Сегодня"
            elif days_until_deadline == 1:
                return "Остался 1 день"
            else:
                return f"Осталось {days_until_deadline}д"

        def display_task_list(self, tasks: list[Task]) -> None:
            list_view = self.query_one("#list_view_all")
            list_view.clear()

            for task in tasks:
                task_name = task.name
                task_status = task.status
                display_text = f""
                
                class_text = get_task_class(task)
                days_text = get_days_text(task)

                match task_status:
                    case Task.Status.COMPLETED:
                        display_text = f"✅ {task_name}"
                    case Task.Status.IN_PROGRESS:
                        display_text = f"🔄 {task_name}"
                    case Task.Status.TODO:
                        display_text = f"📝 {task_name}"
                
                if task.isArchived:
                    display_text = f"🗑️  {task_name}"
                    
                # Include both deadline date and days left text
                list_view.append(ListItem(Label(display_text + f" | {task.deadline}", classes=class_text),
                                          Label(f'({days_text}) [i]{str("\n" + task.discipline) if task.discipline != "" else ""}[/i]', classes=class_text)))

        tasks_filtered = self.taskManager.filters.get_tasks_with_filter(self.current_filter)
        tasks_sorted = get_sorted_task_list(tasks_filtered)
        self.taskManager.filters._set_current_tasks(tasks_sorted)
        display_task_list(self, tasks_sorted)

    def action_home_page(self):
        self.refresh()

    def action_create_new_task(self):
        def check_task(task: Task | None) -> None:
            if task is not None:
                self.taskManager.createNewTask(task)
                self.renderTasks()
    
        self.push_screen(ModalScreenOfCreatingTask(self.taskManager.disciplines), check_task)
    
    def action_exit_app(self):
        self.vault.save()
        self.exit()

    def action_archive_task(self):
        list_view = self.query_one("#list_view_all", ListView)  # Replace with your ListView ID
        if list_view.has_focus:
            # ListView is focused
            selected_index = list_view.index
            if selected_index is not None:
                # Mark the selected task as completed
                task = self.taskManager.current_tasks[selected_index]
                msg = f"Задача '{task.name}' "
                if task.isArchived:
                    self.taskManager.removeFromArchiveTask(task.id)
                    msg += "перемещена в архив"
                else:    
                    self.taskManager.moveToArchiveTask(task.id)
                    msg += "перемещена из архива"
                self.renderTasks()
                self.notify(msg)
        else:
            self.notify("Сначала выберите задачу из списка")
    def action_filter_by_discipline(self):
        return NotImplemented #TODO
    def action_mark_as(self):
        list_view = self.query_one("#list_view_all", ListView)  # Replace with your ListView ID
        if list_view.has_focus:
            # ListView is focused
            selected_index = list_view.index
            if selected_index is not None:
                # Mark the selected task as completed
                task = self.taskManager.current_tasks[selected_index]
                msg = f"Задаче '{task.name}' установлен статус: "
                match task.status:
                    case Task.Status.TODO:
                        self.taskManager.markAsTask(task.id, Task.Status.IN_PROGRESS)
                        msg += "в процессе"
                    case Task.Status.IN_PROGRESS:
                        self.taskManager.markAsTask(task.id, Task.Status.COMPLETED)
                        msg += "выполнена"
                    case Task.Status.COMPLETED:
                        self.taskManager.markAsTask(task.id, Task.Status.TODO)
                        msg += "сделать потом"
                self.renderTasks()
                self.notify(msg)
        else:
            self.notify("Сначала выберите задачу из списка")
    def action_edit_disciplines(self):
        def handle_disciplines_result(result: list[str]) -> None:
            if result is not None:
                self.taskManager.disciplines = result
                self.notify("Дисциплины обновлены", severity="success")
    
        self.push_screen(
            DisciplineEditor(self.taskManager.disciplines.copy()),
            handle_disciplines_result
        )

    def compose(self) -> ComposeResult:
        # Yield other main widgets
        yield Header()
        yield Footer()
        yield Tabs(
            Tab("Архив", id="archive"),            
            Tab("Просрочено", id="expired"),
            Tab("Сегодня", id="today"),
            Tab("На неделе", id="week"),
            Tab("Все", id="all")
        )

        list_items = []
        list_view_all = ListView(*list_items, id="list_view_all")
        yield list_view_all

    def on_mount(self) -> None:
        self.screen.styles.background = "#333"
        TUI.title = f"Active vault: '{self.vault.meta.name}'"
        TUI.sub_title = f'last update: {self.vault.meta.last_updated}'

    @on(Tabs.TabActivated)
    def on_tabs_activated(self, event: Tabs.TabActivated) -> None:
        match event.tab.id:
            case "archive":
                self.current_filter = self.taskManager.Filter.FilterTypes.ARCHIVED
            case "expired":
                self.current_filter = self.taskManager.Filter.FilterTypes.EXPIRED
            case "today":
                self.current_filter = self.taskManager.Filter.FilterTypes.TODAY
            case "week":
                self.current_filter = self.taskManager.Filter.FilterTypes.WEEK
            case "all":
                self.current_filter = self.taskManager.Filter.FilterTypes.ALL
                
        self.renderTasks()

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
                
                self.renderTasks()
    
        selected_index = event.list_view.index    
        self.selected_task: Task = self.taskManager.current_tasks[selected_index]
        self.push_screen(ModalScreenOfEditingTask(self.taskManager.disciplines, self.selected_task), insertTask)

    def __init__(self, user_vault: Vault):
        super().__init__()
        self.vault = user_vault
        self.taskManager = self.vault.taskManager
        self.current_filter = TaskManager.Filter.FilterTypes.EXPIRED
        self.current_list_group_name = self.current_filter.value

    def start(self):
        self.run()