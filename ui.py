""" #FIXME TEST ONLY """
from Backend.Services.time import to_ddmmYYYY_str, to_HHMMSS_ddmmYYYY_str
from Backend.Database.sessions import *
from Frontend.Helper.helper import *
from Frontend.Helper.action_buttons import *
from Frontend.Design.design_ui import Ui_MainWindow
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFrame,
    QWidget,
    QLabel,
    QLineEdit
)
from PyQt6 import QtWidgets
from functools import partial
import typing
TEST_DEV = True
if TEST_DEV:
    from Backend.Services.db_test import *
    initTestDatabase()
""" #FIXME TEST ONLY """

# PyQt6

# Modules
""" Frontend """
""" Frontend """
""" Backend """
# Sessions
# Services
""" Backend """

# Main App class


class MyApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        # Set up the user interface from Designer
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_icons()

        # Variables
        self.logged_in_user = QSignalVariable(None)
        self.logged_in_user.stateChanged.connect(self.renderViewOnUserLoggedIn)

        # Extended design and setup for ui
        self.toPage_Login()  # Started at login page

        # Connect signals and slots
        """ Header buttons """
        # self.ui.pushButton_Home.clicked.connect(self.toPage_MainMenu)
        self.ui.pushButton_SideMenu.clicked.connect(self.toogleSideMenu)
        self.ui.pushButton_Login_Login.clicked.connect(self.login)
        # self.ui.pushButton_Logout.clicked.connect(self.logout)
        # self.ui.pushButton_ChangePassword.clicked.connect(self.toPage_ChangePassword)
        self.ui.pushButton_ChangePassword_Cancel.clicked.connect(
            self.toPage_MainMenu)
        self.ui.pushButton_ChangePassword_Accept.clicked.connect(
            self.changePassword)

        """ Show password buttons """
        self.initPasswordShowButtons()

        # self.renderViewOnUserLoggedIn(is_logged_in=False)

        """ MainMenu Admin """
        self.ui.pushButton_Admin_UserManagement.clicked.connect(
            self.toPage_List_Users)
        self.ui.pushButton_Admin_DatabaseManagement.clicked.connect(
            self.toPage_Database)

        self.hideSideMenu(True)
        self.ui.pushButton_SideMenu.setHidden(True)
        """ MainMenu Admin """

    # Icons

    def init_icons(self):
        # self.ui.pushButton_Home.setIcon(QIcon(QPixmap(icon_home_path)))
        self.ui.pushButton_SideMenu.setIcon(QIcon(QPixmap(icon_menu_path)))
        background_image_path = 'Frontend/Resources/Images/default-avatar.png'
        self.ui.pushButton_UserAvatar.setStyleSheet(f"""
                                                    border-image: url({background_image_path});
                                                    background-repeat: no-repeat;
                                                    background-position: center;
                                                    """)

    def initPasswordShowButtons(self):
        """ Show password buttons """
        self.ui.pushButton_Login_PasswordShow.setIcon(
            QIcon(QPixmap(icon_hide_path)))
        self.ui.pushButton_Login_PasswordShow.clicked.connect(partial(togglePasswordVisibility,
                                                                      line_edit=self.ui.lineEdit_Login_Password,
                                                                      button=self.ui.pushButton_Login_PasswordShow))

        self.ui.pushButton_ChangePassword_OldPasswordShow.setIcon(
            QIcon(QPixmap(icon_hide_path)))
        self.ui.pushButton_ChangePassword_OldPasswordShow.clicked.connect(partial(togglePasswordVisibility,
                                                                                  line_edit=self.ui.lineEdit_ChangePassword_OldPassword,
                                                                                  button=self.ui.pushButton_ChangePassword_OldPasswordShow))

        self.ui.pushButton_ChangePassword_NewPasswordShow.setIcon(
            QIcon(QPixmap(icon_hide_path)))
        self.ui.pushButton_ChangePassword_NewPasswordShow.clicked.connect(partial(togglePasswordVisibility,
                                                                                  line_edit=self.ui.lineEdit_ChangePassword_NewPassword,
                                                                                  button=self.ui.pushButton_ChangePassword_NewPasswordShow))

        self.ui.pushButton_ChangePassword_NewPasswordRetypeShow.setIcon(
            QIcon(QPixmap(icon_hide_path)))
        self.ui.pushButton_ChangePassword_NewPasswordRetypeShow.clicked.connect(partial(togglePasswordVisibility,
                                                                                        line_edit=self.ui.lineEdit_ChangePassword_NewPasswordRetype,
                                                                                        button=self.ui.pushButton_ChangePassword_NewPasswordRetypeShow))

    """ Interacting """

    def hideSideMenu(self, is_hide: bool):
        self.ui.frame_SideMenu.setHidden(is_hide)

    def toogleSideMenu(self):
        is_hide = self.ui.frame_SideMenu.isHidden()
        self.hideSideMenu(is_hide=not is_hide)
    """ Interacting """

    """ Page Login """

    def toPage_Login(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Login)

    def login(self):
        username = self.ui.lineEdit_Login_Username.text()
        password = self.ui.lineEdit_Login_Password.text()
        """ #FIXME TEST ONLY """
        if TEST_DEV:
            username = username if username else 'admin1'
            password = password if password else 'admin'
        """ #FIXME TEST ONLY """
        status, result = CRUD_User.login(username=username, password=password)
        if status == Login_Status.LOGIN_SUCCESS:
            self.logged_in_user.state = result
            self.toPage_MainMenu()
        else:
            popup = PopupMessageBox(title="Đăng nhập thất bại", message=status)
            popup.exec()
            # self.ui.label_Login_Notification.setText(status)

    def logout(self):
        self.logged_in_user.state = None
        self.toPage_Login()

    def renderViewOnUserLoggedIn(self, is_logged_in: bool):
        if is_logged_in:
            self.ui.pushButton_SideMenu.setHidden(False)
            if not self.logged_in_user:
                print("ERROR: No user logged in")
                return
            role = self.logged_in_user.state.role
            if role == RoleStates.ADMIN.name:
                self.renderAdmin()
            elif role == RoleStates.CANDIDATE.name:
                self.renderCandidate()
            elif role == RoleStates.INTERVIEWER.name:
                self.renderInterviewer()
            elif role == RoleStates.JOB_MANAGER.name:
                self.renderJobManager()
        else:
            self.ui.pushButton_SideMenu.setHidden(True)

    def renderAdmin(self):
        print("Admin")
        action_buttons = [
            {"Home", icon_home_path, self}
        ]
        initActionButtons(parent_widget=self.ui.frame_ActionButtons,
                          action_buttons=[])
        pass

    def renderCandidate(self):
        print("Candidate")

    def renderInterviewer(self):
        print("Interviewer")

    def renderJobManager(self):
        print("JobManager")

    """ Page Login """

    """ Page ChangePassword """

    def toPage_ChangePassword(self):
        self.ui.label_ChangePassword_Notification.setText('')
        self.ui.lineEdit_ChangePassword_OldPassword.setText('')
        self.ui.lineEdit_ChangePassword_NewPassword.setText('')
        self.ui.lineEdit_ChangePassword_NewPasswordRetype.setText('')

        self.ui.stackedWidget.setCurrentWidget(self.ui.page_ChangePassword)

    def changePassword(self):
        old_password = self.ui.lineEdit_ChangePassword_OldPassword.text()
        old_password_hash = hash_string(old_password)
        logged_in_user: User = self.logged_in_user.state
        if logged_in_user.password_hash != old_password_hash:
            self.ui.label_ChangePassword_Notification.setText(
                "Mật khẩu cũ không chính xác!")
            return
        new_password = self.ui.lineEdit_ChangePassword_NewPassword.text()
        new_password_retype = self.ui.lineEdit_ChangePassword_NewPasswordRetype.text()
        if new_password != new_password_retype:
            self.ui.label_ChangePassword_Notification.setText(
                "Hai lần nhập mật khẩu mới không trùng khớp!")
            return
        if new_password == old_password:
            self.ui.label_ChangePassword_Notification.setText(
                "Mật khẩu mới trùng với mật khẩu cũ!")
            return
        state, result = CRUD_User.update(
            id=logged_in_user.id, password=new_password)
        if state != CRUD_Status.UPDATED:
            self.ui.label_ChangePassword_Notification.setText(
                f"Cập nhật mật khẩu mới thất bại!\n{state}")
            return
        self.ui.label_ChangePassword_Notification.setText(
            "Cập nhật mật khẩu mới thành công!")

    """ Page ChangePassword """

    """ Page MainMenu """

    def toPage_MainMenu(self):
        if not self.logged_in_user.state:
            return
        role = self.logged_in_user.state.role
        if role == RoleStates.ADMIN.name:
            self.toPage_MainMenu_Admin()
        elif role == RoleStates.CANDIDATE.name:
            self.toPage_MainMenu_Candidate()
        elif role == RoleStates.INTERVIEWER.name:
            self.toPage_MainMenu_Interviewer()
        elif role == RoleStates.JOB_MANAGER.name:
            self.toPage_MainMenu_JobManager()
    """ Page MainMenu """

    """ Page MainMenu Admin """

    def toPage_MainMenu_Admin(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_MainMenu_Admin)

    def toPage_List_Users(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_List)
        state, result = CRUD_User.read_all()
        renderView_List_Users(parent_frame=self.ui.frame_List,
                              users=result,
                              callback_detail=self.toPage_List_UserDetail,
                              callback_delete=self.userDelete)

    def userDelete(self, user: User):
        msg_box = QMessageBox(parent=self.ui.centralwidget)
        msg_box.setWindowTitle(f"XOÁ USER {user.username}")
        msg_box.setText(
            f"Xác nhận xoá {user.name}? Thao tác này không thể hoàn tác!")

        # Change Yes and No button text
        msg_box.button(QMessageBox.StandardButton.Yes).setText("Xoá")
        msg_box.button(QMessageBox.StandardButton.No).setText("Hủy")

        result = msg_box.exec()

        if result == QMessageBox.StandardButton.Yes:
            # Delete the user (implement your deletion logic here)
            CRUD_User.delete(user.id)
            self.toPage_List_Users()

    def toPage_List_UserDetail(self, user: User):
        print(user)

    def toPage_List_AddUser(self):

        pass

    """ Page MainMenu Admin """

    """ Page MainMenu Candidate """

    def toPage_MainMenu_Candidate(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_MainMenu_Candidate)
    """ Page MainMenu Candidate """

    """ Page MainMenu Interviewer """

    def toPage_MainMenu_Interviewer(self):
        self.ui.stackedWidget.setCurrentWidget(
            self.ui.page_MainMenu_Interviewer)
    """ Page MainMenu Interviewer """

    """ Page MainMenu JobManager """

    def toPage_MainMenu_JobManager(self):
        self.ui.stackedWidget.setCurrentWidget(
            self.ui.page_MainMenu_JobManager)
    """ Page MainMenu JobManager """

    """ Page Database """

    def toPage_Database(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        models = all_models
        widget_database = Widget_Database(parent=parent,
                                          models=models,
                                          callback_back=self.toPage_MainMenu,
                                          callback_select_table=self.toPage_Database_Table)
        parent_layout.addWidget(widget_database)

    def toPage_Database_Table(self, model):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        widget_table = Widget_Database_Table(parent=parent,
                                             model=model,
                                             callback_back=self.toPage_Database,
                                             callback_create=self.toPage_Database_Table_CreateData,
                                             callback_read=self.toPage_Database_Table_Read,
                                             callback_update=self.toPage_Database_Table_Update,
                                             callback_delete=self.toPage_Database_Table_Delete)
        parent_layout.addWidget(widget_table)

    def toPage_Database_Table_Delete(self, obj):
        self.deleteData(obj)

    def toPage_Database_Table_Update(self, obj):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        widget_update = Widget_ReadUpdateDelete(parent=parent,
                                                obj=obj,
                                                callback_back=self.toPage_Database_Table,
                                                callback_cancel=self.toPage_Database_Table,
                                                callback_update=self.updateData,
                                                callback_delete=self.deleteData)

        parent_layout.addWidget(widget_update)

    def deleteData(self, obj):
        model = type(obj)
        CRUD_Model = get_crud_class(model_class=model)
        status, result = CRUD_Model.delete(id=obj.id)
        print(status, result)
        if status != CRUD_Status.DELETED:
            return
        self.toPage_Database_Table(model=model)

    def updateData(self, obj, **kwargs):
        model = type(obj)
        CRUD_Model = get_crud_class(model_class=model)
        status, result = CRUD_Model.update(id=obj.id,
                                           **kwargs)
        print(status, result)
        if status != CRUD_Status.UPDATED:
            return
        self.toPage_Database_Table(model=model)

    def toPage_Database_Table_Read(self, obj):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        widget_create = Widget_ReadUpdateDelete(parent=parent,
                                                obj=obj,
                                                callback_back=self.toPage_Database_Table,
                                                callback_cancel=self.toPage_Database_Table,
                                                callback_update=None,
                                                callback_delete=None)

        parent_layout.addWidget(widget_create)

    def toPage_Database_Table_CreateData(self, model):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        widget_create = Widget_Create(parent=parent,
                                      model=model,
                                      callback_back=self.toPage_Database_Table,
                                      callback_cancel=self.toPage_Database_Table,
                                      callback_create=self.createData)

        parent_layout.addWidget(widget_create)

    def createData(self, model, **kwargs):
        CRUD_Model = get_crud_class(model_class=model)
        status, result = CRUD_Model.create(**kwargs)
        print(status, result)
        if status != CRUD_Status.CREATED:
            return
        self.toPage_Database_Table(model=model)

    def toPageDatabase_Table_Data(self, data):
        pass
    """ Page Database """


if __name__ == "__main__":
    app = QApplication([])
    window = MyApplication()
    window.show()
    app.exec()
