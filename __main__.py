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
TEST_USERNAME = 'interviewer1'
TEST_PASSWORD = 'interviewer'
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
        self.setWindowTitle("RMS SYSTEM")

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
        self.ui.pushButton_SettingsAccount.setText(
            get_translation('account_settings'))
        self.ui.pushButton_SettingsAccount.clicked.connect(
            self.toPage_AccountSettings)
        self.ui.pushButton_ChangePassword.setText(
            get_translation('change_password'))
        self.ui.pushButton_ChangePassword.clicked.connect(
            self.toPage_ChangePassword)
        self.ui.pushButton_ChangePassword_Cancel.clicked.connect(
            self.toPage_Settings)
        self.ui.pushButton_ChangePassword_Accept.clicked.connect(
            self.changePassword)

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
        self.ui.pushButton_ChangePassword.setIcon(
            QIcon(QPixmap(icon_change_password_path)))
        self.ui.pushButton_SettingsAccount.setIcon(
            QIcon(QPixmap(icon_settings_path)))

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

    def getLoggedInUser(self) -> User:
        logged_in_user = self.logged_in_user.state
        return logged_in_user

    def renderViewOnUserLoggedIn(self, is_logged_in: bool):
        if is_logged_in:
            self.ui.pushButton_SideMenu.setHidden(False)
            if not self.logged_in_user:
                print("ERROR: No user logged in")
                return
            self.toPage_Home()
            logged_in_user = self.getLoggedInUser()
            self.ui.label_UserName.setText(logged_in_user.name)
            self.ui.label_UserRole.setText(logged_in_user.role)
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
        sidemenu_action_button_setups.insert(0,
                                             [get_translation('home'), icon_home_path, self.toPage_Home])
        sidemenu_action_button_setups.append(
            [get_translation('settings'), icon_settings_path, self.toPage_Settings])
        sidemenu_action_button_setups.append(
            [get_translation('logout'), icon_logout_path, self.logout])
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

    def toPage_Home(self):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Home)

    # region Admin
    def renderAdmin(self):
        """ Sidemenu """
        sidemenu_action_button_setups = [
            [get_translation('database'), icon_database_path,
             self.toPage_Database]
        ]
        """ HOME """
        home_action_button_setups = [
            [f"Database ({len(all_models)})",
             icon_database_path, self.toPage_Database]
        ]
        self.renderBase(sidemenu_action_button_setups=sidemenu_action_button_setups,
                        home_action_button_setups=home_action_button_setups)
    # endregion Admin
    # region Candidate

    def renderCandidate(self):
        """ Sidemenu """
        sidemenu_action_button_setups = [
            [Job.info['description'][LANGUAGE], icon_job_path,
                partial(self.toPage_Candidate_Jobs)],
            ["My application forms", icon_application_form_path,
                self.toPage_Candidate_ApplicationForms]
        ]
        """ HOME """
        home_action_button_setups = [
            [f"{Job.info['description'][LANGUAGE]}", icon_job_path, partial(
                self.toPage_Candidate_Jobs)],
            [f"My application forms", icon_application_form_path,
                self.toPage_Candidate_ApplicationForms]
        ]
        self.renderBase(sidemenu_action_button_setups=sidemenu_action_button_setups,
                        home_action_button_setups=home_action_button_setups)

    def toPage_Candidate_Jobs(self, **kwargs):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        jobs = getAvaiableJobs()
        widget_table = Widget_Database_Table_Instances(parent=parent,
                                                       instances=jobs,
                                                       model=Job,
                                                       my_role=self.logged_in_user.state.role,
                                                       callback_select=self.toPage_Candidate_ApplicationForms_Selected,
                                                       callback_back=self.toPage_Home,
                                                       # callback_create=self.toPage_Database_Table_CreateData,
                                                       callback_read=self.toPage_Candidate_Jobs_Read)
        parent_layout.addWidget(widget_table)

    def toPage_Candidate_Jobs_Read(self, obj, model, **kwargs):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        widget_read = Widget_ReadUpdateDelete(parent=parent,
                                              obj=obj,
                                              model=model,
                                              callback_back=self.toPage_Candidate_Jobs)

        parent_layout.addWidget(widget_read)

    def toPage_Candidate_ApplicationForms_Selected(self, obj, model, **kwargs):
        """ Pass the job obj to create/update my application form """
        # Check if this job is already applied
        this_appliction_form = None
        my_application_forms = self.getMyApplicationForms_Candidate()
        for my_application_form in my_application_forms:
            if my_application_form.job_id == obj.id:
                this_appliction_form = my_application_form
        # If this job is already applied, show the form
        if this_appliction_form:
            # print("Already applied")
            self.toPage_Candidate_ApplicationForms_Update(
                obj=this_appliction_form, model=ApplicationForm)
        # Else create a new form with candidate_id = my_id
        else:
            self.toPage_Candidate_ApplicationForms_Create(obj=obj)

    def toPage_Candidate_ApplicationForms_Update(self, obj, **kwargs):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        widget_update = Widget_ReadUpdateDelete(parent=parent,
                                                obj=obj,
                                                model=ApplicationForm,
                                                my_role=self.logged_in_user.state.role,
                                                callback_back=self.toPage_Candidate_ApplicationForms,
                                                callback_cancel=self.toPage_Candidate_ApplicationForms,
                                                callback_update=self.updateCandidateApplicationForm,
                                                callback_delete=self.deleteCandidateApplicationForm)

        parent_layout.addWidget(widget_update)

    def deleteCandidateApplicationForm(self, obj, **kwargs):
        status, result = CRUD_ApplicationForm.delete(id=obj.id)
        print(status, result)
        if status != CRUD_Status.DELETED:
            QMessageBox.warning(self, "FAILED TO DELETE", get_translation(
                'action failed', language=LANGUAGE))
            return
        QMessageBox.about(self, "DELETED", get_translation(
            'action completed', language=LANGUAGE))
        self.toPage_Candidate_ApplicationForms()

    def getMyApplicationForms_Candidate(self) -> List[ApplicationForm]:
        # Candidate validation
        if self.logged_in_user.state.role != RoleStates.CANDIDATE.name:
            return
        application_forms = self.logged_in_user.state.application_forms
        return application_forms

    def toPage_Candidate_ApplicationForms(self, **kwargs):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        my_application_forms = self.getMyApplicationForms_Candidate()
        widget_table = Widget_Database_Table_Instances(parent=parent,
                                                       instances=my_application_forms,
                                                       model=ApplicationForm,
                                                       my_role=self.logged_in_user.state.role,
                                                       callback_update=self.toPage_Candidate_ApplicationForms_Update,
                                                       callback_back=self.toPage_Home,
                                                       callback_delete=self.deleteCandidateApplicationForm,
                                                       # callback_create=self.toPage_Candidate_ApplicationForms_Create,
                                                       callback_read=self.toPage_Candidate_ApplicationForms_Read)
        parent_layout.addWidget(widget_table)

    def toPage_Candidate_ApplicationForms_Create(self, obj, **kwargs):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        widget_create = Widget_Create_MyApplicationForm(parent=parent,
                                                        candidate_id=self.logged_in_user.state.id,
                                                        obj=obj,
                                                        callback_back=self.toPage_Candidate_Jobs,
                                                        callback_cancel=self.toPage_Candidate_Jobs,
                                                        callback_create=self.createCandidateApplicationForm)

        parent_layout.addWidget(widget_create)

    def updateCandidateApplicationForm(self, obj, **kwargs):
        model = type(obj)
        CRUD_Model = get_crud_class(model_class=model)
        status, result = CRUD_Model.update(id=obj.id,
                                           **kwargs)
        print(status, result)
        if status != CRUD_Status.UPDATED:
            QMessageBox.warning(self, "FAILED TO UPDATE", get_translation(
                'action failed', language=LANGUAGE))
            return
        QMessageBox.about(self, "UPDATED", get_translation(
            'action completed', language=LANGUAGE))
        self.toPage_Candidate_ApplicationForms()

    def createCandidateApplicationForm(self, model=None, **kwargs):
        status, result = CRUD_ApplicationForm.create(**kwargs)
        if status != CRUD_Status.CREATED:
            QMessageBox.warning(self, "FAILED TO CREATE", get_translation(
                'action failed', language=LANGUAGE))
            return
        QMessageBox.about(self, "CREATED", get_translation(
            'action completed', language=LANGUAGE))
        self.toPage_Candidate_ApplicationForms()

    def toPage_Candidate_ApplicationForms_Read(self, obj, model, **kwargs):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        widget_read = Widget_ReadUpdateDelete(parent=parent,
                                              obj=obj,
                                              model=model,
                                              my_role=self.logged_in_user.state.role,
                                              callback_back=self.toPage_JobManager_InterviewerAssginments)

        parent_layout.addWidget(widget_read)

    # endregion Candidate
    # region Interviewer #TODO
    def renderInterviewer(self):
        """ Sidemenu """
        sidemenu_action_button_setups = [
            [Candidate.info['description'][LANGUAGE], icon_candidate_path,
             partial(self.toPage_Database_Table, model=Candidate)],
            [Job.info['description'][LANGUAGE], icon_job_path,
                partial(self.toPage_Database_Table, model=Job)],
            [InterviewerAssignment.info['description'][LANGUAGE], icon_interviewer_asignment_path,
                partial(self.toPage_Interviewer_InterviewerAssignments)],
        ]
        """ HOME """
        home_action_button_setups = [
            [Candidate.info['description'][LANGUAGE], icon_candidate_path,
             partial(self.toPage_Database_Table, model=Candidate)],
            [Job.info['description'][LANGUAGE], icon_job_path,
                partial(self.toPage_Database_Table, model=Job)],
            [InterviewerAssignment.info['description'][LANGUAGE], icon_interviewer_asignment_path,
                partial(self.toPage_Interviewer_InterviewerAssignments)],
        ]
        self.renderBase(sidemenu_action_button_setups=sidemenu_action_button_setups,
                        home_action_button_setups=home_action_button_setups)

    def toPage_Interviewer_InterviewerAssignments(self, **kwargs):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        my_interviewer_assignments = self.getMyInterviewerAssginments()
        widget_table = Widget_Database_Table_Instances(parent=parent,
                                                       instances=my_interviewer_assignments,
                                                       model=InterviewerAssignment,
                                                       my_role=self.logged_in_user.state.role,
                                                       callback_update=self.toPage_Interviewer_InterviewerAssignments_Update,
                                                       callback_back=self.toPage_Home)
        parent_layout.addWidget(widget_table)

    def toPage_Interviewer_InterviewerAssignments_Update(self, obj:InterviewerAssignment, **kwargs):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        widget_update = Widget_Interviewer_InterviewerAssignments_Update(parent=parent,
                                                obj=obj,
                                                my_role=self.logged_in_user.state.role,
                                                callback_back=self.toPage_Interviewer_InterviewerAssignments,
                                                callback_cancel=self.toPage_Interviewer_InterviewerAssignments,
                                                callback_update=self.fromPage_Interviewer_InterviewerAssignments_Update)

        parent_layout.addWidget(widget_update)
    
    def fromPage_Interviewer_InterviewerAssignments_Update(self, obj:InterviewerAssignment, application_form_status_id, **kwargs):
        is_good = True
        status, result = CRUD_InterviewerAssignment.update(id=obj.id,
                                                           **kwargs)
        print(status, result)
        if status != CRUD_Status.UPDATED:
            is_good = False

        status, result = CRUD_ApplicationForm.update(id=obj.application_form_id,
                                                           application_form_status_id=application_form_status_id)
        print(status, result)
        if status != CRUD_Status.UPDATED:
            is_good = False

        if is_good == False:
            QMessageBox.warning(self, "FAILED TO UPDATE", get_translation(
                'action failed', language=LANGUAGE))
            return
        QMessageBox.about(self, "UPDATED", get_translation(
            'action completed', language=LANGUAGE))
        self.toPage_Interviewer_InterviewerAssignments()

    # endregion Interviewer
    # region Job Manager

    def renderJobManager(self):
        """ Sidemenu """
        sidemenu_action_button_setups = [
            [Candidate.info['description'][LANGUAGE], icon_user_path,
             self.toPage_JobManager_Candidates],
            [Job.info['description'][LANGUAGE], icon_job_path,
                partial(self.toPage_Database_Table, model=Job)],
            [Interviewer.info['description'][LANGUAGE], icon_interviewer_path,
                partial(self.toPage_Database_Table, model=Interviewer)],
            [InterviewerAssignment.info['description'][LANGUAGE], icon_interviewer_asignment_path,
                partial(self.toPage_JobManager_InterviewerAssginments)],
        ]
        """ HOME """
        home_action_button_setups = [
            # [f"{get_translation('database')} ({len(all_models)})", icon_database_path, self.toPage_Database],
            [Candidate.info['description'][LANGUAGE], icon_user_path,
             self.toPage_JobManager_Candidates],
            [Job.info['description'][LANGUAGE], icon_job_path,
                partial(self.toPage_Database_Table, model=Job)],
            [Interviewer.info['description'][LANGUAGE], icon_interviewer_path,
                partial(self.toPage_Database_Table, model=Interviewer)],
            [InterviewerAssignment.info['description'][LANGUAGE], icon_interviewer_asignment_path,
                partial(self.toPage_JobManager_InterviewerAssginments)],
        ]
        self.renderBase(sidemenu_action_button_setups=sidemenu_action_button_setups,
                        home_action_button_setups=home_action_button_setups)

    def getMyInterviewerAssginments(self) -> List[InterviewerAssignment]:
        interviewer_assignments = self.logged_in_user.state.interviewer_assignments
        return interviewer_assignments

    def toPage_JobManager_InterviewerAssginments(self, **kwargs):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        my_interviewer_assignments = self.getMyInterviewerAssginments()
        widget_table = Widget_Database_Table_Instances(parent=parent,
                                                       instances=my_interviewer_assignments,
                                                       model=InterviewerAssignment,
                                                       my_role=self.logged_in_user.state.role,
                                                       callback_update=self.toPage_JobManager_InterviewerAssginments_Update,
                                                       callback_back=self.toPage_Home,
                                                       callback_delete=self.fromPage_JobManager_InterviewerAssginments_Delete,
                                                       # callback_create=self.toPage_Candidate_ApplicationForms_Create,
                                                       callback_read=self.toPage_Candidate_ApplicationForms_Read)
        parent_layout.addWidget(widget_table)

    def toPage_JobManager_InterviewerAssginments_Update(self, obj, model=None, **kwargs):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        widget_update = Widget_ReadUpdateDelete(parent=parent,
                                                obj=obj,
                                                model=InterviewerAssignment,
                                                my_role=self.logged_in_user.state.role,
                                                callback_back=self.toPage_JobManager_InterviewerAssginments,
                                                callback_cancel=self.toPage_JobManager_InterviewerAssginments,
                                                callback_update=self.fromPage_JobManager_InterviewerAssginments_Update,
                                                callback_delete=self.fromPage_JobManager_InterviewerAssginments_Delete)

        parent_layout.addWidget(widget_update)

    def fromPage_JobManager_InterviewerAssginments_Update(self, obj, **kwargs):
        model = type(obj)
        CRUD_Model = get_crud_class(model_class=model)
        status, result = CRUD_Model.update(id=obj.id,
                                           **kwargs)
        print(status, result)
        if status != CRUD_Status.UPDATED:
            QMessageBox.warning(self, "FAILED TO UPDATE", get_translation(
                'action failed', language=LANGUAGE))
            return
        QMessageBox.about(self, "UPDATED", get_translation(
            'action completed', language=LANGUAGE))
        self.toPage_JobManager_InterviewerAssginments()

    def fromPage_JobManager_InterviewerAssginments_Delete(self, obj, **kwargs):
        model = type(obj)
        CRUD_Model = get_crud_class(model_class=model)
        status, result = CRUD_Model.delete(id=obj.id)
        print(status, result)
        if status != CRUD_Status.DELETED:
            QMessageBox.warning(self, "FAILED TO DELETE", get_translation(
                'action failed', language=LANGUAGE))
            return
        QMessageBox.about(self, "DELETED", get_translation(
            'action completed', language=LANGUAGE))
        self.toPage_JobManager_InterviewerAssginments()

    def toPage_JobManager_Candidates(self, **kwargs):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        model = Candidate
        status, candidates = CRUD_Candidate.read_all()

        if status != CRUD_Status.FOUND:
            candidates = []

        show_candidates = [candidate for candidate in candidates if any(
            not form.interviewer_assignments and form.application_form_status_id != 3
            for form in candidate.application_forms
        )]

        widget_table = Widget_Database_Table_Instances(parent=parent,
                                                       instances=show_candidates,
                                                       model=model,
                                                       my_role=self.logged_in_user.state.role,
                                                       callback_back=self.toPage_Home,
                                                       callback_create=self.toPage_Database_Table_CreateData,
                                                       callback_select=self.toPage_JobManager_Candidate_ApplicationForms,
                                                       callback_read=self.toPage_JobManager_Candidates_Read,
                                                       callback_delete=self.toPage_Database_Table_Delete)
        parent_layout.addWidget(widget_table)

    def toPage_JobManager_Candidates_Read(self, obj: Candidate, **kwargs):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        widget_read = Widget_ReadUpdateDelete(parent=parent,
                                              obj=obj,
                                              model=Candidate,
                                              my_role=self.logged_in_user.state.role,
                                              callback_back=self.toPage_JobManager_Candidates)

        parent_layout.addWidget(widget_read)

    def toPage_JobManager_Candidate_ApplicationForms(self, obj: Candidate = None, candidate=None, **kwargs):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        if candidate:
            obj = candidate
        candidate_application_forms = obj.application_forms
        show_candidate_application_forms = [
            candidate_application_form
            for candidate_application_form in candidate_application_forms
            if not candidate_application_form.interviewer_assignments
            and candidate_application_form.application_form_status_id != 3
        ]

        widget_table = Widget_Database_Table_Instances(parent=parent,
                                                       instances=show_candidate_application_forms,
                                                       model=ApplicationForm,
                                                       my_role=self.logged_in_user.state.role,
                                                       callback_back=self.toPage_JobManager_Candidates,
                                                       callback_update=None,
                                                       callback_select=self.toPage_JobManager_Candidate_ApplicationForms_Select,
                                                       callback_read=self.toPage_JobManager_Candidate_ApplicationForms_Read,
                                                       callback_delete=self.rejectCandidateApplicationForm)
        parent_layout.addWidget(widget_table)

    def rejectCandidateApplicationForm(self, obj: ApplicationForm, **kwargs):
        status, updated_application_form = CRUD_ApplicationForm.update(
            id=obj.id, application_form_status_id=3)  # Reject status id = 3
        if status != CRUD_Status.UPDATED:
            QMessageBox.warning(self, "FAILED", get_translation(
                'action failed', language=LANGUAGE))
            return
        QMessageBox.about(self, "REJECTED CANDIDATE'S APPLICATION FORM", get_translation(
            'action completed', language=LANGUAGE))
        self.toPage_JobManager_Candidates()

    def toPage_JobManager_Candidate_ApplicationForms_Read(self, obj: ApplicationForm, **kwargs):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        widget_read = Widget_ReadUpdateDelete(parent=parent,
                                              obj=obj,
                                              model=ApplicationForm,
                                              my_role=self.logged_in_user.state.role,
                                              callback_back=partial(self.toPage_JobManager_Candidate_ApplicationForms, candidate=obj.candidate))

        parent_layout.addWidget(widget_read)

    def toPage_JobManager_Candidate_ApplicationForms_Select(self, obj: ApplicationForm, **kwargs):
        selected_application_form = obj
        my_interviewer_assignments = self.getMyInterviewerAssginments()
        found_interviewer_assignment = None
        for my_interviewer_assignment in my_interviewer_assignments:
            if (my_interviewer_assignment.application_form == selected_application_form):
                found_interviewer_assignment = my_interviewer_assignment
                break
        if found_interviewer_assignment:
            self.toPage_JobManager_InterviewerAssginments_UpdateReadDelete(obj=found_interviewer_assignment,
                                                                           application_form=selected_application_form)
        else:
            self.toPage_JobManager_InterviewerAssginments_Create(obj=found_interviewer_assignment,
                                                                 application_form=selected_application_form)

    def toPage_JobManager_InterviewerAssginments_Create(self, obj: InterviewerAssignment, application_form: ApplicationForm, **kwargs):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        widget_create = Widget_Create_InterviewerAssignment(parent=parent,
                                                            job_manager=self.getLoggedInUser(),
                                                            application_form=application_form,
                                                            callback_back=partial(
                                                                self.toPage_JobManager_Candidate_ApplicationForms, candidate=application_form.candidate),
                                                            callback_cancel=partial(
                                                                self.toPage_JobManager_Candidate_ApplicationForms, candidate=application_form.candidate),
                                                            callback_create=self.createData)

        parent_layout.addWidget(widget_create)

    def toPage_JobManager_InterviewerAssginments_UpdateReadDelete(self, obj: InterviewerAssignment, application_form: ApplicationForm, **kwargs):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        widget_update = Widget_ReadUpdateDelete(parent=parent,
                                                obj=obj,
                                                model=InterviewerAssignment,
                                                my_role=self.logged_in_user.state.role,
                                                callback_back=partial(
                                                    self.toPage_JobManager_Candidate_ApplicationForms, candidate=application_form.candidate),
                                                callback_cancel=partial(
                                                    self.toPage_JobManager_Candidate_ApplicationForms, candidate=application_form.candidate),
                                                callback_update=self.updateData,
                                                callback_delete=self.deleteData)

        parent_layout.addWidget(widget_update)

    # endregion Job Manager
    # endregion renderview based on user role
    # endregion

    # region Page Settings
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

    # endregion

    # region Page Database

    def toPage_Database(self, **kwargs):
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

    def toPage_Database_Table(self, model, **kwargs):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        CRUD_Class = get_crud_class(model_class=model)
        status, instances = CRUD_Class.read_all()

        if status != CRUD_Status.FOUND:
            instances = []
        callback_select = kwargs.get('callback_select', None)
        widget_table = Widget_Database_Table_Instances(parent=parent,
                                                       instances=instances,
                                                       model=model,
                                                       my_role=self.logged_in_user.state.role,
                                                       callback_back=self.toPage_Home,
                                                       callback_create=self.toPage_Database_Table_CreateData,
                                                       callback_select=callback_select,
                                                       callback_read=self.toPage_Database_Table_Read,
                                                       callback_update=self.toPage_Database_Table_Update,
                                                       callback_delete=self.toPage_Database_Table_Delete)
        parent_layout.addWidget(widget_table)

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

    def toPage_Database_Table_Read(self, obj, model):
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_Database)
        parent = self.ui.page_Database
        parent_layout = parent.layout()
        clearAllWidgets(parent)
        widget_read = Widget_ReadUpdateDelete(parent=parent,
                                              obj=obj,
                                              model=model,
                                              callback_back=self.toPage_Database_Table,
                                              callback_cancel=self.toPage_Database_Table,
                                              callback_update=None,
                                              callback_delete=None)

        parent_layout.addWidget(widget_read)

    def toPage_Database_Table_Update(self, obj, model, **kwargs):
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

    def toPage_Database_Table_Delete(self, obj, **kwargs):
        self.deleteData(obj)

    def createData(self, model, **kwargs):
        CRUD_Model = get_crud_class(model_class=model)
        status, result = CRUD_Model.create(**kwargs)
        print(status, result)
        if status != CRUD_Status.CREATED:
            QMessageBox.warning(self, "FAILED TO CREATE", get_translation(
                'action failed', language=LANGUAGE))
            return
        QMessageBox.about(self, "CREATED", get_translation(
            'action completed', language=LANGUAGE))
        self.toPage_Database_Table(model=model)

    def updateData(self, obj, **kwargs):
        model = type(obj)
        CRUD_Model = get_crud_class(model_class=model)
        status, result = CRUD_Model.update(id=obj.id,
                                           **kwargs)
        print(status, result)
        if status != CRUD_Status.UPDATED:
            QMessageBox.warning(self, "FAILED TO UPDATE", get_translation(
                'action failed', language=LANGUAGE))
            return
        QMessageBox.about(self, "UPDATED", get_translation(
            'action completed', language=LANGUAGE))
        self.toPage_Database_Table(model=model)

    def deleteData(self, obj, **kwargs):
        model = type(obj)
        CRUD_Model = get_crud_class(model_class=model)
        status, result = CRUD_Model.delete(id=obj.id)
        print(status, result)
        if status != CRUD_Status.DELETED:
            QMessageBox.warning(self, "FAILED TO DELETE", get_translation(
                'action failed', language=LANGUAGE))
            return
        QMessageBox.about(self, "DELETED", get_translation(
            'action completed', language=LANGUAGE))
        self.toPage_Database_Table(model=model)

    # endregion Page Database
if __name__ == "__main__":
    app = QApplication([])
    window = MyApplication()
    window.show()
    app.exec()
