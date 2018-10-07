import List_host
import paramiko
import zipfile
import os
host = List_host.key_conclusion_list_host()
user = 'pi'
secret = List_host.password_conclusion_list_host()
port = 22

class Document:
    """
    fun_inf_user_host:
            - infomathion_etc_passw - функция показывает пользователей из /etc/passwd на удаленной машине
            - useradd - добавить пользователя - запросит name_user, directory, password, id_in_user, id_in_group_user осттальные параметры предопределены в классе
            - zip_on_file - создать архив на удаленной машине в домашней директории пользователя, запросит путь к файлам которые необходимо архивировать
    """
print(Document.__doc__)

fun_inf_user_host = str(input())

def infomathion_etc_passw():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())             # добавляем ключ сервера в список известных хостов — файл .ssh/known_hosts
    client.connect(hostname=host, username=user, password=secret, port=port)
    template_sed = "sed {} /etc/passwd"
    templ = template_sed.format('\'s/:.*//\'')    # sed 's/:.*//' /etc/passwd
    stdin, stdout, stderr = client.exec_command(templ)
    data = stdout.read() + stderr.read()
    client.close()
    print('Existing users:' + '\n', '\n', data.decode("utf-8"))

class UserAdd:
    def __init__(self):
        self.sheath = '/bin/bash'
        self.group_acess = 'adm,cdrom,wheel'
    def teml_add_us(self, name, directory, pas, user_id, us_group_id):
        tepplate = "sudo useradd -d {} -p {} -u {} -g {} -s {} -G {} {}"    # sudo useradd -d /home/user -p 1234 -u 503 -g 500 -s /bin/bash -G adm,cdrom,wheel user
        comm = tepplate.format(directory, pas, user_id, us_group_id, self.sheath, self.group_acess, name)
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(hostname=host, username=user, password=secret, port=port)
        stdin, stdout, stderr = client.exec_command(comm)
        if stderr:
            dataerr = stderr.read().decode("utf-8")
            print(dataerr)
        if stdout:
            x = stdout.read().decode("utf-8")
            with open('input_UserAdd.txt', 'w+') as f:
                f.write(x)
        client.close()

def zip_on_file(pat_file):        #  /home/pi/python_games
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())             # добавляем ключ сервера в список известных хостов — файл .ssh/known_hosts
    client.connect(hostname=host, username=user, password=secret, port=port)
    ftp = client.open_sftp()
    ftp.chdir(pat_file)                                # chdir - переход в директорию
    print('текущая директория', ftp.getcwd())          # выведет путь к текущей директории /home/pi/python_games
    stdin, stdout, stderr = client.exec_command('tar -zcvf paramic_archive.tar.gz' + ' ' + ftp.getcwd())        # Архив будет сохранен в домашней директории
    global status, x
    if stdout:
        print('Создание архива:')
        with open('file_tar_paramic_archive.txt', 'w') as ikt:
            ikt.write(stdout.read().decode("utf-8"))
        status = True                           # без ошибок
        x = 'complited'                         # собрался
    if stderr:
        with open('error_file_tar_paramic_archive.txt', 'w') as inf:
            inf.write(stderr.read().decode("utf-8"))
        status = False                          # есть ошибки
    print(x)
    print(status)
    client.close()

if fun_inf_user_host == 'infomathion_etc_passw':
    infomathion_etc_passw()
elif fun_inf_user_host == 'useradd':
    print("input: name_user, directory, password, id_in_user, id_in_group_user")
    noneme, dorect0ry, pacc, useriod, us_groupe_id = map(str, input().split())  # user /home/user 1234 503 500
    call_UserAdd = UserAdd()
    call_UserAdd.teml_add_us(noneme, dorect0ry, pacc, useriod, us_groupe_id)
elif fun_inf_user_host == 'create_zip_file':
    print("Input file path in remote machine:")
    zip_on_file(str(input()))  # на расберри /home/pi/python_games


