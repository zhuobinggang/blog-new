import sqlite3

def fake_arts(c):
    for i in range(20):
        c.execute(f'insert into articles(title, body) values ("title_{i}", "body_{i}")')

def fake_tags(c):
    for i in range(15):
        c.execute(f'insert into tags (name) values ("tag_{i}")')

def fake_merge_art_tag(c):
    sql = f'insert into merge_article_tag(aid, tid) values (19, 1), (19, 2), (19, 13), (17, 3), (18,3)'
    c.execute(sql)

def run():
    con = sqlite3.connect(db_name)
    c = con.cursor()
    fake_arts(c)
    fake_tags(c)
    fake_merge_art_tag(c)
    con.commit()
    con.close()
