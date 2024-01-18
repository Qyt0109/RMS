# Hệ thống tuyển dụng
#### Cài đặt project
##### Bước 1: Clone project về từ Github
Yêu cầu:
- git

Sau khi clone, project sẽ nằm tại đường dẫn hiện tại của cửa sổ terminal vậy nên hãy cd tới đường dẫn chứa folder muốn chứa project trước khi clone về.
```
cd ./Đường/Dẫn/Tới/Thư/Mục/Chứa
```
Chạy lệnh sau trên terminal
```
git clone https://github.com/Qyt0109/RMS.git
```

#### Chạy project
##### Bước 1: Tạo môi trường ảo
Tạo môi trường ảo (virtual environment) python để cài đặt các thư viện (modules) trên đó, phục vụ cho việc chạy project.
Yêu cầu:
- python (3.11)
- pip
- venv

Cài đặt môi trường ảo trên Macos/Linux:
``` bash
python<Phiên bản(nếu cần)> -m venv <Tên môi trường ảo>
```
VD cài đặt môi trường ảo python 3.11 có tên .VenvMacos:
``` bash
python3.11 -m venv .VenvMacos
```
Sau đó active môi trường lên:
```
source <Tên môi trường ảo>/bin/active
```
VD:
```
source .VenvMacos/bin/active
```

Bước 2: Cài đặt các gói thư viện cần thiết:
Chạy lệnh sau trên terminal:
``` bash
pip install -r requirements.txt
```
Bước 3: Chạy project:
``` bash
python .
```

#### Một số thứ lưu ý:
##### Mật khẩu truy cập database sẽ nằm trong file ./Backend/password.py
File này sẽ không được đính kèm khi clone project về từ trên github vậy nên sẽ cần tự tạo và vứt mật khẩu (được cung cấp) vào đây.
VD file password.py với mật khẩu AbC123:
``` python
db_password = 'AbC123'
```

##### Tài khoản sample cho các quyền của người dùng để đăng nhập trong hệ thống:
<table>
    <tr>
        <th>
        </th>
        <th>
            JobManager
        </th>
        <th>
            Interviewer
        </th>
        <th>
            Contestant
        </th>
    </tr>
    <tr>
        <th>
            Username
        </th>
        <th>
            jobmanager1 - 5
        </th>
        <th>
            interviewer1 - 5
        </th>
        <th>
            contestant1 - 5
        </th>
    </tr>
    <tr>
        <th>
            Password
        </th>
        <th>
            jobmanager
        </th>
        <th>
            interviewer
        </th>
        <th>
            contestant
        </th>
    </tr>
</table>