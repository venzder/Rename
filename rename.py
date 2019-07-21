import zipfile
import os
import re
import shutil


def unzip(path_in, path_out):
    archives = os.listdir(path_in)
    for arch in archives:
        if zipfile.is_zipfile(os.path.join(path_in, arch)):
            with zipfile.ZipFile(os.path.join(path_in, arch), 'r') as zip_file:
                zip_file.extractall(path_out)


def check(dir_temp, dir_result):
    lst_dir_temp = os.listdir(dir_temp)
    lst_dir_result = os.listdir(dir_result)
    for obj in lst_dir_temp:
        if obj not in lst_dir_result:
            shutil.copy(os.path.join(dir_temp, obj), dir_result)


def rename(path_rename):
    xmls = os.listdir(path_rename)
    for file in xmls:
        if os.path.isfile(os.path.join(path_rename, file)):
            with open(os.path.join(path_rename, file), 'r', encoding='utf-8') as xml:
                xml_str = xml.read()
                name = re.search(r'(<Parcel CadastralNumber=)"([0-9:]+)"', xml_str)
                name_final = name.group(2)
                name_final_correct = re.sub(':', '_', name_final)
            os.chdir(path_rename)
            os.rename(file, f'{name_final_correct}.xml')


while True:
    choice_input = input('Желаете поработать с архивами? Y/N ')
    choice = choice_input.lower()
    if choice == 'y':
        root_zip = input('Введите путь места расположения исходного каталога ')
        if os.path.exists(root_zip):
            path_zip = input('Введите путь для распакованных файлов основного архива ')
            path_temp = os.path.join(path_zip, 'temp')
            unzip(root_zip, path_zip)
            unzip(path_zip, path_temp)
            print('Распаковка файлов завершена')

            path_xml = os.path.join(path_zip, 'results')
            os.mkdir(path_xml)
            rename(path_temp)
            check(path_temp, path_xml)

            files = os.listdir(path_zip)
            for file in files:
                if os.path.isdir(os.path.join(path_zip, file)):
                    pass
                else:
                    os.remove(os.path.join(path_zip, file))
            print('Временные файлы удалены')

            print('Переименование исходных данных выполнена')
        else:
            print('Вы неправильно указали исходную дирректорию')
    elif choice == 'n':
        break
    else:
        print('Вы ввели недопустимый символ. Попробуйте еще раз')
