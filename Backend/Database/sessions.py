from enum import EnumMeta
from typing import Callable, List, Tuple
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from Backend.Database.password import db_password
from Backend.Database.models import *
from Backend.Services.hash import hash_string
# Create an SQLite engine
# echo = True to logging any SQL query to console
import platform

db_type = 'mysql'
db_connector_module = 'pymysql'
db_host = 'gateway01.ap-northeast-1.prod.aws.tidbcloud.com'
db_port = '4000'
db_username = '3xKs6MSRB2UKUd5.root'
if platform.system() == "Windows":
    db_ssl_ca_path = 'C:/cer.pem' # https://letsencrypt.org/certs/isrgrootx1.pem
else:
    db_ssl_ca_path = '/etc/ssl/cert.pem'
db_password = db_password

ECHO = False
TEST = True

connection_url_string = f"{db_type}+{db_connector_module}://{db_username}:{db_password}@{db_host}:{db_port}/test?ssl_ca={db_ssl_ca_path}&ssl_verify_cert=true&ssl_verify_identity=true"
if TEST:
    engine = create_engine('sqlite:///Backend/Database/db.sqlite', echo=ECHO)
else:
    engine = create_engine(connection_url_string, echo=ECHO)

# Create the table in the database
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)
# default_session = Session()

session = Session()

class Base_Status(EnumMeta):
    """ # Base class for Enum Status classes\n
    ### Example useage:\n
    - CRUD_Status.ERROR is equal to 'ERROR Đã có lỗi xảy ra'
    - CRUD_Status.ERROR.name is equal to 'ERROR'\n
    - CRUD_Status.ERROR.value is equal to 'Đã có lỗi xảy ra'
    """
    ERROR = 'Đã có lỗi xảy ra'
    FAILED = 'Thất bại'
    SUCCESS = 'Thành công'

    def __str__(self) -> str:
        return f'{self.name} {self.value}'


class CRUD_Status(Base_Status):
    CREATED = 'Đã tạo'
    FOUND = 'Tìm thấy'
    NOT_FOUND = 'Không tìm thấy'
    UPDATED = 'Đã cập nhật'
    DELETED = 'Đã xoá'
    # NO_CHANGES = 'Không có thay đổi'
    # EXISTED = 'Đã tồn tại'

def crud_handler_wrapper(func: Callable) -> Tuple[CRUD_Status, any]:
    def wrapper(*args, **kwargs)->Tuple[CRUD_Status, any]:
        try:
            result = func(*args, **kwargs)
            session.commit()
            return result
        except Exception as e:
            session.rollback()
            return CRUD_Status.ERROR, e
    return wrapper

def read_handler_wrapper(func: Callable) -> Tuple[CRUD_Status, any]:
    def wrapper(*args, **kwargs)->Tuple[CRUD_Status, any]:
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            return CRUD_Status.ERROR, e
    return wrapper

class CRUD_Base:
    # Subclasses should define the SQLAlchemy model class
    model = None
    
    @classmethod
    @crud_handler_wrapper
    def create(cls, **kwargs) -> Tuple[CRUD_Status, any]:
        if 'password' in kwargs:
            kwargs['password_hash'] = hash_string(kwargs.pop('password'))
        new_instance = cls.model(**kwargs)
        session.add(new_instance)
        return CRUD_Status.CREATED, new_instance

    @classmethod
    @read_handler_wrapper
    def read(cls, id: int) -> Tuple[CRUD_Status, any]:
        found_instance = session.query(cls.model).get(id)
        if not found_instance:
            return CRUD_Status.NOT_FOUND, None
        return CRUD_Status.FOUND, found_instance

    @classmethod
    @read_handler_wrapper
    def read_all(cls) -> Tuple[CRUD_Status, List[any]]:
        found_instances = session.query(cls.model).all()
        if not found_instances:
            return CRUD_Status.NOT_FOUND, []
        return CRUD_Status.FOUND, found_instances

    @classmethod
    @crud_handler_wrapper
    def update(cls, id: int, **kwargs) -> Tuple[CRUD_Status, any]:
        state, found_instance = cls.read(id)
        if state == CRUD_Status.NOT_FOUND:
            return CRUD_Status.NOT_FOUND, None
        if 'password' in kwargs:
            kwargs['password_hash'] = hash_string(kwargs.pop('password'))
        for key, value in kwargs.items():
            setattr(found_instance, key, value)
        return CRUD_Status.UPDATED, found_instance

    @classmethod
    @crud_handler_wrapper
    def delete(cls, id: int) -> Tuple[CRUD_Status, any]:
        state, found_instance = cls.read(id)
        if state == CRUD_Status.NOT_FOUND:
            return CRUD_Status.NOT_FOUND, None
        session.delete(found_instance)
        return CRUD_Status.DELETED, None
    
class Login_Status(Base_Status):
    LOGIN_FAILED = "Không thể đăng nhập, xin kiểm tra lại thông tin"
    LOGIN_SUCCESS = "Đăng nhập thành công"
    
class CRUD_User(CRUD_Base):
    model = User

    @classmethod
    def login(cls, username: str, password: str) -> Tuple[Login_Status, any]:
        """ Login with username and password """
        try:
            password_hash = hash_string(password)
            user = session.query(cls.model).filter_by(username=username, password_hash=password_hash).first()
            if user:
                return Login_Status.LOGIN_SUCCESS, user
            else:
                return Login_Status.LOGIN_FAILED, None
        except Exception as e:
            return Login_Status.ERROR, e

class CRUD_Admin(CRUD_Base):
    model = Admin

class CRUD_JobManager(CRUD_Base):
    model = JobManager

class CRUD_Interviewer(CRUD_Base):
    model = Interviewer

class CRUD_Candidate(CRUD_Base):
    model = Candidate

class CRUD_Gender(CRUD_Base):
    model = Gender

class CRUD_RequisitionStatus(CRUD_Base):
    model = RequisitionStatus

class CRUD_Requisition(CRUD_Base):
    model = Requisition

class CRUD_ApplicationForm(CRUD_Base):
    model = ApplicationForm

class CRUD_InterviewerAssignment(CRUD_Base):
    model = InterviewerAssignment

class CRUD_Job(CRUD_Base):
    model = Job

class CRUD_JobStatus(CRUD_Base):
    model = JobStatus

def get_crud_class(model_class)->CRUD_Base:
    # Assuming that the CRUD classes are defined in the same module
    crud_class_name = f"CRUD_{model_class.__name__}"

    # Use globals() to get the class from the global namespace
    crud_class = globals().get(crud_class_name)

    return crud_class