from textual import on
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.screen import ModalScreen
from textual.widgets import Button, Input, DataTable, Label, Static, Footer
from textual.reactive import reactive
from typing import Optional

class DisciplineEditor(ModalScreen[list[str]]):
    """Modal screen for editing disciplines list using DataTable."""
    
    BINDINGS = [
        ("escape", "cancel_edits", "Cancel"),
        ("a", "add_discipline", "Add"),
        ("d", "delete_discipline", "Delete"),
        ("s", "save_disciplines", "Save"),
    ]
    
    disciplines = reactive(list)
    
    def __init__(self, disciplines: list[str], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_disciplines = disciplines.copy()
        self.disciplines = disciplines.copy()
        self.selected_row: Optional[int] = None

    def compose(self) -> ComposeResult:
        with Vertical(id="discipline-container"):
            yield Label("📚 Управление дисциплинами", classes="title")
            
            # Add new discipline section
            with Horizontal(classes="input-section"):
                yield Input(
                    placeholder="Название новой дисциплины...", 
                    id="new-discipline-input"
                )
                yield Button("➕ Добавить", variant="primary", id="add-btn")
            
            # Disciplines table
            yield Label("📋 Список дисциплин:", classes="subtitle")
            yield DataTable(id="disciplines-table")
        yield Footer()
            
    def on_mount(self) -> None:
        """Initialize the data table when the screen mounts."""
        table = self.query_one("#disciplines-table", DataTable)
        table.add_column("№", width=4)
        table.add_column("Название дисциплины", width=30)
        table.cursor_type = "row"
        
        self.populate_table()
        self.query_one("#new-discipline-input", Input).focus()

    def populate_table(self) -> None:
        """Populate the data table with current disciplines."""
        table = self.query_one("#disciplines-table", DataTable)
        table.clear()
        
        for i, discipline in enumerate(self.disciplines, 1):
            table.add_row(str(i), discipline, key=str(i))
        
    @on(Input.Changed, "#new-discipline-input")
    def on_new_discipline_changed(self, event: Input.Changed) -> None:
        """Enable/disable add button based on input."""
        add_btn = self.query_one("#add-btn", Button)
        add_btn.disabled = not event.value.strip()

    @on(DataTable.RowSelected, "#disciplines-table")
    def on_row_selected(self, event: DataTable.RowSelected) -> None:
        """Handle row selection in the data table."""
        if event.row_key is not None:
            # Extract the value from RowKey object
            row_key_value = event.row_key.value
            self.selected_row = int(row_key_value) - 1  # Convert back to 0-based index
            
            if 0 <= self.selected_row < len(self.disciplines):
                selected_discipline = self.disciplines[self.selected_row]

    @on(DataTable.RowHighlighted, "#disciplines-table")
    def on_row_highlighted(self, event: DataTable.RowHighlighted) -> None:
        """Handle row highlighting (keyboard navigation)."""
        if event.row_key is not None:
            # Extract the value from RowKey object
            row_key_value = event.row_key.value
            self.selected_row = int(row_key_value) - 1
            
            if 0 <= self.selected_row < len(self.disciplines):
                selected_discipline = self.disciplines[self.selected_row]

    @on(Button.Pressed, "#add-btn")
    def add_discipline(self) -> None:
        """Add a new discipline."""
        input_widget = self.query_one("#new-discipline-input", Input)
        new_discipline = input_widget.value.strip()
        
        if not new_discipline:
            self.notify("Введите название дисциплины", severity="warning")
            return
            
        if new_discipline in self.disciplines:
            self.notify("❌ Дисциплина с таким названием уже существует", severity="warning")
            return
        
        self.disciplines.append(new_discipline)
        self.populate_table()
        input_widget.value = ""
        self.query_one("#add-btn", Button).disabled = True
        self.notify(f"✅ Дисциплина '{new_discipline}' добавлена", severity="information")
        
        # Auto-focus back to input
        input_widget.focus()

    @on(Button.Pressed, "#delete-btn")
    def delete_discipline(self) -> None:
        """Delete the selected discipline."""
        if self.selected_row is None:
            self.notify("❌ Выберите дисциплину для удаления", severity="warning")
            return
            
        deleted_discipline = self.disciplines[self.selected_row]
        self.disciplines.pop(self.selected_row)
        self.populate_table()
        self.notify(f"✅ Дисциплина '{deleted_discipline}' удалена", severity="information")
        
        self.clear_selection()

    def clear_selection(self) -> None:
        """Clear current selection and reset edit fields."""
        self.selected_row = None
        
        table = self.query_one("#disciplines-table", DataTable)
        if table.row_count > 0:
            table.cursor_coordinate = (0, 0)
        
        self.query_one("#new-discipline-input", Input).focus()

    @on(Button.Pressed, "#save-btn")
    def save_disciplines(self) -> None:
        """Save changes and dismiss the screen."""
        self.dismiss(self.disciplines)

    @on(Button.Pressed, "#cancel-btn")
    def cancel_edits(self) -> None:
        """Cancel editing and dismiss without changes."""
        self.dismiss(None)

    # Keyboard shortcut actions
    def action_add_discipline(self) -> None:
        """Add discipline via keyboard shortcut."""
        self.add_discipline()

    def action_delete_discipline(self) -> None:
        """Delete discipline via keyboard shortcut."""
        self.delete_discipline()

    def action_save_disciplines(self) -> None:
        """Save disciplines via keyboard shortcut."""
        self.save_disciplines()

    def action_cancel_edits(self) -> None:
        """Cancel edits via keyboard shortcut."""
        self.cancel_edits()