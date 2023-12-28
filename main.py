import sys
from PySide2.QtCore import QTimer
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction, QMessageBox


class OpusFocus(QSystemTrayIcon):
    def __init__(self):
        super().__init__()

        self.icon = QIcon("icon.png")
        self.setIcon(self.icon)
        self.setVisible(True)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)

        self.todo_list = []

        self.menu = QMenu()
        self.action_add_todo = QAction("Add todo")
        self.action_remove_todo = QAction("Remove todo")
        self.action_show_todo_list = QAction("Show todo list")
        self.action_clear_todo_list = QAction("Clear todo list")

        self.action_add_todo.triggered.connect(self.add_todo)
        self.action_remove_todo.triggered.connect(self.remove_todo)
        self.action_show_todo_list.triggered.connect(self.show_todo_list)
        self.action_clear_todo_list.triggered.connect(self.clear_todo_list)

        self.menu.addActions([
            self.action_add_todo,
            self.action_remove_todo,
            self.action_show_todo_list,
            self.action_clear_todo_list,
        ])

        self.setContextMenu(self.menu)

        self.update_timer()

    def update_timer(self):
        current_time = datetime.now()
        self.statusTip(f"OpusFocus: {current_time}")

        for todo in self.todo_list:
            if todo["due_date"] <= current_time:
                QMessageBox.warning(
                    None,
                    "To-Do-Erinnerung",
                    f"Die To-Do-Liste '{todo['title']}' ist fällig.",
                )

    def add_todo(self):
        todo_title = input("To-Do-Titel eingeben: ")
        due_date = input("To-Do-Fälligkeitsdatum eingeben (YYYY-MM-DD): ")

        todo = {
            "title": todo_title,
            "due_date": datetime.strptime(due_date, "%Y-%m-%d"),
        }

        self.todo_list.append(todo)
        self.update_todo_list()

    def remove_todo(self):
        todo_index = int(input("To-Do-Index zum Entfernen eingeben: "))

        self.todo_list.pop(todo_index)
        self.update_todo_list()

    def show_todo_list(self):
        for todo in self.todo_list:
            print(f"* {todo['title']} (fällig am {todo['due_date']})")

    def clear_todo_list(self):
        self.todo_list = []
        self.update_todo_list()

    def update_todo_list(self):
        self.menu.clear()

        for todo in self.todo_list:
            action = QAction(todo["title"], self)
            action.triggered.connect(lambda: self.show_todo_details(todo))
            self.menu.addAction(action)

    def show_todo_details(self, todo):
        QMessageBox.information(
            None,
            "To-Do-Details",
            f"* Titel: {todo['title']}\n* Fälligkeitsdatum: {todo['due_date']}",
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    opusfocus = OpusFocus()

    sys.exit(app.exec_())
