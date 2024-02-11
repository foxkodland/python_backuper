import shutil
import os
from datetime import datetime
from textwrap import dedent


BACKUP_FOLDER = r"C:\Users\kodland\Desktop\src"
DESTINATION_FOLDER = r"C:\Users\kodland\Desktop\backups"
FILE_TO_LOGS = 'backup-logs.txt'



def logs(datetime: str, destination_folder: str, backup_folder: str, flag_succes: bool):
    if flag_succes:
        status = "Бэкап успешно создан"
    else:
        status = 'Ошибка создания бекапа'

    msg = dedent(f'''
        {datetime} -------- Начался бэкап
        From {destination_folder}
        To: {backup_folder}
        {status}
    ''')

    with open(FILE_TO_LOGS, 'a', encoding='utf-8') as file:
        file.write(msg)



def delete_old_backups(folder_day: str, count: int):
    # удалить старые бэкапы, если нужно ограничение на 1 день
    spisok_folders = os.listdir(DESTINATION_FOLDER + '/' + folder_day)
    while len(spisok_folders) >= count:
        shutil.rmtree(DESTINATION_FOLDER + "/" + folder_day + '/' + spisok_folders[0])
        spisok_folders.pop(0)


def backup(src: str, dst: str) -> bool:
    '''
        return:
            bool - статус копирования файлов (True - успех, False - неудача)
    '''
    try:
        shutil.copytree(src, dst, symlinks=False, ignore=None)
        copy_success = True
    except:
        copy_success = False

    return copy_success



def main():
    # для каждого дня своя папка с датой
    # --> для каждого бекапа своя папка со временем
    datetime_now = datetime.now()
    folder_day = f'backup_{datetime_now.date()}'  # backup_2024-02-11
    folder_time = f'backup_from_{datetime_now.time().strftime(f"%H-%M-%S")}' # time_19-14-27 

    # ограничение на кол-во хранящихся бэкапов за день. прошлые удалить
    delete_old_backups(folder_day, 3)

    # копирование
    destination_path = f'{DESTINATION_FOLDER}/{folder_day}/{folder_time}'
    status = backup(BACKUP_FOLDER, destination_path)

    # logs
    logs(datetime_now, BACKUP_FOLDER, destination_path, status)



if __name__ == '__main__':
    main()