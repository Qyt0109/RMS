from Frontend.Helper.buttons import *
from Backend.Services.file_handler import *
from functools import partial
from Backend.Database.sessions import *
from Backend.Services.time import *

import PyQt6
from PyQt6 import QtWidgets

from sqlalchemy.orm import sessionmaker, class_mapper, registry
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import sessionmaker
from collections import defaultdict
import signal
import typing
# PyQt6

from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *


# Paths
icon_logout_path = "Frontend/Resources/Bootstrap/box-arrow-left.png"
icon_database_path = "Frontend/Resources/Bootstrap/database-fill.png"
icon_settings_path = "Frontend/Resources/Bootstrap/gear-fill.png"
icon_select_path = "Frontend/Resources/Bootstrap/arrow-right.png"
icon_application_form_path = "Frontend/Resources/Bootstrap/envelope-paper.png"

icon_search_path = "Frontend/Resources/Bootstrap/search.png"
icon_options_path = "Frontend/Resources/Bootstrap/sliders.png"
icon_home_path = "Frontend/Resources/Bootstrap/house-fill.png"
icon_back_path = "Frontend/Resources/Bootstrap/arrow-left.png"
icon_menu_path = "Frontend/Resources/Bootstrap/list.png"
icon_show_path = "Frontend/Resources/Bootstrap/eye.png"
icon_hide_path = "Frontend/Resources/Bootstrap/eye-slash.png"
icon_edit_path = "Frontend/Resources/Bootstrap/pencil-square.png"
icon_delete_path = "Frontend/Resources/Bootstrap/trash3.png"
icon_user_path = "Frontend/Resources/Bootstrap/person.png"
icon_job_path = "Frontend/Resources/Bootstrap/bookmark.png"
icon_candidate_path = "Frontend/Resources/Bootstrap/mortarboard.png"
icon_interviewer_path = "Frontend/Resources/Bootstrap/person.png"
icon_interviewer_asignment_path = "Frontend/Resources/Bootstrap/journal-bookmark.png"
icon_change_password_path = "Frontend/Resources/Bootstrap/key.png"

LANGUAGE: str = str('en')

translate = {
    'back': {
        'en': 'Back',
        'vi': 'Trở lại'
    },
    'create': {
        'en': 'Create',
        'vi': 'Tạo'
    },
    'created': {
        'en': 'Created successfully!',
        'vi': 'Đã tạo thành công!'
    },
    'cancel': {
        'en': 'Cancel',
        'vi': 'Huỷ'
    },
    'action completed':
    {
        'en': 'Action completed successfully!',
        'vi': 'Thực thi thành công!'
    },
    'action failed':
    {
        'en': 'Failed to do the action!\nPlease check and try again.',
        'vi': 'Thực thi thất bại!\nXin kiểm tra và thử lại.'
    },
    'update': {
        'en': 'Update',
        'vi': 'Cập nhật'
    },
    'delete': {
        'en': 'Delete',
        'vi': 'Xoá'
    },
    'view': {
        'en': 'View',
        'vi': 'Xem'
    },
    'action_button': {
        'en': 'Action Buttons',
        'vi': 'Chức năng'
    },
    'add': {
        'en': 'Add',
        'vi': 'Thêm'
    },
    'home': {
        'en': 'Home',
        'vi': 'Trang chủ'
    },
    'database': {
        'en': 'Database',
        'vi': 'Cơ sở dữ liệu'
    },
    'logout': {
        'en': 'Logout',
        'vi': 'Đăng xuất'
    },
    'login': {
        'en': 'Login',
        'vi': 'Đăng nhập'
    },
    'database': {
        'en': 'Database',
        'vi': 'Cơ sở dữ liệu'
    },
    'settings': {
        'en': 'Settings',
        'vi': 'Cài đặt'
    },
    'candidate': {
        'en': 'Candidate',
        'vi': 'Ứng viên'
    },
    'account_settings': {
        'en': 'Account Settings',
        'vi': 'Cài đặt tài khoản'
    },
    'change_password': {
        'en': 'Change password',
        'vi': 'Đổi mật khẩu'
    }




}


def get_translation(key, language=LANGUAGE):
    """
    Get the translation of a key in a specific language.

    Parameters:
    - key: The key for which translation is needed.
    - language: The language ('en' for English, 'vi' for Vietnamese).

    Returns:
    - The translation of the key in the specified language.
    """
    translation = translate.get(key, {}).get(language, key)

    if not translation:
        print(
            f"No translation available for key '{key}' in language '{language}'")
        return key

    return translation


def initActionButtons(parent_widget: QWidget,
                      action_buttons: list[QPushButton]):
    clearAllWidgets(parent_widget=parent_widget)
    parent_layout = parent_widget.layout()
    for action_button in action_buttons:
        parent_layout.addWidget(action_button)


def getAvaiableJobs(avaiable_job_id: int = 1):
    """ Assuming Job instances with\n#### job_status_id=avaiable_job_id\nis avaiable for anyone """
    status, instances = CRUD_Job.read_by_filter(job_status_id=avaiable_job_id)
    print(status, instances)
    if status != CRUD_Status.FOUND:
        instances = []
    return instances


def clearAllWidgets(parent_widget: QWidget):
    layout = parent_widget.layout()
    if layout:
        while layout.count():
            w = layout.takeAt(0).widget()
            if w:
                w.deleteLater()


def clearLayoutWidgets(layout: QLayout):
    while layout.count():
        widget = layout.takeAt(0).widget()
        if widget:
            widget.deleteLater()


def togglePasswordVisibility(line_edit: QLineEdit, button: QPushButton):
    is_hide = line_edit.echoMode() == QLineEdit.EchoMode.Password
    if is_hide:
        line_edit.setEchoMode(QLineEdit.EchoMode.Normal)
        button.setIcon(QIcon(QPixmap(icon_show_path)))
    else:
        line_edit.setEchoMode(QLineEdit.EchoMode.Password)
        button.setIcon(QIcon(QPixmap(icon_hide_path)))


def setTableTextCell(table: QTableWidget, text: str, row, col):
    qitem = QTableWidgetItem(text)
    qitem.setFlags(qitem.flags() & ~PyQt6.QtCore.Qt.ItemFlag.ItemIsEditable)
    table.setItem(row, col, qitem)


def setTableWidgetCell(table: QTableWidget, widget: QWidget, row, col):
    table.setCellWidget(row, col, widget)


def setTableResizeMode(table: QTableWidget, resize_modes: List[QHeaderView.ResizeMode]):
    for col, resize_mode in enumerate(resize_modes):
        table.horizontalHeader().setSectionResizeMode(col, resize_mode)


def hide_columns_by_header_labels(table_widget: QTableWidget, header_labels: list[str]):
    header = table_widget.horizontalHeader()

    for col in range(table_widget.columnCount()):
        item = header.model().headerData(col, header.orientation())

        if item and item in header_labels:
            table_widget.setColumnHidden(col, True)


def get_id_for_row(table_widget, row):
    header_labels = [table_widget.horizontalHeaderItem(col).text()
                     for col in range(table_widget.columnCount())]

    id_column_index = header_labels.index(
        "id") if "id" in header_labels else -1

    if id_column_index != -1:
        id_item = table_widget.item(row, id_column_index)
        if id_item and id_item.text() != 'None':
            return int(id_item.text())
    return None


def populate_table(table_widget: QTableWidget, instances: list, model):

    # Set the number of rows in the table
    if not instances:
        return
    table_widget.setRowCount(len(instances))

    table_columns = []
    is_user_subclass = issubclass(model, User) and model is not User
    if is_user_subclass:
        user_columns = getattr(User, '__table__', None).columns
        if user_columns:
            table_columns += list(user_columns)
    table_columns += list(model.__table__.columns)
    # Populate the table with data
    for row, instance in enumerate(instances):

        for col, column in enumerate(table_columns):
            """
            if column.primary_key:
                # If the column is the primary key, use the value directly
                item_text = str(getattr(instance, column.name))
            """
            if column.primary_key:
                # If the column is the primary key, use the value directly
                item_text = str(getattr(instance, column.name))
            if getColumnFileType(column=column) == FileTypes.PDF_FILE.value:
                item_text = "PDF file"
            elif column.foreign_keys:
                # Get the class of the related model
                related_model_class = list(column.foreign_keys)[0].column.table
                # Get the foreign key value
                foreign_key_value = getattr(instance, column.name, None)

                # Fetch the corresponding instance using the foreign key value
                related_instance = session.query(
                    related_model_class).filter_by(id=foreign_key_value).first()
                if str(related_model_class) in ['interviewers', 'job_managers', 'candidates', 'admins']:
                    status, user = CRUD_User.read(id=related_instance.id)
                    item_text = str(user.name)
                else:
                    if related_instance:
                        item_text = str(related_instance.name)
                    else:
                        item_text = ''

            else:
                attr = getattr(instance, column.name)
                if attr:
                    item_text = str(attr)
                else:
                    item_text = ''

            item = QTableWidgetItem(item_text)
            table_widget.setItem(row, col, item)


class QSignalVariable(QObject):
    model = any
    stateChanged = pyqtSignal(bool)

    def __init__(self, initial_state=None):
        super().__init__()
        self._state = initial_state

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        if self._state != new_state:
            self._state = new_state
            # Emit signal with True if new_state is not None, False otherwise
            self.stateChanged.emit(new_state is not None)


class Widget_Database(QWidget):
    def __init__(self, parent: QWidget, models, callback_back=None, callback_select_table=None) -> None:
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        frame_buttons = QFrame(self)
        frame_buttons_layout = QHBoxLayout(frame_buttons)
        # Set layout alignment to the left
        frame_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        pushButton_Back = ActionButton(
            parent=self, text=get_translation(key='back'))
        pushButton_Back.clicked.connect(callback_back)
        frame_buttons_layout.addWidget(pushButton_Back)
        self.layout.addWidget(frame_buttons)

        # Create a scrollable widget
        scrollable_widget = QScrollArea(self)
        scrollable_widget.setWidgetResizable(True)
        # Create a container widget to hold the layout
        container_widget = QWidget(self)
        container_layout = QVBoxLayout(container_widget)

        for model in models:
            pushButton_Model = ActionButton(
                parent=self, text=model.__tablename__)
            pushButton_Model.clicked.connect(
                partial(callback_select_table, model=model))
            container_layout.addWidget(pushButton_Model)
        spacer_widget = QWidget(parent=self)
        spacer_widget.setSizePolicy(QSizePolicy.Policy.Expanding,
                                    QSizePolicy.Policy.Expanding)
        container_layout.addWidget(spacer_widget)
        scrollable_widget.setWidget(container_widget)
        self.layout.addWidget(scrollable_widget)


class Widget_Database_Table(QWidget):
    def __init__(self,
                 parent: QWidget,
                 model,
                 my_role=None,
                 callback_back=None,
                 callback_create=None,
                 callback_read=None,
                 callback_select=None,
                 callback_update=None,
                 callback_delete=None) -> None:
        super().__init__(parent)
        self.callback_back = callback_back
        self.callback_create = callback_create
        self.callback_read = callback_read
        self.callback_select = callback_select
        self.callback_update = callback_update
        self.callback_delete = callback_delete
        self.layout = QVBoxLayout(self)
        self.model = model

        # """ Check if model is subclass of User but not the class User itself
        self.is_user_subclass = issubclass(model, User) and model is not User
        # """

        """ Check if model operand permission with my role """
        check_model = self.model
        if self.is_user_subclass:
            check_model = User
        is_create = isPermissionToMe(model=check_model,
                                     my_role=my_role,
                                     operand='create')
        is_read = isPermissionToMe(model=check_model,
                                   my_role=my_role,
                                   operand='read')
        is_update = isPermissionToMe(model=check_model,
                                     my_role=my_role,
                                     operand='update')
        is_delete = isPermissionToMe(model=check_model,
                                     my_role=my_role,
                                     operand='delete')

        frame_buttons = QFrame(self)
        frame_buttons_layout = QHBoxLayout(frame_buttons)
        # Set layout alignment to the left
        frame_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        pushButton_Back = ActionButton(
            parent=self, text=get_translation(key='back'))
        pushButton_Back.clicked.connect(partial(self.back_button_clicked))
        frame_buttons_layout.addWidget(pushButton_Back)
        if is_create:
            pushButton_Create = ActionButton(
                parent=self, text=get_translation(key='add'))
            pushButton_Create.clicked.connect(
                partial(self.create_button_clicked))
            frame_buttons_layout.addWidget(pushButton_Create)
        self.layout.addWidget(frame_buttons)

        # Create a QTableWidget to display data
        self.table_widget = QTableWidget(self)

        header_labels = []
        table_columns = []
        column_count = 0

        hide_columns = []

        if self.is_user_subclass:
            table_columns += list(User.__table__.columns)

        # Set up the table headers based on model attributes
        table_columns += list(model.__table__.columns)

        for table_column in table_columns:
            if isThisColumnHideToMe(column=table_column, my_role=my_role):
                hide_columns.append(getColumnTranslation(
                    column=table_column, language=LANGUAGE))

        # +1 for the extra action buttons column
        column_count += len(table_columns) + 1

        # Get the Database's table column descriptions for the headers
        header_labels += [getColumnTranslation(column=column, language=LANGUAGE)
                          for column in table_columns]

        # Add an extra column for functionality
        header_labels += [get_translation(key='action_button')]

        # Set the horizontal header labels for the QTableWidget
        self.table_widget.setColumnCount(column_count)
        self.table_widget.setHorizontalHeaderLabels(header_labels)

        # Retrieve all instances of the model from the database
        CRUD_Class = get_crud_class(model_class=self.model)
        status, instances = CRUD_Class.read_all()

        if status != CRUD_Status.FOUND:
            instances = []

        # Populate the table with data
        populate_table(table_widget=self.table_widget,
                       instances=instances,
                       model=self.model)

        # Add buttons to the last column for each row
        for row in range(self.table_widget.rowCount()):
            button_frame = QWidget(self)
            button_layout = QHBoxLayout(button_frame)
            if is_read:
                read_button = ActionButton(parent=self,
                                           icon_path=icon_show_path,
                                           stylesheet_normal="background-color: rgba(0, 0, 255, 80);",
                                           stylesheet_hover="background-color: rgba(0, 0, 255, 140);")

                read_button.clicked.connect(
                    partial(self.read_button_clicked,
                            id=get_id_for_row(table_widget=self.table_widget,
                                              row=row)))
                button_layout.addWidget(read_button)
            if is_update:
                update_button = ActionButton(parent=self,
                                             icon_path=icon_edit_path,
                                             stylesheet_normal="background-color: rgba(255, 255, 0, 80);",
                                             stylesheet_hover="background-color: rgba(255, 255, 0, 140);")
                update_button.clicked.connect(
                    partial(self.update_button_clicked,
                            id=get_id_for_row(table_widget=self.table_widget,
                                              row=row)))
                button_layout.addWidget(update_button)
            if is_delete:
                delete_button = ActionButton(icon_path=icon_delete_path,
                                             stylesheet_normal="background-color: rgba(255, 0, 0, 80);",
                                             stylesheet_hover="background-color: rgba(255, 0, 0, 140);")
                delete_button.clicked.connect(
                    partial(self.delete_button_clicked,
                            id=get_id_for_row(table_widget=self.table_widget,
                                              row=row)))
                button_layout.addWidget(delete_button)
            if self.callback_select:
                select_button = ActionButton(parent=self,
                                             icon_path=icon_select_path,
                                             stylesheet_normal="background-color: rgba(0, 255, 0, 80);",
                                             stylesheet_hover="background-color: rgba(0, 255, 0, 140);")
                select_button.clicked.connect(
                    partial(self.select_button_clicked,
                            id=get_id_for_row(table_widget=self.table_widget,
                                              row=row)))
                button_layout.addWidget(select_button)
            button_layout.setContentsMargins(0, 0, 0, 0)
            button_layout.setSpacing(0)

            self.table_widget.setCellWidget(row,
                                            column_count - 1,  # Last column
                                            button_frame)
        self.table_widget.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents)
        for col in range(1, column_count - 1):
            # Col from 1 to column - 2
            self.table_widget.horizontalHeader().setSectionResizeMode(
                col, QHeaderView.ResizeMode.Stretch)
        self.table_widget.horizontalHeader().setSectionResizeMode(
            column_count - 1, QHeaderView.ResizeMode.ResizeToContents)

        self.table_widget.setSortingEnabled(True)
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()

        hide_columns.append('id')

        hide_columns_by_header_labels(table_widget=self.table_widget,
                                      header_labels=hide_columns)

        self.layout.addWidget(self.table_widget)

    def select_button_clicked(self, id):
        if not self.callback_select:
            return
        status, obj = get_crud_class(self.model).read(id)
        if status != CRUD_Status.FOUND:
            return
        self.callback_select(obj=obj, model=self.model)

    def read_button_clicked(self, id):
        if not self.callback_read:
            return
        status, obj = get_crud_class(self.model).read(id)
        if status != CRUD_Status.FOUND:
            return
        self.callback_read(obj=obj, model=self.model)

    def update_button_clicked(self, id):
        if not self.callback_update:
            return
        status, obj = get_crud_class(self.model).read(id)
        if status != CRUD_Status.FOUND:
            return
        self.callback_update(obj=obj, model=self.model)

    def delete_button_clicked(self, id):
        if not self.callback_delete:
            return
        status, obj = get_crud_class(self.model).read(id)

        if status != CRUD_Status.FOUND:
            return
        self.callback_delete(obj=obj)

    def back_button_clicked(self):
        if not self.callback_back:
            return
        self.callback_back()

    def create_button_clicked(self):
        if not self.callback_create:
            return
        self.callback_create(model=self.model)


class Widget_Database_Table_Instances(QWidget):
    def __init__(self,
                 parent: QWidget,
                 instances,
                 model,
                 my_role=None,
                 callback_back=None,
                 callback_create=None,
                 callback_read=None,
                 callback_select=None,
                 callback_update=None,
                 callback_delete=None) -> None:
        super().__init__(parent)
        self.callback_back = callback_back
        self.callback_create = callback_create
        self.callback_read = callback_read
        self.callback_select = callback_select
        self.callback_update = callback_update
        self.callback_delete = callback_delete
        self.layout = QVBoxLayout(self)
        self.instances = instances
        self.model = model

        # """ Check if model is subclass of User but not the class User itself
        self.is_user_subclass = issubclass(model, User) and model is not User
        # """

        """ Check if model operand permission with my role """
        check_model = self.model
        if self.is_user_subclass:
            check_model = User
        is_create = isPermissionToMe(model=check_model,
                                     my_role=my_role,
                                     operand='create')
        is_read = isPermissionToMe(model=check_model,
                                   my_role=my_role,
                                   operand='read')
        is_update = isPermissionToMe(model=check_model,
                                     my_role=my_role,
                                     operand='update')
        is_delete = isPermissionToMe(model=check_model,
                                     my_role=my_role,
                                     operand='delete')

        frame_buttons = QFrame(self)
        frame_buttons_layout = QHBoxLayout(frame_buttons)
        # Set layout alignment to the left
        frame_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        pushButton_Back = ActionButton(
            parent=self, text=get_translation(key='back'))
        pushButton_Back.clicked.connect(partial(self.back_button_clicked))
        frame_buttons_layout.addWidget(pushButton_Back)
        if is_create:
            pushButton_Create = ActionButton(
                parent=self, text=get_translation(key='add'))
            pushButton_Create.clicked.connect(
                partial(self.create_button_clicked))
            frame_buttons_layout.addWidget(pushButton_Create)
        self.layout.addWidget(frame_buttons)

        # Create a QTableWidget to display data
        self.table_widget = QTableWidget(self)

        header_labels = []
        table_columns = []
        column_count = 0

        hide_columns = []

        if self.is_user_subclass:
            table_columns += list(User.__table__.columns)

        # Set up the table headers based on model attributes
        table_columns += list(model.__table__.columns)

        for table_column in table_columns:
            if isThisColumnHideToMe(column=table_column, my_role=my_role):
                hide_columns.append(getColumnTranslation(
                    column=table_column, language=LANGUAGE))

        # +1 for the extra action buttons column
        column_count += len(table_columns) + 1

        # Get the Database's table column descriptions for the headers
        header_labels += [getColumnTranslation(column=column, language=LANGUAGE)
                          for column in table_columns]

        # Add an extra column for functionality
        header_labels += [get_translation(key='action_button')]

        # Set the horizontal header labels for the QTableWidget
        self.table_widget.setColumnCount(column_count)
        self.table_widget.setHorizontalHeaderLabels(header_labels)

        # Populate the table with data
        populate_table(table_widget=self.table_widget,
                       instances=self.instances,
                       model=self.model)

        # Add buttons to the last column for each row
        for row in range(self.table_widget.rowCount()):
            button_frame = QWidget(self)
            button_layout = QHBoxLayout(button_frame)
            if is_read:
                read_button = ActionButton(parent=self,
                                           icon_path=icon_show_path,
                                           stylesheet_normal="background-color: rgba(0, 0, 255, 80);",
                                           stylesheet_hover="background-color: rgba(0, 0, 255, 140);")

                read_button.clicked.connect(
                    partial(self.read_button_clicked,
                            id=get_id_for_row(table_widget=self.table_widget,
                                              row=row)))
                button_layout.addWidget(read_button)
            if is_update:
                if callback_update:
                    update_button = ActionButton(parent=self,
                                                 icon_path=icon_edit_path,
                                                 stylesheet_normal="background-color: rgba(255, 255, 0, 80);",
                                                 stylesheet_hover="background-color: rgba(255, 255, 0, 140);")
                    update_button.clicked.connect(
                        partial(self.update_button_clicked,
                                id=get_id_for_row(table_widget=self.table_widget,
                                                  row=row)))
                    button_layout.addWidget(update_button)
            if is_delete:
                delete_button = ActionButton(icon_path=icon_delete_path,
                                             stylesheet_normal="background-color: rgba(255, 0, 0, 80);",
                                             stylesheet_hover="background-color: rgba(255, 0, 0, 140);")
                delete_button.clicked.connect(
                    partial(self.delete_button_clicked,
                            id=get_id_for_row(table_widget=self.table_widget,
                                              row=row)))
                button_layout.addWidget(delete_button)
            if self.callback_select:
                select_button = ActionButton(parent=self,
                                             icon_path=icon_select_path,
                                             stylesheet_normal="background-color: rgba(0, 255, 0, 80);",
                                             stylesheet_hover="background-color: rgba(0, 255, 0, 140);")
                select_button.clicked.connect(
                    partial(self.select_button_clicked,
                            id=get_id_for_row(table_widget=self.table_widget,
                                              row=row)))
                button_layout.addWidget(select_button)
            button_layout.setContentsMargins(0, 0, 0, 0)
            button_layout.setSpacing(0)

            self.table_widget.setCellWidget(row,
                                            column_count - 1,  # Last column
                                            button_frame)
        self.table_widget.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents)
        for col in range(1, column_count - 1):
            # Col from 1 to column - 2
            self.table_widget.horizontalHeader().setSectionResizeMode(
                col, QHeaderView.ResizeMode.Stretch)
        self.table_widget.horizontalHeader().setSectionResizeMode(
            column_count - 1, QHeaderView.ResizeMode.ResizeToContents)

        self.table_widget.setSortingEnabled(True)
        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()

        hide_columns.append('id')

        hide_columns_by_header_labels(table_widget=self.table_widget,
                                      header_labels=hide_columns)

        self.layout.addWidget(self.table_widget)

    def select_button_clicked(self, id):
        if not self.callback_select:
            return
        status, obj = get_crud_class(self.model).read(id)
        if status != CRUD_Status.FOUND:
            return
        self.callback_select(obj=obj, model=self.model)

    def read_button_clicked(self, id):
        if not self.callback_read:
            return
        status, obj = get_crud_class(self.model).read(id)
        if status != CRUD_Status.FOUND:
            return
        self.callback_read(obj=obj, model=self.model)

    def update_button_clicked(self, id):
        if not self.callback_update:
            return
        status, obj = get_crud_class(self.model).read(id)
        if status != CRUD_Status.FOUND:
            return
        self.callback_update(obj=obj, model=self.model)

    def delete_button_clicked(self, id):
        if not self.callback_delete:
            return
        status, obj = get_crud_class(self.model).read(id)

        if status != CRUD_Status.FOUND:
            return
        self.callback_delete(obj=obj)

    def back_button_clicked(self):
        if not self.callback_back:
            return
        self.callback_back()

    def create_button_clicked(self):
        if not self.callback_create:
            return
        self.callback_create(model=self.model)

class Widget_Interviewer_InterviewerAssignments_Update(QWidget):
    def __init__(self,
                 parent: QWidget,
                 obj: InterviewerAssignment,
                 my_role,
                 callback_back=None,
                 callback_cancel=None,
                 callback_update=None) -> None:
        super().__init__(parent)
        self.callback_back = callback_back
        self.callback_cancel = callback_cancel
        self.callback_update = callback_update
        layout = QVBoxLayout(self)
        # layout.setContentsMargins(0, 0, 0, 0)
        self.layout = layout
        self.obj = obj
        self.model = InterviewerAssignment
        self.line_edits = {}
        self.comboboxes = {}
        frame_buttons = QFrame(self)
        frame_buttons_layout = QHBoxLayout(frame_buttons)
        # Set layout alignment to the left
        frame_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        pushButton_Back = ActionButton(
            parent=self, text=get_translation(key='back'))
        pushButton_Back.clicked.connect(partial(self.back_button_clicked))
        frame_buttons_layout.addWidget(pushButton_Back)
        self.layout.addWidget(frame_buttons)
        # Create a scrollable widget
        scrollable_widget = QScrollArea(self)
        scrollable_widget.setWidgetResizable(True)
        # Create a container widget to hold the layout
        container_widget = QWidget(self)
        container_layout = QVBoxLayout(container_widget)

        hide_columns = ['interviewer_id', 'job_manager_id']
        # Get the mapped class and its properties using inspect
        mapper = inspect(self.model)
        for column in mapper.columns:
            # Skip the PK 'id' column or any other columns you want to exclude
            if column.primary_key:
                continue
            # Skip 'hide' column
            if isThisColumnHideToMe(column=column, my_role=my_role):
                continue
            if column.name in hide_columns:
                continue
            # Get translated description of the column
            description = getColumnTranslation(
                column=column, language=LANGUAGE)
            if column.nullable or not callback_update:
                label_name = QLabel(f"{description}:", parent=self)
            else:
                label_name = QLabel(f"{description} (*):", parent=self)
                label_name.setStyleSheet("color: rgb(153, 0, 0)")

            container_layout.addWidget(label_name)
            # Updateable column ?
            is_not_updateable = not isUpdateableToMe(
                column=column, my_role=my_role) or not callback_update

            # Check if the column is a File column
            file_type = getColumnFileType(column=column)
            if file_type == FileTypes.PDF_FILE.value:
                self.widget_cv_holder = Widget_FilePath(parent=self,
                                                        data=getattr(
                                                            self.obj, column.name, None),
                                                        file_type=FileTypes.PDF_FILE.value,
                                                        is_upload=self.callback_update,
                                                        is_download='dummy string')
                container_layout.addWidget(self.widget_cv_holder)
                continue

            if is_not_updateable:
                if column.foreign_keys:
                    # Get the class of the related model
                    related_model_class = list(column.foreign_keys)[
                        0].column.table
                    # Get the foreign key value
                    foreign_key_value = getattr(self.obj, column.name, None)

                    # Fetch the corresponding instance using the foreign key value
                    instance = session.query(related_model_class).filter_by(
                        id=foreign_key_value).first()
                    if str(related_model_class) in ['interviewers', 'job_managers', 'candidates', 'admins']:
                        status, user = CRUD_User.read(id=instance.id)
                        label_value_text = str(user.name)
                    else:
                        label_value_text = str(
                            instance.name) if instance else ''
                else:
                    attr = getattr(self.obj, column.name, None)
                    label_value_text = str(attr) if attr else ''
                label_value = QLabel(label_value_text)
                label_value.setStyleSheet(
                    "background-color:rgba(0, 0, 153, 30); padding: 5px 5px 5px 5ps;")
                container_layout.addWidget(label_value)
                # self.labels[column.name] = label_value
                continue

            # Check if the column is a Date column
            if column.type.python_type is datetime.date:
                date_edit = QDateEdit(self)
                date_value = getattr(self.obj, column.name, None)
                if date_value:
                    date_edit.setDate(
                        QDate(date_value.year, date_value.month, date_value.day))
                date_edit.setDisabled(is_not_updateable)
                self.line_edits[column.name] = date_edit
                container_layout.addWidget(date_edit)

            # Check if the column is a Datetime column
            elif column.type.python_type is datetime.datetime:
                datetime_picker = QDateTimeEdit(self)
                datetime_value = getattr(self.obj, column.name, None)
                if datetime_value:
                    datetime_picker.setDateTime(QDateTime(datetime_value))
                datetime_picker.setDisabled(is_not_updateable)
                self.line_edits[column.name] = datetime_picker
                container_layout.addWidget(datetime_picker)
            else:
                # Check if the column is a foreign key
                if column.foreign_keys:
                    combobox = QComboBox(self)
                    # Add a "None" option as the first item
                    combobox.addItem("None", None)
                    # Get the class of the related model
                    related_model = list(column.foreign_keys)[0].column.table
                    # Get the foreign key value
                    foreign_key_value = getattr(self.obj, column.name, None)

                    # Fetch the corresponding instance using the foreign key value
                    related_instances = session.query(related_model).all()
                    for instance in related_instances:
                        if str(related_model) in ['interviewers', 'job_managers', 'candidates', 'admins']:
                            status, user = CRUD_User.read(id=instance.id)
                            item_text = str(user.name)
                        else:
                            item_text = str(instance.name)
                        combobox.addItem(item_text, instance.id)

                    current_value = getattr(self.obj, column.name, None)
                    index = combobox.findData(current_value)
                    combobox.setCurrentIndex(index)

                    self.comboboxes[column.name] = combobox
                    container_layout.addWidget(combobox)
                else:
                    attr = getattr(self.obj, column.name)
                    if attr:
                        item_text = str(attr)
                    else:
                        item_text = ''

                    line_edit_input = QLineEdit(item_text, parent=self)
                    # Enable clear button for QLineEdit
                    line_edit_input.setClearButtonEnabled(True)
                    line_edit_input.setDisabled(is_not_updateable)
                    self.line_edits[column.name] = line_edit_input
                    container_layout.addWidget(line_edit_input)
        
        container_layout.addWidget(QLabel(parent=self, text=getModelDescription(ApplicationFormStatus, LANGUAGE) + ":"))
        
        combobox_application_status = QComboBox(self)
        combobox_application_status.addItem("None", None)
        status, application_statuses = CRUD_ApplicationFormStatus.read_all()
        for application_status in application_statuses:
            combobox_application_status.addItem(application_status.name, application_status.id)
        current_value = self.obj.application_form.application_form_status.id if self.obj.application_form.application_form_status else "None"
        index = combobox_application_status.findData(current_value)
        if index == -1:
            index = 0
        combobox_application_status.setCurrentIndex(index)
        self.combobox_application_status = combobox_application_status
        container_layout.addWidget(self.combobox_application_status)

        self.button_view_application_form = ActionButton(self, "View Application Form")
        self.button_view_application_form.clicked.connect(self.button_view_application_form_clicked)
        container_layout.addWidget(self.button_view_application_form)

        spacer_widget = QWidget(parent=self)
        spacer_widget.setSizePolicy(QSizePolicy.Policy.Expanding,
                                    QSizePolicy.Policy.Expanding)
        container_layout.addWidget(spacer_widget)
        # Set the container widget as the content of the scrollable widget
        scrollable_widget.setWidget(container_widget)
        self.layout.addWidget(scrollable_widget)
        # Frame for action buttons
        frame_buttons = QFrame(self)
        frame_buttons_layout = QHBoxLayout(frame_buttons)

        # Update mode
        if callback_update:
            update_button = ActionButton(self, get_translation('update'))
            update_button.clicked.connect(partial(self.update_button_clicked))
            frame_buttons_layout.addWidget(update_button)
            cancel_button = ActionButton(self, get_translation('cancel'))
            cancel_button.clicked.connect(partial(self.cancel_button_clicked))
            frame_buttons_layout.addWidget(cancel_button)
        self.layout.addWidget(frame_buttons)
        self.setLayout(self.layout)

    def button_view_application_form_clicked(self):
        popup_application_form = Popup_ApplicationForm(obj=self.obj.application_form)
        popup_application_form.exec()

    def back_button_clicked(self):
        if not self.callback_back:
            return
        self.callback_back(model=self.model, obj=self.obj)

    def cancel_button_clicked(self):
        if self.callback_cancel:
            self.callback_cancel(model=self.model)

    def update_button_clicked(self):
        if not self.callback_update:
            return

        # Update the model object with user input
        for name, line_edit in self.line_edits.items():
            setattr(self.obj, name, line_edit.text()
                    if line_edit.text() != '' else None)

        # Set foreign key values
        for column_name, combobox in self.comboboxes.items():
            selected_instance_id = combobox.currentData()
            setattr(self.obj, column_name, selected_instance_id)

        model_values = {
            name: self.get_widget_value(widget) for name, widget in self.line_edits.items()
        }

        application_form_status_id = self.combobox_application_status.currentData()
        self.callback_update(obj=self.obj, application_form_status_id=application_form_status_id, **model_values)

    def get_widget_value(self, widget):
        if isinstance(widget, QDateTimeEdit):
            return widget.dateTime().toPyDateTime() if widget.dateTime().isValid() else None
        else:
            return widget.text() if widget.text() != '' else None

class Popup_ApplicationForm(QDialog):
    def __init__(self, obj:ApplicationForm):
        super().__init__()
        self.setWindowTitle(obj.name)
        self.setMinimumWidth(420)
        self.layout = QHBoxLayout()

        widget_read_candidate = Widget_Read(parent=self,
                                              obj=obj.candidate,
                                              model=Candidate,
                                              my_role=RoleStates.CANDIDATE.name)
        self.layout.addWidget(widget_read_candidate)

        widget_read_application_form = Widget_Read(parent=self,
                                              obj=obj,
                                              model=ApplicationForm,
                                              my_role=RoleStates.CANDIDATE.name)
        self.layout.addWidget(widget_read_application_form)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)

class Widget_Read(QWidget):
    def __init__(self,
                 parent: QWidget,
                 obj: Base,
                 model,
                 my_role=None) -> None:
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.obj = obj
        self.model = model

        label = QLabel(parent=self, text=getModelDescription(model=model, language=LANGUAGE))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("background-color:rgba(0, 0, 180, 120)")
        self.layout.addWidget(label)

        scrollable_widget = QScrollArea(self)
        scrollable_widget.setWidgetResizable(True)
        # Create a container widget to hold the layout
        container_widget = QWidget(self)
        container_layout = QVBoxLayout(container_widget)

        hide_columns = ['password_hash', 'username']
        # Get the mapped class and its properties using inspect
        mapper = inspect(self.model)
        for column in mapper.columns:
            # Skip the PK 'id' column or any other columns you want to exclude
            if column.primary_key:
                continue
            # Skip 'hide' column
            if isThisColumnHideToMe(column=column, my_role=my_role):
                continue
            if column.name in hide_columns:
                continue
            # Get translated description of the column
            description = getColumnTranslation(
                column=column, language=LANGUAGE)
            label_name = QLabel(f"{description}:", parent=self)

            container_layout.addWidget(label_name)

            # Check if the column is a File column
            file_type = getColumnFileType(column=column)
            if file_type == FileTypes.PDF_FILE.value:
                self.widget_cv_holder = Widget_FilePath(parent=self,
                                                        data=getattr(
                                                            self.obj, column.name, None),
                                                        file_type=FileTypes.PDF_FILE.value,
                                                        is_download='dummy string')
                container_layout.addWidget(self.widget_cv_holder)
                continue

            if column.foreign_keys:
                # Get the class of the related model
                related_model_class = list(column.foreign_keys)[
                    0].column.table
                # Get the foreign key value
                foreign_key_value = getattr(self.obj, column.name, None)

                # Fetch the corresponding instance using the foreign key value
                instance = session.query(related_model_class).filter_by(
                    id=foreign_key_value).first()
                if str(related_model_class) in ['interviewers', 'job_managers', 'candidates', 'admins']:
                    status, user = CRUD_User.read(id=instance.id)
                    label_value_text = str(user.name)
                else:
                    label_value_text = str(
                        instance.name) if instance else ''
            else:
                attr = getattr(self.obj, column.name, None)
                label_value_text = str(attr) if attr else ''
            label_value = QLabel(label_value_text)
            label_value.setStyleSheet(
                "background-color:rgba(0, 0, 153, 30); padding: 5px 5px 5px 5ps;")
            container_layout.addWidget(label_value)
            # self.labels[column.name] = label_value

        spacer_widget = QWidget(parent=self)
        spacer_widget.setSizePolicy(QSizePolicy.Policy.Expanding,
                                    QSizePolicy.Policy.Expanding)
        container_layout.addWidget(spacer_widget)
        # Set the container widget as the content of the scrollable widget
        scrollable_widget.setWidget(container_widget)
        self.layout.addWidget(scrollable_widget)

class Widget_ReadUpdateDelete(QWidget):
    """
    Read: callback_update = None\n
    or\n
    Update: callback_update = callback_update\n
    Disable Delete: callback_delete = None\n
    or\n
    Enable Delete: callback_delete = callback_delete\n
    """

    def __init__(self,
                 parent: QWidget,
                 obj: Base,
                 model,
                 my_role=None,
                 callback_back=None,
                 callback_cancel=None,
                 callback_update=None,
                 callback_delete=None) -> None:
        super().__init__(parent)
        self.callback_back = callback_back
        self.callback_cancel = callback_cancel
        self.callback_update = callback_update
        self.callback_delete = callback_delete
        layout = QVBoxLayout(self)
        # layout.setContentsMargins(0, 0, 0, 0)
        self.layout = layout
        self.obj = obj
        self.model = model
        self.line_edits = {}
        self.comboboxes = {}
        frame_buttons = QFrame(self)
        frame_buttons_layout = QHBoxLayout(frame_buttons)
        # Set layout alignment to the left
        frame_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        if self.callback_back:
            pushButton_Back = ActionButton(
                parent=self, text=get_translation(key='back'))
            pushButton_Back.clicked.connect(partial(self.back_button_clicked))
            frame_buttons_layout.addWidget(pushButton_Back)
        self.layout.addWidget(frame_buttons)
        # Create a scrollable widget
        scrollable_widget = QScrollArea(self)
        scrollable_widget.setWidgetResizable(True)
        # Create a container widget to hold the layout
        container_widget = QWidget(self)
        container_layout = QVBoxLayout(container_widget)

        hide_columns = ['password_hash', 'username']
        # Get the mapped class and its properties using inspect
        mapper = inspect(self.model)
        for column in mapper.columns:
            # Skip the PK 'id' column or any other columns you want to exclude
            if column.primary_key:
                continue
            # Skip 'hide' column
            if isThisColumnHideToMe(column=column, my_role=my_role):
                continue
            if column.name in hide_columns:
                continue
            # Get translated description of the column
            description = getColumnTranslation(
                column=column, language=LANGUAGE)
            if column.nullable or not callback_update:
                label_name = QLabel(f"{description}:", parent=self)
            else:
                label_name = QLabel(f"{description} (*):", parent=self)
                label_name.setStyleSheet("color: rgb(153, 0, 0)")

            container_layout.addWidget(label_name)
            # Updateable column ?
            is_not_updateable = not isUpdateableToMe(
                column=column, my_role=my_role) or not callback_update

            # Check if the column is a File column
            file_type = getColumnFileType(column=column)
            if file_type == FileTypes.PDF_FILE.value:
                self.widget_cv_holder = Widget_FilePath(parent=self,
                                                        data=getattr(
                                                            self.obj, column.name, None),
                                                        file_type=FileTypes.PDF_FILE.value,
                                                        is_upload=self.callback_update,
                                                        is_download='dummy string')
                container_layout.addWidget(self.widget_cv_holder)
                continue

            if is_not_updateable:
                if column.foreign_keys:
                    # Get the class of the related model
                    related_model_class = list(column.foreign_keys)[
                        0].column.table
                    # Get the foreign key value
                    foreign_key_value = getattr(self.obj, column.name, None)

                    # Fetch the corresponding instance using the foreign key value
                    instance = session.query(related_model_class).filter_by(
                        id=foreign_key_value).first()
                    if str(related_model_class) in ['interviewers', 'job_managers', 'candidates', 'admins']:
                        status, user = CRUD_User.read(id=instance.id)
                        label_value_text = str(user.name)
                    else:
                        label_value_text = str(
                            instance.name) if instance else ''
                else:
                    attr = getattr(self.obj, column.name, None)
                    label_value_text = str(attr) if attr else ''
                label_value = QLabel(label_value_text)
                label_value.setStyleSheet(
                    "background-color:rgba(0, 0, 153, 30); padding: 5px 5px 5px 5ps;")
                container_layout.addWidget(label_value)
                # self.labels[column.name] = label_value
                continue

            # Check if the column is a Date column
            if column.type.python_type is datetime.date:
                date_edit = QDateEdit(self)
                date_value = getattr(self.obj, column.name, None)
                if date_value:
                    date_edit.setDate(
                        QDate(date_value.year, date_value.month, date_value.day))
                date_edit.setDisabled(is_not_updateable)
                self.line_edits[column.name] = date_edit
                container_layout.addWidget(date_edit)

            # Check if the column is a Datetime column
            elif column.type.python_type is datetime.datetime:
                datetime_picker = QDateTimeEdit(self)
                datetime_value = getattr(self.obj, column.name, None)
                if datetime_value:
                    datetime_picker.setDateTime(QDateTime(datetime_value))
                datetime_picker.setDisabled(is_not_updateable)
                self.line_edits[column.name] = datetime_picker
                container_layout.addWidget(datetime_picker)
            else:
                # Check if the column is a foreign key
                if column.foreign_keys:
                    combobox = QComboBox(self)
                    # Add a "None" option as the first item
                    combobox.addItem("None", None)
                    # Get the class of the related model
                    related_model = list(column.foreign_keys)[0].column.table
                    # Get the foreign key value
                    foreign_key_value = getattr(self.obj, column.name, None)

                    # Fetch the corresponding instance using the foreign key value
                    related_instances = session.query(related_model).all()
                    for instance in related_instances:
                        if str(related_model) in ['interviewers', 'job_managers', 'candidates', 'admins']:
                            status, user = CRUD_User.read(id=instance.id)
                            item_text = str(user.name)
                        else:
                            item_text = str(instance.name)
                        combobox.addItem(item_text, instance.id)

                    current_value = getattr(self.obj, column.name, None)
                    index = combobox.findData(current_value)
                    combobox.setCurrentIndex(index)

                    self.comboboxes[column.name] = combobox
                    container_layout.addWidget(combobox)
                else:
                    attr = getattr(self.obj, column.name)
                    if attr:
                        item_text = str(attr)
                    else:
                        item_text = ''

                    line_edit_input = QLineEdit(item_text, parent=self)
                    # Enable clear button for QLineEdit
                    line_edit_input.setClearButtonEnabled(True)
                    line_edit_input.setDisabled(is_not_updateable)
                    self.line_edits[column.name] = line_edit_input
                    container_layout.addWidget(line_edit_input)

        spacer_widget = QWidget(parent=self)
        spacer_widget.setSizePolicy(QSizePolicy.Policy.Expanding,
                                    QSizePolicy.Policy.Expanding)
        container_layout.addWidget(spacer_widget)
        # Set the container widget as the content of the scrollable widget
        scrollable_widget.setWidget(container_widget)
        self.layout.addWidget(scrollable_widget)
        # Frame for action buttons
        frame_buttons = QFrame(self)
        frame_buttons_layout = QHBoxLayout(frame_buttons)

        # Update mode
        if callback_update:
            update_button = ActionButton(self, get_translation('update'))
            update_button.clicked.connect(partial(self.update_button_clicked))
            frame_buttons_layout.addWidget(update_button)
        if callback_delete:
            delete_button = ActionButton(self, get_translation('delete'))
            delete_button.clicked.connect(partial(self.delete_button_clicked))
            frame_buttons_layout.addWidget(delete_button)
        if callback_update or callback_delete:
            cancel_button = ActionButton(self, get_translation('cancel'))
            cancel_button.clicked.connect(partial(self.cancel_button_clicked))
            frame_buttons_layout.addWidget(cancel_button)
        self.layout.addWidget(frame_buttons)
        self.setLayout(self.layout)

    def back_button_clicked(self):
        if not self.callback_back:
            return
        self.callback_back(model=self.model, obj=self.obj)

    def cancel_button_clicked(self):
        if self.callback_cancel:
            self.callback_cancel(model=self.model)

    def on_upload_file(self, column_name):
        pass

    def on_save_pdf_file(self, column_name):

        pass

    def update_button_clicked(self):
        if not self.callback_update:
            return

        # Update the model object with user input
        for name, line_edit in self.line_edits.items():
            setattr(self.obj, name, line_edit.text()
                    if line_edit.text() != '' else None)

        # Set foreign key values
        for column_name, combobox in self.comboboxes.items():
            selected_instance_id = combobox.currentData()
            setattr(self.obj, column_name, selected_instance_id)

        model_values = {
            name: self.get_widget_value(widget) for name, widget in self.line_edits.items()
        }
        self.callback_update(obj=self.obj, **model_values)

    def get_widget_value(self, widget):
        if isinstance(widget, QDateTimeEdit):
            return widget.dateTime().toPyDateTime() if widget.dateTime().isValid() else None
        else:
            return widget.text() if widget.text() != '' else None

    def delete_button_clicked(self):
        if not self.callback_delete:
            return
        self.callback_delete(obj=self.obj)


class Widget_SelfUpdate(QWidget):
    """
    Read: callback_update = None\n
    or\n
    Update: callback_update = callback_update\n
    Disable Delete: callback_delete = None\n
    or\n
    Enable Delete: callback_delete = callback_delete\n
    """

    def __init__(self,
                 parent: QWidget,
                 obj: Base,
                 # model = None,
                 callback_back=None,
                 callback_cancel=None,
                 callback_update=None) -> None:
        super().__init__(parent)
        self.callback_back = callback_back
        self.callback_cancel = callback_cancel
        self.callback_update = callback_update
        layout = QVBoxLayout(self)
        # layout.setContentsMargins(0, 0, 0, 0)
        self.layout = layout
        self.obj = obj
        self.model = type(obj)
        self.line_edits = {}
        self.comboboxes = {}
        frame_buttons = QFrame(self)
        frame_buttons_layout = QHBoxLayout(frame_buttons)
        # Set layout alignment to the left
        frame_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        pushButton_Back = ActionButton(
            parent=self, text=get_translation(key='back'))
        pushButton_Back.clicked.connect(partial(self.back_button_clicked))
        frame_buttons_layout.addWidget(pushButton_Back)
        self.layout.addWidget(frame_buttons)
        # Create a scrollable widget
        scrollable_widget = QScrollArea(self)
        scrollable_widget.setWidgetResizable(True)
        # Create a container widget to hold the layout
        container_widget = QWidget(self)
        container_layout = QVBoxLayout(container_widget)
        # Get the mapped class and its properties using inspect
        mapper = inspect(self.model)
        hide_clomuns = ['password_hash']
        disable_columns = ['username', 'role']
        for column in mapper.columns:
            # Skip the PK 'id' column or any other columns you want to exclude
            if column.primary_key:
                continue
            # Skip hide_clomuns
            if column.name in hide_clomuns:
                continue

            # Get translated description of the column
            description = column.info.get(
                'description', {}).get(LANGUAGE, column.name)
            if column.nullable:
                label_name = QLabel(description, parent=self)
            else:
                label_name = QLabel(f"{description} *", parent=self)
                label_name.setStyleSheet("color: rgb(153, 0, 0)")

            container_layout.addWidget(label_name)

            # Disable columns in disable_columns
            is_disable = column.name in disable_columns
            if is_disable:
                if column.foreign_keys:
                    # Get the class of the related model
                    related_model_class = list(column.foreign_keys)[
                        0].column.table
                    # Get the foreign key value
                    foreign_key_value = getattr(self.obj, column.name, None)

                    # Fetch the corresponding instance using the foreign key value
                    related_instance = session.query(
                        related_model_class).filter_by(id=foreign_key_value).first()
                    label_value_text = str(related_instance.name)
                else:
                    attr = getattr(self.obj, column.name, None)
                    label_value_text = str(attr)
                label_value = QLabel(label_value_text)
                label_value.setStyleSheet(
                    "background-color:rgba(0, 0, 153, 30); padding: 5px 5px 5px 5ps;")
                container_layout.addWidget(label_value)
                # self.labels[column.name] = label_value
                continue

            # Check if the column is a Date column
            if column.type.python_type is datetime.date:
                date_edit = QDateEdit(self)
                date_value = getattr(self.obj, column.name, None)
                if date_value:
                    date_edit.setDate(
                        QDate(date_value.year, date_value.month, date_value.day))
                self.line_edits[column.name] = date_edit
                container_layout.addWidget(date_edit)

            # Check if the column is a Datetime column
            elif column.type.python_type is datetime.datetime:
                datetime_picker = QDateTimeEdit(self)
                datetime_value = getattr(self.obj, column.name, None)
                if datetime_value:
                    datetime_picker.setDateTime(QDateTime(datetime_value))
                self.line_edits[column.name] = datetime_picker
                container_layout.addWidget(datetime_picker)
            else:
                # Check if the column is a foreign key
                if column.foreign_keys:

                    combobox = QComboBox(self)
                    # Add a "None" option as the first item
                    combobox.addItem("None", None)
                    # Get the class of the related model
                    related_model_class = list(column.foreign_keys)[
                        0].column.table
                    # Get the foreign key value
                    foreign_key_value = getattr(self.obj, column.name, None)

                    # Fetch the corresponding instance using the foreign key value
                    related_instances = session.query(
                        related_model_class).all()
                    for related_instance in related_instances:
                        combobox.addItem(related_instance.name,
                                         related_instance.id)

                    current_value = getattr(self.obj, column.name, None)
                    index = combobox.findData(current_value)
                    combobox.setCurrentIndex(index)
                    self.comboboxes[column.name] = combobox
                    container_layout.addWidget(combobox)
                else:
                    attr = getattr(self.obj, column.name)
                    if attr:
                        item_text = str(attr)
                    else:
                        item_text = ''

                    line_edit_input = QLineEdit(item_text, parent=self)
                    # Enable clear button for QLineEdit
                    line_edit_input.setClearButtonEnabled(True)
                    self.line_edits[column.name] = line_edit_input
                    container_layout.addWidget(line_edit_input)

        spacer_widget = QWidget(parent=self)
        spacer_widget.setSizePolicy(QSizePolicy.Policy.Expanding,
                                    QSizePolicy.Policy.Expanding)
        container_layout.addWidget(spacer_widget)
        # Set the container widget as the content of the scrollable widget
        scrollable_widget.setWidget(container_widget)
        self.layout.addWidget(scrollable_widget)
        # Frame for action buttons
        frame_buttons = QFrame(self)
        frame_buttons_layout = QHBoxLayout(frame_buttons)

        # Update mode
        if callback_update:
            update_button = ActionButton(self, get_translation('update'))
            update_button.clicked.connect(partial(self.update_button_clicked))
            frame_buttons_layout.addWidget(update_button)
            cancel_button = ActionButton(self, get_translation('cancel'))
            cancel_button.clicked.connect(partial(self.cancel_button_clicked))
            frame_buttons_layout.addWidget(cancel_button)

        self.layout.addWidget(frame_buttons)
        self.setLayout(self.layout)

    def back_button_clicked(self):
        if not self.callback_back:
            return
        self.callback_back(model=self.model)

    def cancel_button_clicked(self):
        if self.callback_cancel:
            self.callback_cancel(model=self.model)

    def update_button_clicked(self):
        if not self.callback_update:
            return

        # Update the model object with user input
        for name, line_edit in self.line_edits.items():
            setattr(self.obj, name, line_edit.text()
                    if line_edit.text() != '' else None)

        # Set foreign key values
        for column_name, combobox in self.comboboxes.items():
            selected_instance_id = combobox.currentData()
            setattr(self.obj, column_name, selected_instance_id)

        model_values = {
            name: self.get_widget_value(widget) for name, widget in self.line_edits.items()
        }
        self.callback_update(obj=self.obj, **model_values)

    def get_widget_value(self, widget):
        if isinstance(widget, QDateTimeEdit):
            return widget.dateTime().toPyDateTime() if widget.dateTime().isValid() else None
        else:
            return widget.text() if widget.text() != '' else None


class Widget_Create_MyApplicationForm(QWidget):
    def __init__(self, parent: QWidget, candidate_id, obj, callback_back=None, callback_cancel=None, callback_create=None) -> None:
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.candidate_id = candidate_id
        self.obj = obj  # job
        self.model = ApplicationForm

        frame_buttons = QFrame(self)
        frame_buttons_layout = QHBoxLayout(frame_buttons)
        # Set layout alignment to the left
        frame_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        pushButton_Back = ActionButton(
            parent=self, text=get_translation('back'))
        pushButton_Back.clicked.connect(partial(self.back_button_clicked,
                                                callback_back=callback_back))
        frame_buttons_layout.addWidget(pushButton_Back)
        self.layout.addWidget(frame_buttons)

        # Create a scrollable widget
        scrollable_widget = QScrollArea(self)
        scrollable_widget.setWidgetResizable(True)

        # Create a container widget to hold the layout
        container_widget = QWidget(self)
        container_layout = QVBoxLayout(container_widget)

        is_nullable = ApplicationForm.name.nullable
        if is_nullable:
            label_name_text = getColumnTranslation(
                column=ApplicationForm.name, language=LANGUAGE) + ":"
        else:
            label_name_text = getColumnTranslation(
                column=ApplicationForm.name, language=LANGUAGE) + " (*):"
        self.label_name = QLabel(parent=self, text=label_name_text)
        if not is_nullable:
            self.label_name.setStyleSheet("color: rgb(153, 0, 0)")
        container_layout.addWidget(self.label_name)

        self.lineEdit_name = QLineEdit()
        container_layout.addWidget(self.lineEdit_name)

        is_nullable = ApplicationForm.cv.nullable
        if is_nullable:
            label_cv_text = getColumnTranslation(
                column=ApplicationForm.cv, language=LANGUAGE) + ":"
        else:
            label_cv_text = getColumnTranslation(
                column=ApplicationForm.cv, language=LANGUAGE) + " (*):"
        self.label_cv = QLabel(parent=self, text=label_cv_text)
        if not is_nullable:
            self.label_cv.setStyleSheet("color: rgb(153, 0, 0)")
        container_layout.addWidget(self.label_cv)

        self.widget_cv_holder = Widget_FilePath(parent=self,
                                                file_type=FileTypes.PDF_FILE.value,
                                                is_upload='dummy string',
                                                is_download='dummy string')
        container_layout.addWidget(self.widget_cv_holder)
        is_nullable = ApplicationForm.job_id.nullable
        if is_nullable:
            label_job_text = getColumnTranslation(
                column=ApplicationForm.job_id, language=LANGUAGE) + ":"
        else:
            label_job_text = getColumnTranslation(
                column=ApplicationForm.job_id, language=LANGUAGE) + " (*):"
        self.label_job = QLabel(text=label_job_text, parent=self)
        if not is_nullable:
            self.label_cv.setStyleSheet("color: rgb(153, 0, 0)")
        container_layout.addWidget(self.label_job)

        label_job_value = QLabel(obj.name)
        label_job_value.setStyleSheet(
            "background-color:rgba(0, 0, 153, 30); padding: 5px 5px 5px 5ps;")
        container_layout.addWidget(label_job_value)

        # Spacer
        spacer_widget = QWidget(parent=self)
        spacer_widget.setSizePolicy(QSizePolicy.Policy.Expanding,
                                    QSizePolicy.Policy.Expanding)
        container_layout.addWidget(spacer_widget)

        scrollable_widget.setWidget(container_widget)
        self.layout.addWidget(scrollable_widget)

        cancel_button = ActionButton(self, get_translation(key='cancel'))
        cancel_button.clicked.connect(partial(self.cancel_button_clicked,
                                              callback_cancel=callback_cancel))

        create_button = ActionButton(self, get_translation(key='create'))
        create_button.clicked.connect(partial(self.create_button_clicked,
                                              callback_create=callback_create))

        frame_buttons = QFrame(self)
        frame_buttons_layout = QHBoxLayout(frame_buttons)
        frame_buttons_layout.addWidget(cancel_button)
        frame_buttons_layout.addWidget(create_button)
        self.layout.addWidget(frame_buttons)
        self.setLayout(self.layout)

        # self.setLayout(self.layout)
    def on_selected_cv_file(self, file_path):
        self.label_cv_file_path.setText(file_path)
        pass

    def back_button_clicked(self, callback_back):
        callback_back(model=self.model)

    def cancel_button_clicked(self, callback_cancel):
        callback_cancel(model=self.model)

    def create_button_clicked(self, callback_create):
        cv_bytes_data = self.widget_cv_holder.get_uploaded_data()
        callback_create(model=ApplicationForm,
                        name=self.lineEdit_name.text(),
                        cv=cv_bytes_data,
                        candidate_id=self.candidate_id,
                        job_id=self.obj.id)

    def get_widget_value(self, widget):
        if isinstance(widget, QDateTimeEdit):
            return widget.dateTime().toPyDateTime() if widget.dateTime().isValid() else None
        else:
            return widget.text() if widget.text() != '' else None


class Widget_Create_InterviewerAssignment(QWidget):
    def __init__(self, parent: QWidget, job_manager, application_form, callback_back=None, callback_cancel=None, callback_create=None) -> None:
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.job_manager = job_manager
        self.application_form = application_form
        self.model = InterviewerAssignment

        frame_buttons = QFrame(self)
        frame_buttons_layout = QHBoxLayout(frame_buttons)
        # Set layout alignment to the left
        frame_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        pushButton_Back = ActionButton(
            parent=self, text=get_translation('back'))
        pushButton_Back.clicked.connect(partial(self.back_button_clicked,
                                                callback_back=callback_back))
        frame_buttons_layout.addWidget(pushButton_Back)
        self.layout.addWidget(frame_buttons)

        # Create a scrollable widget
        scrollable_widget = QScrollArea(self)
        scrollable_widget.setWidgetResizable(True)

        # Create a container widget to hold the layout
        container_widget = QWidget(self)
        container_layout = QVBoxLayout(container_widget)

        container_layout.addWidget(QLabel(parent=self, text="Creating Interview Assignment for:\nCandidate: " +
                                   application_form.candidate.name + "\nApplication Form: " + application_form.name))

        is_nullable = InterviewerAssignment.interview_location.nullable
        if is_nullable:
            label_interview_location_text = getColumnTranslation(
                column=InterviewerAssignment.interview_location, language=LANGUAGE) + ":"
        else:
            label_interview_location_text = getColumnTranslation(
                column=InterviewerAssignment.interview_location, language=LANGUAGE) + " (*):"
        self.label_interview_location = QLabel(
            parent=self, text=label_interview_location_text)
        if not is_nullable:
            self.label_interview_location.setStyleSheet(
                "color: rgb(153, 0, 0)")
        container_layout.addWidget(self.label_interview_location)

        self.lineEdit_interview_location = QLineEdit()
        container_layout.addWidget(self.lineEdit_interview_location)

        is_nullable = InterviewerAssignment.interview_datetime.nullable
        if is_nullable:
            label_interview_datetime_text = getColumnTranslation(
                column=InterviewerAssignment.interview_datetime, language=LANGUAGE) + ":"
        else:
            label_interview_datetime_text = getColumnTranslation(
                column=InterviewerAssignment.interview_datetime, language=LANGUAGE) + " (*):"
        self.label_interview_datetime = QLabel(
            parent=self, text=label_interview_datetime_text)
        if not is_nullable:
            self.label_interview_datetime.setStyleSheet(
                "color: rgb(153, 0, 0)")
        container_layout.addWidget(self.label_interview_datetime)
        self.datetime_picker_interview_datetime = QDateTimeEdit(self)
        self.datetime_picker_interview_datetime.setDateTime(
            QDateTime.currentDateTime())
        container_layout.addWidget(self.datetime_picker_interview_datetime)

        is_nullable = InterviewerAssignment.interviewer_id.nullable
        if is_nullable:
            label_interviewer_id_text = getColumnTranslation(
                column=InterviewerAssignment.interviewer_id, language=LANGUAGE) + ":"
        else:
            label_interviewer_id_text = getColumnTranslation(
                column=InterviewerAssignment.interviewer_id, language=LANGUAGE) + " (*):"
        self.label_interviewer_id = QLabel(
            parent=self, text=label_interviewer_id_text)
        if not is_nullable:
            self.label_interviewer_id.setStyleSheet("color: rgb(153, 0, 0)")
        container_layout.addWidget(self.label_interviewer_id)
        self.combobox_interviewer = QComboBox(self)
        # Add a "None" option as the first item
        self.combobox_interviewer.addItem("None", None)
        # Add all instances
        status, interviewers = CRUD_Interviewer.read_all()

        for interviewer in interviewers:
            # status, user = CRUD_User.read(interviewer.id)
            self.combobox_interviewer.addItem(
                str(interviewer.name), interviewer.id)

        container_layout.addWidget(self.combobox_interviewer)

        # Spacer
        spacer_widget = QWidget(parent=self)
        spacer_widget.setSizePolicy(QSizePolicy.Policy.Expanding,
                                    QSizePolicy.Policy.Expanding)
        container_layout.addWidget(spacer_widget)

        scrollable_widget.setWidget(container_widget)
        self.layout.addWidget(scrollable_widget)

        cancel_button = ActionButton(self, get_translation(key='cancel'))
        cancel_button.clicked.connect(partial(self.cancel_button_clicked,
                                              callback_cancel=callback_cancel))

        create_button = ActionButton(self, get_translation(key='create'))
        create_button.clicked.connect(partial(self.create_button_clicked,
                                              callback_create=callback_create))

        frame_buttons = QFrame(self)
        frame_buttons_layout = QHBoxLayout(frame_buttons)
        frame_buttons_layout.addWidget(cancel_button)
        frame_buttons_layout.addWidget(create_button)
        self.layout.addWidget(frame_buttons)
        self.setLayout(self.layout)

    def back_button_clicked(self, callback_back):
        callback_back(model=self.model)

    def cancel_button_clicked(self, callback_cancel):
        callback_cancel(model=self.model)

    def create_button_clicked(self, callback_create):
        callback_create(model=InterviewerAssignment,
                        interview_location=self.lineEdit_interview_location.text(),
                        interview_datetime=self.datetime_picker_interview_datetime.dateTime().toPyDateTime(),
                        interviewer_id=self.combobox_interviewer.currentData(),
                        job_manager_id=self.job_manager.id,
                        application_form_id=self.application_form.id)


class Widget_Create(QWidget):
    def __init__(self, parent: QWidget, model: Base, callback_back=None, callback_cancel=None, callback_create=None) -> None:
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.model = model

        self.line_edits = {}
        self.comboboxes = {}

        frame_buttons = QFrame(self)
        frame_buttons_layout = QHBoxLayout(frame_buttons)
        # Set layout alignment to the left
        frame_buttons_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        pushButton_Back = ActionButton(
            parent=self, text=get_translation('back'))
        pushButton_Back.clicked.connect(partial(self.back_button_clicked,
                                                callback_back=callback_back))
        frame_buttons_layout.addWidget(pushButton_Back)
        self.layout.addWidget(frame_buttons)

        # Create a scrollable widget
        scrollable_widget = QScrollArea(self)
        scrollable_widget.setWidgetResizable(True)

        # Create a container widget to hold the layout
        container_widget = QWidget(self)
        container_layout = QVBoxLayout(container_widget)
        mapper = class_mapper(self.model)

        for prop in mapper.iterate_properties:
            if hasattr(prop, 'columns') and len(prop.columns) == 1:
                column = prop.columns[0]
                # Skip the PK 'id' column or any other columns you want to exclude
                if column.primary_key:
                    continue
                # Column description (* is nullable=False)
                description = column.info.get(
                    'description', {}).get(LANGUAGE, column.name)
                if column.nullable:
                    label_name = QLabel(description, parent=self)
                else:
                    label_name = QLabel(f"{description} *", parent=self)
                    label_name.setStyleSheet("color: rgb(153, 0, 0)")
                container_layout.addWidget(label_name)
                # Check if the column is a Date column
                if column.type.python_type is datetime.date:
                    date_edit = QDateEdit(self)
                    date_edit.setDate(QDate.currentDate())
                    self.line_edits[column.name] = date_edit
                    container_layout.addWidget(date_edit)
                # Check if the column is a Datetime column
                elif column.type.python_type is datetime.datetime:
                    datetime_picker = QDateTimeEdit(self)
                    datetime_picker.setDateTime(QDateTime.currentDateTime())
                    self.line_edits[column.name] = datetime_picker
                    container_layout.addWidget(datetime_picker)
                else:
                    # Check if the column is a foreign key
                    if column.foreign_keys:
                        combobox = QComboBox(self)
                        # Add a "None" option as the first item
                        combobox.addItem("None", None)
                        # Add all instances
                        related_model = list(column.foreign_keys)[
                            0].column.table

                        related_instances = session.query(related_model).all()

                        for instance in related_instances:

                            if str(related_model) in ['interviewers', 'job_managers', 'candidates', 'admins']:
                                status, user = CRUD_User.read(id=instance.id)

                                combobox.addItem(str(user.name), instance.id)
                            else:
                                combobox.addItem(
                                    str(instance.name), instance.id)

                        self.comboboxes[column.name] = combobox
                        container_layout.addWidget(combobox)
                    else:
                        line_edit_input = QLineEdit(parent=self)
                        # Enable clear button for QLineEdit
                        line_edit_input.setClearButtonEnabled(True)
                        self.line_edits[column.name] = line_edit_input
                        container_layout.addWidget(line_edit_input)
        # Spacer
        spacer_widget = QWidget(parent=self)
        spacer_widget.setSizePolicy(QSizePolicy.Policy.Expanding,
                                    QSizePolicy.Policy.Expanding)
        container_layout.addWidget(spacer_widget)

        scrollable_widget.setWidget(container_widget)
        self.layout.addWidget(scrollable_widget)

        cancel_button = ActionButton(self, get_translation(key='cancel'))
        cancel_button.clicked.connect(partial(self.cancel_button_clicked,
                                              callback_cancel=callback_cancel))

        create_button = ActionButton(self, get_translation(key='create'))
        create_button.clicked.connect(partial(self.create_button_clicked,
                                              callback_create=callback_create))

        frame_buttons = QFrame(self)
        frame_buttons_layout = QHBoxLayout(frame_buttons)
        frame_buttons_layout.addWidget(cancel_button)
        frame_buttons_layout.addWidget(create_button)
        self.layout.addWidget(frame_buttons)
        self.setLayout(self.layout)

        # self.setLayout(self.layout)

    def back_button_clicked(self, callback_back):
        callback_back(model=self.model)

    def cancel_button_clicked(self, callback_cancel):
        callback_cancel(model=self.model)

    def create_button_clicked(self, callback_create):
        # Create the model object with user input
        model_values = {
            name: self.get_widget_value(widget) for name, widget in self.line_edits.items()
        }

        # Set foreign key values
        for column_name, combobox in self.comboboxes.items():
            selected_instance_id = combobox.currentData()
            model_values[column_name] = selected_instance_id

        callback_create(model=self.model, **model_values)

    def get_widget_value(self, widget):
        if isinstance(widget, QDateTimeEdit):
            return widget.dateTime().toPyDateTime() if widget.dateTime().isValid() else None
        else:
            return widget.text() if widget.text() != '' else None
