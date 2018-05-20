import re
import json
import os
import time
from Config import Config
import joblib
import hashlib
from functools import wraps
import pandas as pd


class RainBowSql(object):
    def __init__(self):
        self.__info = 'MIT License'
        self.__copyright = 'Copyright (c) 2018 Hanjun Liu'
        self.__github = 'https://github.com/ETCartman/RainBowSql'
        self.__current_user = 'admin'
        self.__user_right = 0
        self.__current_db = ''
        self.__current_db_name = ''
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
###################################################################################################

                Available In Github: https://github.com/ETCartman/RainBowSql
 _______  _______ _________ _        ______   _______           _______  _______  _       
(  ____ )(  ___  )\__   __/( (    /|(  ___ \ (  ___  )|\     /|(  ____ \(  ___  )( \      
| (    )|| (   ) |   ) (   |  \  ( || (   ) )| (   ) || )   ( || (    \/| (   ) || (      
| (____)|| (___) |   | |   |   \ | || (__/ / | |   | || | _ | || (_____ | |   | || |      
|     __)|  ___  |   | |   | (\ \) ||  __ (  | |   | || |( )| |(_____  )| |   | || |      
| (\ (   | (   ) |   | |   | | \   || (  \ \ | |   | || || || |      ) || | /\| || |      
| ) \ \__| )   ( |___) (___| )  \  || )___) )| (___) || () () |/\____) || (_\ \ || (____/\\
|/   \__/|/     \|\_______/|/    )_)|/ \___/ (_______)(_______)\_______)(____\/_)(_______/
                                                            
                           ---> type help to get help <---        {}        License:{}
                                                                            {}
                                                                            
###################################################################################################
        
        """.format(self.__version, self.__info, self.__copyright))

    @staticmethod
    def help():
        print("""
        command:
                login: To login RainBowSql.
                signup: To Create an account.
                logout: To logout.
                exit | quit: Exit RainBowSql.
        sql:
            database:
                    show database: show all database.
                    create database <...>: create a database named <...>
                    use database <...>: use a database named <...>
                    drop database <...>: drop a database name <...>
                
        """)

    @staticmethod
    def password_to_md5(password):
        """
        将密码转换成md5
        :param password: 明文密码
        :return: 加密后的密码
        """
        md5 = hashlib.md5()
        md5.update(password.encode('utf-8'))
        return md5.hexdigest()

    @staticmethod
    def login_require(func):
        """
        检测是否登陆
        :param func: 需要登陆才能运行的函数
        :return:
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            if args[0].__current_user == "" and args[0].__user_right == "":
                print("[!] You need login first!")
            elif args[0].__user_right > 1:
                print("[!] Your account have no access to do anything!")
            else:
                return func(*args, **kwargs)

        return wrapper

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
        if name_exists is None:
            user_info[username] = {'password': self.password_to_md5(password),
                                   'user_right': 2,
                                   }
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
        if user_info.get(username, None) and \
                user_info[username].get("password", None) == self.password_to_md5(password):
            print("[+] Welcom {}!".format(username))
            self.__current_user = username
            self.__user_right = user_info[username].get("user_right", "")
        else:
            print("[!] User does not exist or wrong password!")

    def change_user_right(self, user):
        if self.__user_right != 0:
            print("[!] You have no access to change user right!")
            return
        if user == 'admin':
            print("[!] Your are admin!")
        user_info = joblib.load(self.config['user_info_path'])
        if user_info.get(user, None):
            user_info[user]['user_right'] = 1
            joblib.dump(user_info, self.config['user_info_path'])
            print("[+] Change Success!")
        else:
            print("[!] User does not exist!")

    def logout(self):
        """
        登出
        :return:None
        """
        self.__current_user = ''
        self.__user_right = ''
        print("[+] Logout!")

    def check_environment(self):
        """
        检查所需目录是否存在,若不存在就创建缺失目录
        :return: None
        """
        if not os.path.exists('userinfo'):
            os.mkdir('userinfo')
            admin_user = {
                'admin': {"password": self.password_to_md5("admin888"), 'user_right': 0},
            }
            joblib.dump(admin_user, self.config['user_info_path'])
        if not os.path.exists('database'):
            os.makedirs('database')

    def create_database(self, dbname):
        """
        创建数据库
        :param dbname: 数据库名称
        :return: None
        """
        dbname_path = self.config['db_path'] + dbname
        print(dbname_path)
        if dbname in os.listdir(self.config['db_path']):
            print("[!] DataBase exixts!")
        else:
            database = {
                'name': dbname,
                'master': [self.__current_user, 'admin'],
                'tables': {},
                'table_name': [],
                }
            joblib.dump(database, dbname_path)
            print("[+] DataBase created!")

    def use_database(self, dbname):
        """
        选择已存在的数据库
        :param dbname: 数据库名称
        :return: None
        """
        if dbname not in os.listdir(self.config['db_path']):
            print("[!] Can not find DataBase!")
        else:
            db = joblib.load(self.config['db_path'] + '/' +dbname)
            if self.__current_user not in db['master']:
                print('[!] You have no access to this database!')
                return
            print("[+] Using database {}".format(dbname))
            self.__current_db = db
            self.__current_db_name = dbname

    def drop_database(self, dbname):
        """
        删除database
        :param dbname:要删除的数据库名称
        :return: None
        """
        dbname_path = self.config['db_path'] + dbname
        if dbname not in os.listdir(self.config['db_path']):
            print("[!] Can not find DataBase!")
        else:
            os.remove(dbname_path)
            if self.__current_db_name == dbname:
                self.__current_db_name = ''
            print("[+] Database {} is droped!".format(dbname))

    def show_database(self):
        print("[+] All Databases:")
        for db in os.listdir(self.config['db_path']):
            print("\t[-] {}".format(db))

    def create_table(self, table_name, cols):
        # if len(table_name) != len():
        #     print("[!] Names should be equal!")
        #     return
        if self.__current_db_name == '':
            print("[!] You need to use database!")
            return
        if table_name in self.__current_db.get('table_name'):
            print("[!] Table exist!")
            return
        table = pd.DataFrame(columns=cols)
        self.__current_db['tables'][table_name] = table
        self.__current_db['table_name'].append(table_name)
        print("[+] Table {} created!".format(table_name))
        self.save_db()

    def show_tables(self):
        if self.__current_db_name == '':
            print("[!] You need to use database!")
            return
        for i in self.__current_db['table_name']:
            print("\t[-] {}".format(i))

    def drop_table(self, table_name):
        if self.__current_db_name == '':
            print("[!] You need to use database!")
            return
        if table_name not in self.__current_db['table_name']:
            print("[!] Table is not exist!")
            return
        del self.__current_db['tables'][table_name]
        self.__current_db['table_name'].remove(table_name)
        print("[+] Table dropped!")
        self.save_db()

    def insert(self, table_name, data):
        if self.__current_db_name == '':
            print("[!] You need to use database!")
            return
        if table_name not in self.__current_db['table_name']:
            print("[!] Table is not exist!")
            return
        table = self.__current_db['tables'][table_name]
        if len(table.columns) != len(data):
            print("[!] Data error!")
            return
        index = len(table)
        table.loc[index] = dict(zip(table.columns, data))
        print("[+] Data Inserted!")
        self.save_db()

    def select(self, cols, table_name):
        if self.__current_db_name == '':
            print("[!] You need to use database!")
            return
        if table_name not in self.__current_db['table_name']:
            print("[!] Table is not exist!")
            return
        table = self.__current_db['tables'][table_name]
        if cols[0] == '*':
            print(table)
            return

        print("#" * 20)
        print(table[cols])
        print("#" * 20)

    def save_db(self):
        joblib.dump(self.__current_db, self.config['db_path'] + self.__current_db_name)

    def get_command(self):
        """
        从控制台获取命令
        :return: None
        """
        command = input("[>]") if not self.__current_db_name else input("[{} > ]".format(self.__current_db_name))
        command = command.lower()
        return command

    @login_require.__get__(object, None)
    def query(self, sql):
        """
        执行sql语句
        :param sql:sql语句
        :return: None
        """
        sql_words = sql.lower().split(" ")
        if len(sql_words) < 2:
            print("[!] Wrong query!")
            return
        operate = sql_words[0]
        if operate == 'use':
            if sql_words[1] == 'database':
                try:
                    self.use_database(sql_words[2])
                except:
                    print("[!] Wrong query!")

        if operate == 'create':
            if sql_words[1] == 'database':
                try:
                    self.create_database(sql_words[2])
                except:
                    print("[!] Wrong query!")
            if sql_words[1] == 'table':
                self.create_table(sql_words[2], sql_words[3:])

        if operate == 'insert':
            try:
                self.insert(sql_words[1], sql_words[2:])
            except:
                print("[!] Inser error")

        if operate == 'drop':
            if sql_words[1] == 'database':
                try:
                    self.drop_database(sql_words[2])
                except:
                    print("[!] Wrong query!")
            if sql_words[1] == 'table':
                try:
                    self.drop_table(sql_words[2])
                except:
                    print("[!] Wrong query!")

        if operate == 'show':
            if sql_words[1] == 'databases':
                try:
                    self.show_database()
                except:
                    print("[!] Wrong query!")

            if sql_words[1] == 'tables':
                try:
                    self.show_tables()
                except:
                    print("[!] Wrong query!")

        if operate == 'change':
            try:
                self.change_user_right(sql_words[1])
            except:
                print("[!] Wrong query!")

        if operate == 'select':
            try:
                self.select(sql_words[1:-2], sql_words[-1])
            except:
                print("[!] select error!")

    def run(self):
        """
        运行DBMS
        :return: None
        """
        while True:
            command = self.get_command()
            if command == 'login':
                self.login()
            elif command == 'signup':
                self.signup()
            elif command == 'logout':
                self.logout()
            elif command == 'quit' or command == 'exit':
                print("[:)] Thanks for using RainBowSql. Bye~~")
                exit(0)
            elif command == 'help':
                self.help()

            else:
                self.query(command)


if __name__ == '__main__':
    db = RainBowSql()
    db.run()
