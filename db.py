import sqlite3
import zlib
import base64

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

def empty_tables(table_names = ['articles', 'tags', 'merge_article_tag']):
    con = sqlite3.connect(db_name)
    c = con.cursor()
    for table in table_names:
        sql = f'delete from {table}'
        c.execute(sql)
    con.commit()
    con.close()


def insert_article(title, body):
    sql = f'insert into articles (title, body) values ("{title}", "{body}")'
    insert(sql)

def flatten(t):
    return [item for sublist in t for item in sublist]

def insert_article_with_tids(title, body, tids):
    insert_article(title, body)
    if len(tids) > 0:
        tids = [int(tid) for tid in tids]
        aids = select(f'select a.id from articles as a where a.title = "{title}"')
        aids = [int(aid[0]) for aid in aids]
        if len(aids) < 1:
            pass
        else:
            aid_tid_pairs = flatten([[(aid,tid) for tid in tids] for aid in aids])
            aid_tid_pairs = [str(item) for item in aid_tid_pairs]
            values = ','.join(aid_tid_pairs)
            sql = f'insert into merge_article_tag (aid, tid) values {values}'
            insert(sql)

def insert_tags(tag_names):
    if len(tag_names) < 1:
        pass
    else:
        values = ','.join([f'("{name}")' for name in tag_names])
        sql = f'insert into tags (name) values {values}'
        insert(sql)

def string_list_to_sql_in_function_param(string_list):
    return ",".join([f'"{text}"' for text in string_list])

def select_mock(bull_shit):
    return [(1, 'aa'),(2, 'bb')]

def select_tags_by_tag_names(tag_names):
    sql = f'select t.id, t.name from tags t where t.name in({string_list_to_sql_in_function_param(tag_names)})'
    tags = select(sql)
    tags = [{'id': tid, 'name': tname} for tid, tname in tags]
    return tags

def select_all_tags():
    sql = f'select t.id, t.name from tags as t'
    return select(sql)

def select_all_articles():
    sql = f'select a.id, a.title from articles as a'
    return select(sql)

def not_exist_tag_names(tag_names):
    # tags = select_mock(sql)
    tags = select_tags_by_tag_names(tag_names)
    tag_names_exist = [tag['name'] for tag in tags]
    names_not_exist = [name for name in tag_names if name not in tag_names_exist]
    return names_not_exist

# 同时创建和关联tag
def create_tags_if_not_exist_return_tags(tag_names):
    tag_names_to_create = not_exist_tag_names(tag_names)
    insert_tags(tag_names_to_create)
    tags = select_tags_by_tag_names(tag_names)
    return tags

def b64e(s):
    return base64.b64encode(s.encode()).decode()

def b64d(s):
    return base64.b64decode(s.encode("utf-8")).decode()

def compress(text):
    return b64e(text) 

def decompress(text):
    return b64d(text)
