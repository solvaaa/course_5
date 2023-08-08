class ConfigParser:

    def __init__(self):
        pass

    def read(self, path):
        with open(path, 'r') as config_file:
            config_data = config_file.read().split('[')
        if not config_data[0]:
            del config_data[0]
        config = {}
        assert len(config_data) > 0
        for config_section in config_data:
            name, params = config_section.split(']\n')
            params_list = params.split('\n')
            config[name] = {}
            for param in params_list:
                if param:
                    param_key, param_value = param.split('=')
                    config[name][param_key] = param_value
        self.config = config


cp = ConfigParser()
res = cp.read('database.ini')


