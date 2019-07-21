import zipfile
import os
import re


while True:
    choice_input = input('Желаете поработать с архивами? Y/N ')
    choice = choice_input.lower()
    if choice == 'y':
        root_zip = input('Введите путь места расположения исходного каталога ')
        if os.path.exists(root_zip):
            path_zip = input('Введите путь для распакованных файлов основного архива ')
            archives = os.listdir(root_zip)
            for arch in archives:
                with zipfile.ZipFile(os.path.join(root_zip, arch), 'r') as zip_file:
                    zip_file.extractall(path_zip)
            archives2 = os.listdir(path_zip)
            for file in archives2:
                if zipfile.is_zipfile(os.path.join(path_zip, file)):
                    with zipfile.ZipFile(os.path.join(path_zip, file), 'r') as zip_file2:
                        zip_file2.extractall(os.path.join(path_zip, 'results'))
            print('Распаковка файлов завершена')

            path_xml = os.path.join(path_zip, 'results')
            xmls = os.listdir(path_xml)
            for file in xmls:
                if os.path.isfile(os.path.join(path_xml, file)):
                    with open(os.path.join(path_xml, file), 'r', encoding='utf-8') as xml:
                        xml_str = xml.read()
                        name = re.search(r'(<Parcel CadastralNumber=)"([0-9:]+)"', xml_str)
                        name_final = name.group(2)
                        name_final_correct = re.sub(':', '_', name_final)
                    os.chdir(path_xml)
                    os.rename(file, f'{name_final_correct}.xml')
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
