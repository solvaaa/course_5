class ConfigParser:

    def __init__(self):
        self.config = {}

    def read(self, path):
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

    def items(self, section):
        return self.config[section]


