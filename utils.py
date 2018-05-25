import re


def where_cond(sql):
    sql = sql[1:]
    return sql.split('=')


def set_cond(sql, chr):
    set_cond = re.compile(chr)
    set_cond = re.search(set_cond, sql).group().split(' ')[1:-1]
    # name_value = {}
    # for i in set_cond:
    #     name, value = i.split("=")
    #     name_value[name] = value
    return set_cond[0].split('=')


if __name__ == '__main__':
    print(where_cond("name=1 and age=1"))
    print(set_cond("Set a=1 from"))