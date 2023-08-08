from src.parser import ConfigParser


def config(filename='src/database.ini', section='postgresql') -> dict:
    '''
    Функция для получения параметров вбазы данных в виде словаря
    из определённой секции .ini файла
    :param filename: Путь к файлу параметров базы данных
    :param section: Название секции внутри .ini файла
    :return: Словарь с параметрами
    '''
    parser = ConfigParser()
    parser.read(filename)
    db_params = {}
    if parser.has_section(section):
        params = parser.get_item(section)
        for param in params:
            db_params[param[0]] = param[1]
    else:
        raise Exception(
            'Section {0} is not found in the {1} file.'.format(section, filename))
    return db_params
