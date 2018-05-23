import re
import json
import os
import time
from Config import Config
import joblib
import hashlib
from functools import wraps
import pandas as pd
from utils import *


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

    @staticmethod
    def db_require(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if args[0].__current_db == "":
                print("[!] You need to use database!")
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
                'table_cols': {},
                'index': {},
                'views': {},
                'right': {
                    'select': [],
                    'delete': [],
                    'insert': [],
                    'update': [],
                }
            }
            joblib.dump(database, dbname_path)
            print("[+] DataBase created!")

    def check_right(self, command):
        if self.__current_user not in self.__current_db['right'][command] or \
                self.__current_user not in self.__current_db['master']:
            print("[!] You have no right to {}".format(command))
            return False
        return True

    def use_database(self, dbname):
        """
        选择已存在的数据库
        :param dbname: 数据库名称
        :return: None
        """
        if dbname not in os.listdir(self.config['db_path']):
            print("[!] Can not find DataBase!")
        else:
            db = joblib.load(self.config['db_path'] + '/' + dbname)
            # if self.__current_user not in db['master']:
            #     print('[!] You have no access to this database!')
            #     return
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
        if not self.is_use_database():
            return
        if table_name in self.__current_db.get('table_name'):
            print("[!] Table exist!")
            return
        cols_info = {}
        col_names = []
        for i in cols:
            col_name, dtype, prime_key, for_key, not_none = i.split(':')
            cols_info[col_name] = {
                'type': dtype,
                'prim_key': True if prime_key == '1' else False,
                'for_key': True if for_key == '1' else False,
                'not_none': True if not_none == '1' else False
            }
            col_names.append(col_name)
        table = pd.DataFrame(columns=col_names)
        self.__current_db['tables'][table_name] = table
        self.__current_db['table_name'].append(table_name)
        self.__current_db['table_cols'][table_name] = cols_info
        print("[+] Table {} created!".format(table_name))
        self.save_db()

    def show_tables(self):
        if not self.is_use_database():
            return
        for i in self.__current_db['table_name']:
            print("\t[-] {}".format(i))
            print("#" * 20)
            print("[-] {}".format(self.__current_db['tables'][i].info()))
            print("[-] {}".format(self.__current_db['table_cols'][i]))
            print("#" * 20)

    def drop_table(self, table_name):
        if not self.is_use_database():
            return
        if table_name not in self.__current_db['table_name']:
            print("[!] Table is not exist!")
            return
        del self.__current_db['tables'][table_name]
        self.__current_db['table_name'].remove(table_name)
        del self.__current_db['table_cols'][table_name]
        print("[+] Table dropped!")
        self.save_db()

    def insert(self, table_name, data):
        if not self.is_use_database():
            return
        if self.check_right('insert'):
            return

        if table_name not in self.__current_db['table_name']:
            print("[!] Table is not exist!")
            return
        table = self.__current_db['tables'][table_name]
        col_info = self.__current_db['table_cols'][table_name]
        if len(table.columns) != len(data):
            print("[!] Data error!")
            return
        index = len(table)
        hat_data = dict(zip(table.columns, data))
        for col, col_data in hat_data.items():
            if col_info[col]['prim_key']:
                if col_data in list(table[col]):
                    print("[!] Primary Key is exist!")
                    return
            if col_info[col]['for_key']:
                if col_data in list(table[col]):
                    print("[!] Foreign key is exist!")
                    return
            if col_info[col]['not_none']:
                if col_data == 'none':
                    print("[!] Data can not be None!")
                    return
        table.loc[index] = hat_data
        self.__current_db['tables'][table_name] = table
        print("[+] Data Inserted!")
        self.save_db()

    def select(self, cols, table_name):
        if self.__current_db_name == '':
            print("[!] You need to use database!")
            return
        if self.check_right('select'):
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

    def update(self, table_name, cols, condition=False):
        if not self.is_use_database():
            return
        if self.check_right('update'):
            return

        if table_name not in self.__current_db['table_name']:
            print("[!] Table is not exist!")
            return

    def delete(self, table_name, where_cond):
        if not self.is_use_database():
            return
        if self.check_right('delete'):
            return

        if table_name not in self.__current_db['table_name']:
            print("[!] Table is not exist!")
            return
        table = self.__current_db['tables'][table_name]

        where_cond = where_cond.split('=')
        table = table[table[where_cond[0]] != where_cond[1]]
        self.__current_db['tables'][table_name] = table
        print("[+] Info Deleted!")
        self.save_db()

    def get_view_data(self, sql):
        pass

    def create_view(self, name, sql):
        if not self.is_use_database():
            return
        if name in self.__current_db['views'].keys():
            print("[!] View is exist!")
            return
        self.__current_db['views'][name] = " ".join(sql)
        self.save_db()
        print("[+] View is created!")

    def show_views(self):
        if not self.is_use_database():
            return
        for name, content in self.__current_db['views'].items():
            print('\t[-] {0}-->{1}'.format(name, content))

    def create_index(self):
        if not self.is_use_database():
            return

    def save_db(self):
        joblib.dump(self.__current_db, self.config['db_path'] + self.__current_db_name)

    def is_use_database(self):
        if self.__current_db_name == '':
            print("[!] You need to use database!")
            return False
        else:
            return True

    def add_right(self, command, user_name):
        if not self.is_use_database():
            return
        if self.__current_user not in self.__current_db['master']:
            print("[!] You have no right!")
            return
        for i in command:
            self.__current_db['right'][i].append(user_name)
            print("[+] {} have access to use {}".format(user_name, i))
        self.save_db()

    def remove_right(self, command, user_name):
        if not self.is_use_database():
            return
        if self.__current_user not in self.__current_db['master']:
            print("[!] You have no right!")
            return
        for i in command:
            try:
                self.__current_db['right'][i].remove(user_name)
                print("[+] {} have no access to use {} now!".format(user_name, i))
            except:
                print("[!] No {}".format(user_name))
                return
        self.save_db()

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
        sql = sql.lower()
        sql_words = sql.split(" ")
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
                try:
                    self.create_table(sql_words[2], sql_words[3:])
                except:
                    print("[!] Error!")
            if sql_words[1] == 'view':
                try:
                    self.create_view(sql_words[2], sql_words[3:])
                except:
                    print("[!] Error!")

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

            if sql_words[1] == 'views':
                try:
                    self.show_views()
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

        if operate == 'update':
            table_name = sql_words[1]
            if 'where' in sql:
                condition = where_cond(sql.split("where")[-1])
                set_chr = r'set (.*?) where'
            else:
                condition = False
                set_chr = r'set (.*?)$'
            set_con = set_cond(sql, set_chr)
            print(condition)
            print(set_con)

        if operate == 'delete':
            table_name = sql_words[1]
            if 'where' not in sql_words:
                print("[!] No where condition!")
                return
            where_ = sql.split('where')[-1].strip()
            self.delete(table_name, where_)

        if operate == 'grant':
            if 'to' not in sql_words:
                print("[!] No to!")
                return
            try:
                self.add_right(sql_words[1:-2], sql_words[-1])
            except:
                print("[!] grant error!")

        if operate == 'revoke':
            if 'to' not in sql_words:
                print("[!] No to!")
                return
            try:
                self.remove_right(sql_words[1:-2], sql_words[-1])
            except:
                print("[!] revoke error!")

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
    db.use_database('lhj')
    db.run()
