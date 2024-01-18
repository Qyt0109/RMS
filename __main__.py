# region Import Modules
""" Backend modules """
import typing
from functools import partial
from PyQt6 import QtWidgets
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
from PyQt6.QtGui import QPixmap, QIcon
from Frontend.Design.design_ui import Ui_MainWindow
from Frontend.Helper.popups import *
from Frontend.Helper.helper import *
from Frontend.Helper import helper
from Backend.Services.time import to_ddmmYYYY_str, to_HHMMSS_ddmmYYYY_str
from Backend.Database.sessions import *
""" Backend modules """
""" Frontend modules """
""" Frontend modules """
""" PyQt6 modules """
""" Python modules """
""" Python modules """
# endregion Import Modules

""" #FIXME TEST ONLY """
TEST_USERNAME = 'job_manager1'
TEST_PASSWORD = 'job_manager'
TEST_DEV = True
if TEST_DEV:
    from Backend.Services.db_test import *
    initTestDatabase()
""" #FIXME TEST ONLY """

class MyApplication(QMainWindow):
    # region Init MyApplication class
    def __init__(self):
        super().__init__()
        """ Set up the user interface from Designer"""
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        """ Init icons """
        self.init_icons()

        """ Signal variables """
        self.logged_in_user = QSignalVariable(None)
        self.logged_in_user.stateChanged.connect(self.renderViewOnUserLoggedIn)

        # Extended design and setup for ui
        self.toPage_Login()  # Started at login page

        # Connect signals and slots
        """ SideMenu button """
        self.ui.pushButton_SideMenu.clicked.connect(self.toogleSideMenu)
        self.ui.pushButton_SideMenu.setHidden(True)
        self.hideSideMenu(True)
        """ Login button """
        self.ui.pushButton_Login_Login.clicked.connect(self.login)

        """ Show password buttons """
        self.initPasswordShowButtons()

        """ MainMenu """

        """ Page Settings """
        self.ui.pushButton_SettingsAccount.setText(get_translation('account_settings'))
        self.ui.pushButton_SettingsAccount.clicked.connect(self.toPage_AccountSettings)
        self.ui.pushButton_ChangePassword.setText(get_translation('change_password'))
        self.ui.pushButton_ChangePassword.clicked.connect(self.toPage_ChangePassword)
        self.ui.pushButton_ChangePassword_Cancel.clicked.connect(self.toPage_Settings)
        self.ui.pushButton_ChangePassword_Accept.clicked.connect(self.changePassword)

    def init_icons(self):
        # self.ui.pushButton_Home.setIcon(QIcon(QPixmap(icon_home_path)))
        self.ui.pushButton_SideMenu.setIcon(QIcon(QPixmap(icon_menu_path)))
        background_image_path = 'Frontend/Resources/Images/default-avatar.png'
        self.ui.pushButton_UserAvatar.setStyleSheet(f"""
                                                    border-image: url({background_image_path});
                                                    background-repeat: no-repeat;
                                                    background-position: center;
                                                    """)
        self.ui.pushButton_Login_PasswordShow.setIcon(
            QIcon(QPixmap(icon_hide_path)))
        self.ui.pushButton_ChangePassword_OldPasswordShow.setIcon(
            QIcon(QPixmap(icon_hide_path)))
        self.ui.pushButton_ChangePassword_NewPasswordShow.setIcon(
            QIcon(QPixmap(icon_hide_path)))
        self.ui.pushButton_ChangePassword_NewPasswordRetypeShow.setIcon(
            QIcon(QPixmap(icon_hide_path)))
        self.ui.pushButton_ChangePassword.setIcon(QIcon(QPixmap(icon_change_password_path)))
        self.ui.pushButton_SettingsAccount.setIcon(QIcon(QPixmap(icon_settings_path)))


    def initPasswordShowButtons(self):
        """ Show password buttons """
        self.ui.pushButton_Login_PasswordShow.clicked.connect(partial(togglePasswordVisibility,
                                                                      line_edit=self.ui.lineEdit_Login_Password,
                                                                      button=self.ui.pushButton_Login_PasswordShow))

        self.ui.pushButton_ChangePassword_OldPasswordShow.clicked.connect(partial(togglePasswordVisibility,
                                                                                  line_edit=self.ui.lineEdit_ChangePassword_OldPassword,
                                                                                  button=self.ui.pushButton_ChangePassword_OldPasswordShow))

        self.ui.pushButton_ChangePassword_NewPasswordShow.clicked.connect(partial(togglePasswordVisibility,
                                                                                  line_edit=self.ui.lineEdit_ChangePassword_NewPassword,
                                                                                  button=self.ui.pushButton_ChangePassword_NewPasswordShow))

        self.ui.pushButton_ChangePassword_NewPasswordRetypeShow.clicked.connect(partial(togglePasswordVisibility,
                                                                                        line_edit=self.ui.lineEdit_ChangePassword_NewPasswordRetype,
                                                                                        button=self.ui.pushButton_ChangePassword_NewPasswordRetypeShow))
    # endregion
    # region SideMenu

    def hideSideMenu(self, is_hide: bool):
        self.ui.frame_SideMenu.setHidden(is_hide)

    def toogleSideMenu(self):
        is_hide = self.ui.frame_SideMenu.isHidden()
        self.hideSideMenu(is_hide=not is_hide)
    # endregion
    # region Login Logout Handler
    # region Login Logout
    def toPage_Login(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Login)

    def login(self):
        username = self.ui.lineEdit_Login_Username.text()
        password = self.ui.lineEdit_Login_Password.text()
        """ #FIXME TEST ONLY """
        if TEST_DEV:
            username = username if username else TEST_USERNAME
            password = password if password else TEST_PASSWORD
        """ #FIXME TEST ONLY """
        status, result = CRUD_User.login(username=username, password=password)
        if status == Login_Status.LOGIN_SUCCESS:
            self.logged_in_user.state = result
        else:
            popup = PopupOk(title="Đăng nhập thất bại", message=status)
            popup.exec()
            # self.ui.label_Login_Notification.setText(status)

    def logout(self):
        confirm_dialog = PopupYesNo(parent=self.ui.centralwidget,
                                    title="Logout",
                                    message='Confirm logging out?',
                                    yes_button_text="LOGOUT",
                                    no_button_text="Cancel")

        result = confirm_dialog.exec()
        print(result)

        if result == QDialog.DialogCode.Accepted:
            self.hideSideMenu(True)
            self.logged_in_user.state = None
            self.toPage_Login()
    # endregion Login Logout
    # region renderview based on user role

    def renderViewOnUserLoggedIn(self, is_logged_in: bool):
        if is_logged_in:
            self.ui.pushButton_SideMenu.setHidden(False)
            if not self.logged_in_user:
                print("ERROR: No user logged in")
                return
            self.toPage_Home()
            self.ui.label_UserName.setText(self.logged_in_user.state.name)
            self.ui.label_UserRole.setText(self.logged_in_user.state.role)
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

    def renderBase(self, sidemenu_action_button_setups, home_action_button_setups):
        """ Sidemenu """
        sidemenu_action_button_setups.append([get_translation('settings'), icon_settings_path, self.toPage_Settings])
        sidemenu_action_button_setups.append([get_translation('logout'), icon_logout_path, self.logout])
        sidemenu_action_buttons = []
        for sidemenu_action_button_setup in sidemenu_action_button_setups:
            sidemenu_action_buttons.append(ActionButton(parent=self.ui.frame_ActionButtons,
                                               text=sidemenu_action_button_setup[0],
                                               icon_path=sidemenu_action_button_setup[1],
                                               signal=sidemenu_action_button_setup[2],
                                               stylesheet_normal=sidemenu_stylesheet_normal,
                                               stylesheet_hover=sidemenu_stylesheet_hover))
        initActionButtons(parent_widget=self.ui.frame_ActionButtons,
                          action_buttons=sidemenu_action_buttons)
        """ HOME """        
        home_action_buttons = []
        for home_action_button_setup in home_action_button_setups:
            action_button = (ActionButton(parent=self.ui.frame_ActionButtons,
                                               text=home_action_button_setup[0],
                                               icon_path=home_action_button_setup[1],
                                               signal=home_action_button_setup[2],
                                               stylesheet_normal=home_button_stylesheet_normal,
                                               stylesheet_hover=home_button_stylesheet_hover))
            action_button.setMaximumSize(400, 200)
            action_button.setMinimumSize(120, 120)
            home_action_buttons.append(action_button)
        
        initActionButtons(parent_widget=self.ui.frame_Home,
                          action_buttons=home_action_buttons)
        
    def renderAdmin(self):
        """ Sidemenu """
        sidemenu_action_button_setups = [
            [get_translation('home'), icon_home_path, self.toPage_Home],
            [get_translation('database'), icon_database_path, self.toPage_Database],
        ]
        """ HOME """
        home_action_button_setups = [
            [f"Database\n({len(all_models)})", icon_database_path, self.toPage_Database]
        ]
        self.renderBase(sidemenu_action_button_setups=sidemenu_action_button_setups,
                        home_action_button_setups=home_action_button_setups)

    def renderCandidate(self):
        print("Candidate")

    def renderInterviewer(self):
        print("Interviewer")

    def renderJobManager(self):
        """ Sidemenu """
        sidemenu_action_button_setups = [
            [get_translation('home'), icon_home_path, self.toPage_Home],
            # [get_translation('database'), icon_database_path, self.toPage_Database],
            [get_translation('candidate'), icon_user_path, partial(self.toPage_Database_Table, model=Candidate)],
            [Job.info['description'][LANGUAGE], icon_job_path, partial(self.toPage_Database_Table, model=Job)],
            [Interviewer.info['description'][LANGUAGE], icon_interviewer_path, partial(self.toPage_Database_Table, model=Interviewer)],
            [InterviewerAssignment.info['description'][LANGUAGE], icon_interviewer_asignment_path, partial(self.toPage_Database_Table, model=InterviewerAssignment)],
        ]
        """ HOME """
        status, candidates = CRUD_Candidate.read_all()
        status, jobs = CRUD_Job.read_all()
        status, interviewers = CRUD_Interviewer.read_all()
        status, interviewer_assignments = CRUD_InterviewerAssignment.read_all()

        home_action_button_setups = [
            # [f"{get_translation('database')} ({len(all_models)})", icon_database_path, self.toPage_Database],
            [f"{Candidate.info['description'][LANGUAGE]} ({len(candidates)})", icon_candidate_path, partial(self.toPage_Database_Table, model=Candidate)],
            [f"{Job.info['description'][LANGUAGE]} ({len(jobs)})", icon_job_path, partial(self.toPage_Database_Table, model=Job)],
            [f"{Interviewer.info['description'][LANGUAGE]} ({len(interviewers)})", icon_interviewer_path, partial(self.toPage_Database_Table, model=Interviewer)],
            [f"{InterviewerAssignment.info['description'][LANGUAGE]} ({len(interviewer_assignments)})", icon_interviewer_asignment_path, partial(self.toPage_Database_Table, model=InterviewerAssignment)],
        ]
        self.renderBase(sidemenu_action_button_setups=sidemenu_action_button_setups,
                        home_action_button_setups=home_action_button_setups)
    # endregion renderview based on user role
    # endregion
        
    """ Page Settings """
    def toPage_Settings(self, **kwargs):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Settings)

    def toPage_AccountSettings(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        widget_update = Widget_SelfUpdate(parent=parent,
                                                obj=self.logged_in_user.state,
                                                callback_back=self.toPage_Settings,
                                                callback_cancel=self.toPage_Settings,
                                                callback_update=self.selfAccountUpdate)

        parent_layout.addWidget(widget_update)

    def selfAccountUpdate(self, obj, **kwargs):
        model = type(obj)
        CRUD_Model = get_crud_class(model_class=model)
        status, result = CRUD_Model.update(id=obj.id,
                                           **kwargs)
        print(status, result)
        if status != CRUD_Status.UPDATED:
            return
        self.toPage_Settings()
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
    # region Home

    def toPage_Home(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Home)
    # endregion Home

    def toPage_List_Users(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_List)
        state, result = CRUD_User.read_all()
        renderView_List_Users(parent_frame=self.ui.frame_List,
                              users=result,
                              callback_detail=self.toPage_List_UserDetail,
                              callback_delete=self.userDelete)

    def userDelete(self, user: User):
        if not user:
            return
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


    """ Page Database """

    def toPage_Database(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        models = all_models
        widget_database = Widget_Database(parent=parent,
                                          models=models,
                                          callback_back=self.toPage_Home,
                                          callback_select_table=self.toPage_Database_Table)
        parent_layout.addWidget(widget_database)

    def toPage_Database_Table(self, model):
        print(model)
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        widget_table = Widget_Database_Table(parent=parent,
                                             model=model,
                                             my_role=self.logged_in_user.state.role,
                                             callback_back=self.toPage_Home,
                                             callback_create=self.toPage_Database_Table_CreateData,
                                             callback_read=self.toPage_Database_Table_Read,
                                             callback_update=self.toPage_Database_Table_Update,
                                             callback_delete=self.toPage_Database_Table_Delete)
        parent_layout.addWidget(widget_table)

    def toPage_Database_Table_Delete(self, obj):
        self.deleteData(obj)

    def toPage_Database_Table_Update(self, obj, model):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        widget_update = Widget_ReadUpdateDelete(parent=parent,
                                                obj=obj,
                                                model=model,
                                                my_role=self.logged_in_user.state.role,
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

    def toPage_Database_Table_Read(self, obj, model):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        widget_read = Widget_ReadUpdateDelete(parent=parent,
                                                obj=obj,
                                                model = model,
                                                callback_back=self.toPage_Database_Table,
                                                callback_cancel=self.toPage_Database_Table,
                                                callback_update=None,
                                                callback_delete=None)

        parent_layout.addWidget(widget_read)

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
