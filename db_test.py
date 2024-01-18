from Backend.Services.db_test import *


if __name__ == "__main__":
    printAllUsers()
    status, result = CRUD_User.login(username='admin1', password='admin')
    print(status)
    print(result)