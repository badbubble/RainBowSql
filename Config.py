class Config(object):
    def __init__(self):
        pass

    @staticmethod
    def get_config():
        config = {
            'user_info_path': 'userinfo/userinfo.rb',
            'db_path': 'database/'

        }
        return config
