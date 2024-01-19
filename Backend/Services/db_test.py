from Backend.Database.sessions import *


def initTestDatabase():
    CRUD_Gender.create(name="Male")
    CRUD_Gender.create(name="Female")
    CRUD_JobStatus.create(name="Hiring")
    CRUD_JobStatus.create(name="Not available")
    CRUD_JobStatus.create(name="Closed")
    for i in range(1, 6):
        status, result = CRUD_Admin.create(username=f"admin{i}",
                                           password="admin",
                                           email=f"admin{i}@gmail.com",
                                           birthday=datetime(2001, i, i),
                                           # admin_col=f"Test admin {i}",
                                           name=f"Admin Number {i}",
                                           gender_id=1)
        print(status)
        print(result)

        status, result = CRUD_Candidate.create(username=f"candidate{i}",
                                               password="candidate",
                                               email=f"candidate{i}@gmail.com",
                                               birthday=datetime(2001, i, i),
                                               # candidate_col=f"Test candidate {i}",
                                               name=f"Candidate Number {i}",
                                               gender_id=1,
                                               citizen_identification_code=f'xxx{i}',
                                               address=f"{i} Street",
                                               skill=f"Skill number {i}",
                                               academic_level=f"academic level {i}",
                                               experience=f"Test {i}",
                                               degree=f"Good {i}")
        print(status)
        print(result)

        status, result = CRUD_Interviewer.create(username=f"interviewer{i}",
                                                 password="interviewer",
                                                 email=f"interviewer{i}@gmail.com",
                                                 birthday=datetime(2001, i, i),
                                                 # interviewer_col=f"Test interviewer {i}",
                                                 name=f"Interviewer Number {i}",
                                                 gender_id=2)
        print(status)
        print(result)

        status, result = CRUD_JobManager.create(username=f"job_manager{i}",
                                                password="job_manager",
                                                email=f"job_manager{i}@gmail.com",
                                                birthday=datetime(2001, i, i),
                                                # job_manager_col=f"Test job_manager {i}",
                                                name=f"Job Manager Number {i}",
                                                gender_id=2)
        print(status)
        print(result)

        status, result = CRUD_Job.create(name=f"Job {i}",
                                         description=f"This is job {i}'s description...",
                                         pay=f"{i}.000.000.000 $ / Year",
                                         requirement=f"Required: Must have {i}",
                                         job_status_id= i % 3 + 1)


def printAllUsers():
    status, result = CRUD_User.read_all()
    print(status)
    for user in result:
        print(user)
