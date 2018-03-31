import re
import json
import os
import time
from Config import Config
import joblib
import hashlib


class RainBowSql(object):
    def __init__(self):
        self.__db_author = 'liuhanjun'
        self.__current_user = ''
        self.__db_path = ''
        self.__current_db = ''
        self.__current_table = ''
        self.__version = 'v1.0'
        self._welcome()
        self.config = Config.get_config()

    def _welcome(self):
        """
        显示欢迎界面
        :return: None
        """
        print("""
 _______  _______ _________ _        ______   _______           _______  _______  _       
(  ____ )(  ___  )\__   __/( (    /|(  ___ \ (  ___  )|\     /|(  ____ \(  ___  )( \      
| (    )|| (   ) |   ) (   |  \  ( || (   ) )| (   ) || )   ( || (    \/| (   ) || (      
| (____)|| (___) |   | |   |   \ | || (__/ / | |   | || | _ | || (_____ | |   | || |      
|     __)|  ___  |   | |   | (\ \) ||  __ (  | |   | || |( )| |(_____  )| |   | || |      
| (\ (   | (   ) |   | |   | | \   || (  \ \ | |   | || || || |      ) || | /\| || |      
| ) \ \__| )   ( |___) (___| )  \  || )___) )| (___) || () () |/\____) || (_\ \ || (____/\\
|/   \__/|/     \|\_______/|/    )_)|/ \___/ (_______)(_______)\_______)(____\/_)(_______/
                                                            
                                                            {}        By:{}
        
        """.format(self.__version, self.__db_author))

    def password_to_md5(self, password):
        """
        将密码转换成md5
        :param password: 明文密码
        :return: 加密后的密码
        """
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        return md5.hexdigest()



    def signup(self):
        """
        注册账号
        :return: None
        """

        if os.path.exists(self.config['user_info_path']):
            user_info = joblib.load(self.config['user_info_path'])
        else:
            user_info = dict()

        username = input("[>] Please Enter Username: ")
        password = input("[>] Please Enter Password: ")
        name_exists = user_info.get(username, None)
        if name_exists == None:
            user_info[username] = self.password_to_md5(password)
            print("[+] Signup Success!")
            joblib.dump(user_info, self.config['user_info_path'])
        else:
            print("[!] Sorry username existed, please try again!!!")




if __name__ == '__main__':
    db = RainBowSql()
    db.signup()
