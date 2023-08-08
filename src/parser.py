from abc import ABC, abstractmethod


class Parser(ABC):

    def read(self, path):
        pass

    def has_section(self, section):
        pass

    def get_item(self, section):
        pass


class ConfigParser(Parser):

    def __init__(self):
        self.config = {}

    def read(self, path='src/database.ini'):
        with open(path, 'r') as config_file:
            config_data = config_file.read().split('[')
        if not config_data[0]:
            del config_data[0]
        config = {}
        for config_section in config_data:
            name, params = config_section.split(']\n')
            params_list = params.split('\n')
            config[name] = []
            for param in params_list:
                if param:
                    param_key, param_value = param.split('=')
                    config[name].append((param_key, param_value))
        self.config = config

    def has_section(self, section):
        return section in self.config

    def get_item(self, section):
        if self.has_section(section):
            return self.config[section]
        else:
            raise KeyError(f'No section {section} in config file')


class QueryParser(Parser):

    def __init__(self):
        self.queries = {}

    def read(self, path='src/queries.sql'):
        with open(path, 'r', encoding='utf-8') as sql_file:
            queries_raw = sql_file.read()
        queries_list = queries_raw.split(';')
        queries = {}
        for query_raw in queries_list:
            if query_raw:
                query_and_comment = query_raw.strip().split('\n')
                comment = query_and_comment[0]
                query = '\n'.join(query_and_comment[1:]).strip()
                assert comment.startswith('--', 0, 2), f'Wrong query format near {query_raw}'
                name = comment[2:]
                queries[name] = query
        self.queries = queries

    def has_section(self, section):
        return section in self.queries

    def get_item(self, section):
        if self.has_section(section):
            return self.queries[section]
        else:
            raise KeyError('No such query in file')
