import sqlite3

db_name = 'blog'

def select(sql):
    con = sqlite3.connect(db_name)
    c = con.cursor()
    c.execute(sql)
    res = c.fetchall()
    con.close()
    return res

def insert(sql):
    con = sqlite3.connect(db_name)
    c = con.cursor()
    c.execute(sql)
    con.commit()
    con.close()

def insert_article(title, body):
    sql = f'insert into articles (title, body) values ("{title}", "{body}")'
    insert(sql)

def string_list_to_sql_in_function_param(string_list):
    return ",".join([f'"{text}"' for text in string_list])

def create_tags_if_not_exist_return_tid(tags):
    sql = f'select t.id, t.name from tags t where t.name in({string_list_to_sql_in_function_param(tags)})'
    return sql
