from bottle import route, run, template
from bottle import static_file
import json
import sqlite3

db_name = 'blog'

def select(sql):
    con = sqlite3.connect(db_name)
    c = con.cursor()
    c.execute(sql)
    res = c.fetchall()
    con.close()
    return res


@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./static/html')

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

# (21, 'title_19', 'body_19', '2022-01-17 16:15:10', '2022-01-17 16:15:10', '')
def article2dic(art):
    idx, title, body, created, updated, _ = art
    return {'id': idx, 'title': title, 'body': body, 'created': created, 'updated': updated} 

def tag2dic(tag):
    idx, name = tag
    return {'id': idx, 'name': name}

def default_limit_offset(page_num):
    page_num = int(page_num)
    limit = 10
    offset = (page_num - 1) * limit
    return limit, offset

@route('/ajax-articles/page/<page_num>')
def ajax_articles(page_num):
    limit, offset = default_limit_offset(page_num)
    arts = select(f'select * from articles order by id desc limit {limit} offset {offset}')
    return json.dumps([article2dic(art) for art in arts])

@route('/ajax-tags/page/<page_num>')
def ajax_tags(page_num):
    limit, offset = default_limit_offset(page_num)
    tags = select(f'select * from tags order by id desc limit {limit} offset {offset}')
    return json.dumps([tag2dic(tag) for tag in tags])

run(host='localhost', port=8080)

