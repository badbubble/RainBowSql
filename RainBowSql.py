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
        self.__current_db = ''
        self.__current_table = ''
        self.__version = 'v1.0'
        self._welcome()
        self.config = Config.get_config()
        self.check_environment()


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
                                                            
type help to get help                                                            {}        By:{}
        
        """.format(self.__version, self.__db_author))

    def help(self):
        print("""
        command:
                login: To login RainBowSql.
                signup: To Create an account.
                exit | quit: Exit RainBowSql.
                
        """)

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

    def login(self):
        """
        用户登陆
        :return: None
        """
        if os.path.exists(self.config['user_info_path']):
            user_info = joblib.load(self.config['user_info_path'])
        else:
            print("[!] No user, Please signup!")
            self.signup()
            print("[-] Please Login!")
            user_info = joblib.load(self.config['user_info_path'])

        username = input("[>] Please Enter Username: ")
        password = input("[>] Please Enter Password: ")
        if user_info.get(username, None) == self.password_to_md5(password):
            print("[+] Welcom {}!".format(username))
            self.__current_user = username
        else:
            print("[!] User does not exist or wrong password!")


    def check_environment(self):
        if not os.path.exists('userinfo'):
            os.makedirs("userinfo")
        if not os.path.exists('database'):
            os.makedirs('database')

    def get_command(self):
        command = input("[>]") if not self.__current_db else input("[{} > ]".format(self.__current_db))
        command = command.lower()
        return command

    def run(self):
        while(True):
            command = self.get_command()
            if command == 'login':
                self.login()
            elif command == 'signup':
                self.signup()
            elif command == 'quit' or command == 'exit':
                print("[:)] Thanks for using RainBowSql. Bye~~")
                exit(0)
            elif command == 'help':
                self.help()





if __name__ == '__main__':
    db = RainBowSql()
    #db.login()
    db.run()
