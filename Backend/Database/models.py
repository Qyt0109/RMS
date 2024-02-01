from enum import Enum
from datetime import datetime

from sqlalchemy import Table, case, create_engine, ForeignKey, Column, Integer, Float, BLOB, Boolean, DATETIME, DATE, String, LargeBinary, DateTime, Text, func, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

from Backend.Services.time import to_ddmmYYYY_str, to_HHMMSS_ddmmYYYY_str

# Create a base class for declarative models
Base = declarative_base()

STRING_LENGTH = 64

class OperandStates(Enum):
    CREATE = 'create'
    READ = 'read',
    UPDATE = 'update'
    DELETE = 'delete'

class RoleStates(Enum):
    USER = 'Người dùng'
    ADMIN = 'Quản trị viên hệ thống'
    CANDIDATE = 'Ứng viên'
    INTERVIEWER = 'Người phỏng vấn'
    JOB_MANAGER = 'Người quản lý công việc'


class FileTypes(Enum):
    ALL_FILE = 'All Files (*)'
    IMAGE_FILE = 'Image Files (*.png *.jpg *.bmp *.gif)'
    PDF_FILE = 'PDF Files (*.pdf)'


class ReprAble:
    def __repr__(self):
        class_name = self.__class__.__name__
        attributes = []
        abandon = ['_sa_class_manager',
                   '_sa_class_state']

        for attr, value in self.__dict__.items():
            # Exclude _sa_instance_state attribute
            if attr.startswith("__") or attr.startswith("_"):
                continue
            if isinstance(value, datetime):
                formatted_datetime = to_HHMMSS_ddmmYYYY_str(value)
                attributes.append(f'{attr}={formatted_datetime}')
            else:
                attributes.append(f'{attr}={repr(value)}')

        return f'{class_name}({", ".join(attributes)})'


class Genders(Enum):
    MALE = 'Nam'
    FEMALE = 'Nữ'


"""
hide            T           T           F           F

updateable      F           T           F           T

state           hide        hide        readonly    updateable

if not hide:
    if updateable:
        state = updateable
    else:
        state = readonly
else:
    state = hide

"""


class User(Base, ReprAble):
    info = {
        'description': {
            'en': 'User',
            'vi': 'Người dùng'
        },
        'permission':
        {
            # Permission at List page
            'create':
            [
                RoleStates.ADMIN.name
            ],
            'read':
            [
                RoleStates.ADMIN.name,
                RoleStates.JOB_MANAGER.name,
                RoleStates.INTERVIEWER.name
            ],
            'update':
            [
                RoleStates.ADMIN.name
            ],
            'delete':
            [
                RoleStates.ADMIN.name
            ]
        }
    }
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(STRING_LENGTH), unique=True, nullable=False,
                      info={
                          'description':
                          {
                              'en': 'Username',
                              'vn': 'Tên tài khoản'
                          },
                          'hide':
                          {
                              RoleStates.CANDIDATE.name,
                              RoleStates.INTERVIEWER.name,
                              RoleStates.JOB_MANAGER.name,
                              RoleStates.USER.name
                          },
                          'updateable':
                          [
                              RoleStates.ADMIN.name
                          ]})

    password_hash = Column(String(STRING_LENGTH), nullable=False,
                           info={
                               'description':
                               {
                                   'en': 'Password hash',
                                   'vn': 'Mã băm của mật khẩu'
                               },
                               'hide':
                               {
                                   RoleStates.CANDIDATE.name,
                                   RoleStates.INTERVIEWER.name,
                                   RoleStates.JOB_MANAGER.name,
                                   RoleStates.USER.name
                               },
                               'updateable':
                               [
                                   RoleStates.ADMIN.name
                               ]})
    name = Column(String(STRING_LENGTH), nullable=False,
                  info={'description': {
                      'en': 'Full Name',
                      'vn': 'Họ và tên'
                  },
        'updateable':
        [
                      RoleStates.ADMIN.name
                  ]})
    email = Column(String(STRING_LENGTH), unique=True, nullable=False,
                   info={'description': {
                       'en': 'Email',
                       'vn': 'Địa chỉ Email'
                   },
        'updateable':
        [
                       RoleStates.ADMIN.name
                   ]})
    phone_number = Column(String(STRING_LENGTH),
                          info={'description': {
                              'en': 'Phone Number',
                              'vn': 'Số điện thoại'
                          },
        "updateable":
        [
                              RoleStates.ADMIN.name
                          ]})
    birthday = Column(Date, nullable=False,
                      info={'description': {
                          'en': 'Birthday',
                          'vn': 'Ngày sinh'
                      },
                          "updateable":
                          [
                              RoleStates.ADMIN.name
                      ]})
    role = Column(String(STRING_LENGTH),
                  info={
                      'description':
                      {
                          'en': 'User Role',
                          'vn': 'Vai trò người dùng'
                      },
        'hide':
        {
                          # RoleStates.ADMIN.name,
                          RoleStates.CANDIDATE.name,
                          RoleStates.INTERVIEWER.name,
                          RoleStates.JOB_MANAGER.name,
                          RoleStates.USER.name
                      }})
    avatar = Column(LargeBinary,
                    info={'description': {
                        'en': 'Avatar',
                        'vn': 'Ảnh đại diện'
                    },
                        "updateable":
                        [
                        RoleStates.ADMIN.name
                    ],
                        'filetype': FileTypes.IMAGE_FILE.value
                    })
    # created_time = Column(DateTime, default=datetime.now())

    # n-1 relationships
    gender_id = Column(Integer, ForeignKey('genders.id'),
                       info={'description': {
                           'en': 'Gender',
                           'vn': 'Giới tính'
                       },
        "updateable":
        [
                           RoleStates.ADMIN.name
                       ]})
    gender = relationship('Gender', back_populates='users')

    __mapper_args__ = {
        'polymorphic_identity': RoleStates.USER.name,
        'polymorphic_on': role,
        'with_polymorphic': '*'
    }


class Admin(User):
    info = {
        'description': {
            'en': 'Admin',
            'vi': 'Quản trị viên'
        },
        'permission':
        {
            # Permission at List page
            'create':
            [
                RoleStates.ADMIN.name
            ],
            'read':
            [
                RoleStates.ADMIN.name
            ],
            'update':
            [
                RoleStates.ADMIN.name
            ],
            'delete':
            [
                RoleStates.ADMIN.name
            ]
        }
    }
    __tablename__ = 'admins'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    # Other Admin's column here...

    __mapper_args__ = {
        'polymorphic_identity': RoleStates.ADMIN.name,
        'polymorphic_load': 'inline'
    }


class Candidate(User):
    info = {
        'description': {
            'en': 'Candidate',
            'vi': 'Ứng viên'
        },
        'permission':
        {
            # Permission at List page
            'create':
            [
                RoleStates.ADMIN.name
            ],
            'read':
            [
                RoleStates.ADMIN.name
            ],
            'update':
            [
                RoleStates.ADMIN.name
            ],
            'delete':
            [
                RoleStates.ADMIN.name
            ]
        }
    }
    __tablename__ = 'candidates'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    citizen_identification_code = Column(String(length=STRING_LENGTH),
                                         info={'description': {
                                             'en': 'Citizen Identification Code',
                                             'vn': 'Mã căn cước công dân'
                                         }})
    address = Column(String(length=STRING_LENGTH),
                     info={'description': {
                         'en': 'Address',
                         'vn': 'Địa chỉ'
                     }})
    skill = Column(String(length=STRING_LENGTH),
                   info={'description': {
                       'en': 'Skill',
                       'vn': 'Kỹ năng'
                   }})
    academic_level = Column(String(length=STRING_LENGTH),
                            info={'description': {
                                'en': 'Academic Level',
                                'vn': 'Trình độ học vấn'
                            }})
    experience = Column(String(length=STRING_LENGTH),
                        info={'description': {
                            'en': 'Experience',
                            'vn': 'Kinh nghiệm làm việc'
                        }})
    degree = Column(String(length=STRING_LENGTH),
                    info={'description': {
                        'en': 'Degree',
                        'vn': 'Bằng cấp'
                    }})
    # Other Candidate's columns here...

    # 1-n relationships
    
    application_forms = relationship(
        "ApplicationForm", back_populates="candidate")
    
    __mapper_args__ = {
        'polymorphic_identity': RoleStates.CANDIDATE.name,
        'polymorphic_load': 'inline'
    }


class Interviewer(User, ReprAble):
    info = {
        'description': {
            'en': 'Interviewer',
            'vi': 'Người phỏng vấn'
        },
        'permission':
        {
            # Permission at List page
            'create':
            [
                RoleStates.ADMIN.name
            ],
            'read':
            [
                RoleStates.ADMIN.name,
                RoleStates.JOB_MANAGER.name
            ],
            'update':
            [
                RoleStates.ADMIN.name
            ],
            'delete':
            [
                RoleStates.ADMIN.name
            ]
        }
    }
    __tablename__ = 'interviewers'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    # Other Interviewer's column here...

    # 1-n relationships
    interviewer_assignments = relationship(
        "InterviewerAssignment", back_populates="interviewer")

    def __repr__(self):
        return f'{self.__class__.__name__}({super().__repr__()})'

    __mapper_args__ = {
        'polymorphic_identity': RoleStates.INTERVIEWER.name,
        'polymorphic_load': 'inline'
    }


class JobManager(User, ReprAble):
    info = {
        'description': {
            'en': 'Job Manager',
            'vi': 'Người quản lý công việc'
        },
        'permission':
        {
            # Permission at List page
            'create':
            [
                RoleStates.ADMIN.name
            ],
            'read':
            [
                RoleStates.ADMIN.name
            ],
            'update':
            [
                RoleStates.ADMIN.name
            ],
            'delete':
            [
                RoleStates.ADMIN.name
            ]
        }
    }
    __tablename__ = 'job_managers'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    # Other Interviewer's column here...

    # 1-n relationships
    interviewer_assignments = relationship(
        "InterviewerAssignment", back_populates="job_manager")

    def __repr__(self):
        return f'{self.__class__.__name__}({super().__repr__()})'

    __mapper_args__ = {
        'polymorphic_identity': RoleStates.JOB_MANAGER.name,
        'polymorphic_load': 'inline'
    }


class JobStatus(Base, ReprAble):
    info = {
        'description': {
            'en': 'Job Status',
            'vi': 'Trạng thái công việc'
        },
        'permission':
        {
            # Permission at List page
            'create':
            [
                RoleStates.ADMIN.name
            ],
            'read':
            [
                RoleStates.ADMIN.name
            ],
            'update':
            [
                RoleStates.ADMIN.name
            ],
            'delete':
            [
                RoleStates.ADMIN.name
            ]
        }
    }
    __tablename__ = 'job_statuses'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=STRING_LENGTH), nullable=False, unique=True,
                  info={'description': {
                      'en': 'Job Status Name',
                      'vn': 'Tên trạng thái công việc'
                  }})

    # 1-n relationships
    jobs = relationship("Job", back_populates="job_status")


class Job(Base, ReprAble):
    info = {
        'description': {
            'en': 'Job',
            'vi': 'Công việc'
        },
        'permission':
        {
            # Permission at List page
            'create':
            [
                RoleStates.ADMIN.name,
                RoleStates.JOB_MANAGER.name
            ],
            'read':
            [
                RoleStates.ADMIN.name,
                RoleStates.JOB_MANAGER.name,
                RoleStates.INTERVIEWER.name,
                RoleStates.CANDIDATE.name
            ],
            'update':
            [
                RoleStates.ADMIN.name,
                RoleStates.JOB_MANAGER.name
            ],
            'delete':
            [
                RoleStates.ADMIN.name,
                RoleStates.JOB_MANAGER.name
            ]
        }
    }

    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=STRING_LENGTH), nullable=False, unique=True,
                  info={'description': {
                      'en': 'Job Name',
                      'vn': 'Tên công việc'
                  },
        'updateable':
        [
                      RoleStates.ADMIN.name,
                      RoleStates.JOB_MANAGER.name
                  ]})
    description = Column(String(length=STRING_LENGTH), nullable=False,
                         info={'description': {
                             'en': 'Job Description',
                             'vn': 'Mô tả công việc'
                         },
        'updateable':
        [
                             RoleStates.ADMIN.name,
                             RoleStates.JOB_MANAGER.name
                         ]})
    pay = Column(String(length=STRING_LENGTH), nullable=False,
                 info={'description': {
                     'en': 'Job Pay',
                     'vn': 'Mức lương công việc'
                 },
        'updateable':
        [
                     RoleStates.ADMIN.name,
                     RoleStates.JOB_MANAGER.name
                 ]})
    requirement = Column(String(length=STRING_LENGTH), nullable=False,
                         info={'description': {
                             'en': 'Job Requirement',
                             'vn': 'Yêu cầu công việc'
                         },
        'updateable':
        [
                             RoleStates.ADMIN.name,
                             RoleStates.JOB_MANAGER.name
                         ]})
    # 1-n relationships
    application_forms = relationship('ApplicationForm', back_populates='job')

    # n-1 relationships
    job_status_id = Column(Integer, ForeignKey(
        'job_statuses.id'), nullable=False,
        info={'description': {
            'en': 'Job Status',
            'vn': 'Trạng thái công việc'
        },
        'updateable':
        [
            RoleStates.ADMIN.name,
            RoleStates.JOB_MANAGER.name
        ]})
    job_status = relationship('JobStatus', back_populates='jobs')


class InterviewerAssignment(Base, ReprAble):
    info = {
        'description': {
            'en': 'Interviewer assignment',
            'vi': 'Giao phỏng vấn'
        },
        'permission':
        {
            # Permission at List page
            'create':
            [
                RoleStates.ADMIN.name,
                RoleStates.JOB_MANAGER.name
            ],
            'read':
            [
                RoleStates.ADMIN.name,
                RoleStates.JOB_MANAGER.name
            ],
            'update':
            [
                RoleStates.ADMIN.name,
                RoleStates.JOB_MANAGER.name
            ],
            'delete':
            [
                RoleStates.ADMIN.name,
                RoleStates.JOB_MANAGER.name
            ]
        }
    }
    __tablename__ = 'interviewer_assignments'
    id = Column(Integer, primary_key=True)
    interview_location = Column(String(length=STRING_LENGTH),
                                nullable=False,
                                info={'description': {
                                    'en': 'Interview Location',
                                    'vn': 'Địa điểm phỏng vấn'
                                },
        "updateable":
        [
                                    RoleStates.ADMIN.name,
                                    RoleStates.JOB_MANAGER.name,
                                ]})
    interview_datetime = Column(DateTime,
                                nullable=False,
                                info={'description': {
                                    'en': 'Interview Datetime',
                                    'vn': 'Thời điểm phỏng vấn'
                                },
                                    "updateable":
                                    [
                                    RoleStates.ADMIN.name,
                                    RoleStates.JOB_MANAGER.name,
                                ]})
    note = Column(String(length=STRING_LENGTH),
                  info={'description': {
                      'en': 'Interview Note',
                      'vn': 'Ghi chú phỏng vấn'
                  },
        "updateable":
        [
                      RoleStates.ADMIN.name,
                      RoleStates.JOB_MANAGER.name,
                  ]})
    # n-1 Relationships
    interviewer_id = Column(Integer, ForeignKey('interviewers.id'),
                            nullable=False,
                            info={'description': {
                                'en': 'Interviewer',
                                'vn': 'Nhân viên phỏng vấn'
                            },
        "updateable":
        [
                                RoleStates.ADMIN.name,
                                RoleStates.JOB_MANAGER.name,
                            ]})
    interviewer = relationship(
        "Interviewer", back_populates="interviewer_assignments")
    job_manager_id = Column(Integer, ForeignKey('job_managers.id'),
                            nullable=False,
                            info={'description': {
                                'en': 'Job Manager',
                                'vn': 'Người quản lý công việc'
                            },
        "updateable":
        [
                                RoleStates.ADMIN.name,
                                RoleStates.JOB_MANAGER.name,
                            ]})
    job_manager = relationship(
        "JobManager", back_populates="interviewer_assignments")
    application_form_id = Column(Integer, ForeignKey('application_forms.id'),
                          nullable=False,
                          info={'description': {
                              'en': 'Application form',
                            'vi': 'Đơn ứng tuyển'
                          },
        "updateable":
        [
                              RoleStates.ADMIN.name,
                              RoleStates.JOB_MANAGER.name,
                          ]})
    application_form = relationship(
        "ApplicationForm", back_populates="interviewer_assignments")


class ApplicationForm(Base, ReprAble):
    info = {
        'description': {
            'en': 'Application form',
            'vi': 'Đơn ứng tuyển'
        },
        'permission':
        {
            # Permission at List page
            'create':
            [
                RoleStates.ADMIN.name,
                # RoleStates.CANDIDATE.name
            ],
            'read':
            [
                RoleStates.ADMIN.name,
                RoleStates.JOB_MANAGER.name,
                RoleStates.CANDIDATE.name
            ],
            'update':
            [
                RoleStates.ADMIN.name,
                RoleStates.JOB_MANAGER.name,
                RoleStates.CANDIDATE.name
            ],
            'delete':
            [
                RoleStates.ADMIN.name,
                RoleStates.CANDIDATE.name
            ]
        }
    }
    __tablename__ = 'application_forms'
    id = Column(Integer, primary_key=True)
    cv = Column(LargeBinary,
                info={
                    'description':
                    {
                        'en': 'CV',
                        'vn': 'CV'
                    },
                    'filetype': FileTypes.PDF_FILE.value,
                    'updateable':
                    [
                        RoleStates.ADMIN.name,
                        RoleStates.CANDIDATE.name
                    ]
                })
    # 1-n relationship
    interviewer_assignments =  relationship(argument='InterviewerAssignment', back_populates='application_form')

    # n-1 relationships
    candidate_id = Column(Integer, ForeignKey('candidates.id'),
                          nullable=False,
                          info={'description': {
                              'en': 'Candidate',
                              'vn': 'Ứng viên'
                          },
        'hide':
        [
                              RoleStates.CANDIDATE.name
                          ]})
    candidate = relationship("Candidate", back_populates="application_forms")
    job_id = Column(Integer, ForeignKey('jobs.id'),
                    nullable=False,
                    info={'description': {
                        'en': 'Apply to job',
                              'vn': 'Vị trí ứng tuyển'
                    }})
    job = relationship("Job", back_populates="application_forms")

    # n-1 relationships
    application_form_status_id = Column(
        Integer, ForeignKey('application_form_statuses.id'),
        info={'description': {
            'en': 'Application form status',
            'vn': 'Trạng thái hồ sơ ứng tuyển'
        },
        'hide':
        [
            RoleStates.CANDIDATE.name
        ]})
    application_form_status = relationship(
        "ApplicationFormStatus", back_populates="application_forms")


class Gender(Base, ReprAble):
    info = {
        'description': {
            'en': 'Genders',
            'vi': 'Giới tính'
        },
        'permission':
        {
            # Permission at List page
            'create':
            [
                RoleStates.ADMIN.name
            ],
            'read':
            [
                RoleStates.ADMIN.name
            ],
            'update':
            [
                RoleStates.ADMIN.name
            ],
            'delete':
            [
                RoleStates.ADMIN.name
            ]
        }
    }
    __tablename__ = 'genders'
    id = Column(Integer, primary_key=True)
    name = Column(String(STRING_LENGTH),
                  nullable=False,
                  unique=True,
                  info={'description': {
                      'en': 'Gender name',
                      'vn': 'Giới tính'
                  }})

    # 1-n relationships
    users = relationship('User', back_populates='gender')

class ApplicationForm_Status(Enum):
    HIRED = "Hired"
    INTERVIEW_PENDING = "Interview pending"
    REJECT = "Reject"


class ApplicationFormStatus(Base, ReprAble):
    info = {
        'description': {
            'en': 'Appliction form statuses',
            'vi': 'Trạng thái hồ sơ ứng tuyển'
        },
        'permission':
        {
            # Permission at List page
            'create':
            [
                RoleStates.ADMIN.name
            ],
            'read':
            [
                RoleStates.ADMIN.name
            ],
            'update':
            [
                RoleStates.ADMIN.name
            ],
            'delete':
            [
                RoleStates.ADMIN.name
            ]
        }
    }
    __tablename__ = 'application_form_statuses'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=STRING_LENGTH),
                  unique=True,
                  nullable=False,
                  info={'description': {
                      'en': 'Appliction form status name',
                      'vn': 'Tên trạng thái hồ sơ ứng tuyển'
                  }})
    status = Column(String(length=STRING_LENGTH),
                    info={'description': {
                        'en': 'Appliction form status',
                        'vn': 'Trạng thái hồ sơ ứng tuyển'
                    }})

    # 1-n relationships
    application_forms = relationship(
        "ApplicationForm", back_populates="application_form_status")

def isPermissionToMe(model, my_role, operand: str):
    """ operand = create/read/update/delete """
    # Get the 'permission' dictionary, default to an empty dictionary if it doesn't exist
    permission_info = model.info.get('permission', {})

    # Get the 'operand' list from the 'permission' dictionary, default to an empty list if it doesn't exist
    read_permission_roles = permission_info.get(operand, [])

    # Check if my_role is in the 'operand' list
    is_allowed = my_role in read_permission_roles

    return is_allowed

def getModelDescription(model, language):
    return model.info.get('description', {}).get(language, '')

def getColumnFileType(column):
    return column.info.get('filetype', None)

def getColumnHideToRoles(column):
    return column.info.get('hide', [])

def isThisColumnHideToMe(column, my_role):
    hide_to_roles = getColumnHideToRoles(column=column)
    is_hide = my_role in hide_to_roles
    return is_hide

def getColumnUpdateableToRoles(column):
    return column.info.get('updateable', [])

def isUpdateableToMe(column, my_role):
    updateable_to_roles = getColumnUpdateableToRoles(column=column)
    is_updateable = my_role in updateable_to_roles
    return is_updateable

def getColumnTranslation(column, language):
    return column.info.get('description', {}).get(language, column.name)


all_models = [obj for obj in globals().values() if isinstance(
    obj, type) and issubclass(obj, Base) and obj != Base]
