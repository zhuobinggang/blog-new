from bottle import route, run, template, redirect
from bottle import static_file
from db import select, decompress
import json

@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./static/html')

@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

# (21, 'title_19', 'body_19', '2022-01-17 16:15:10', '2022-01-17 16:15:10', '')
def article2dic(art):
    idx, title, created, updated = art
    return {'id': idx, 'title': title, 'created': created, 'updated': updated} 

def tag2dic(tag):
    idx, name = tag
    return {'id': idx, 'name': name}

def default_limit_offset(page_num):
    page_num = int(page_num)
    limit = 10
    offset = (page_num - 1) * limit
    return limit, offset

def number_list_to_sql_in_function_param(number_list):
    return ",".join([str(num) for num in number_list])

def aid_tag_names_to_dic(aid_tag_names):
    return [{"aid":aid, "tag_name": tag_name, "tag_id": tid} for aid, tag_name, tid in aid_tag_names]

def select_from_aid_tag_names(aid_tag_names, art):
    return [aid_tag_name for aid_tag_name in aid_tag_names if aid_tag_name['aid'] == art['id']]

@route('/ajax-articles/page/<page_num>')
def ajax_articles(page_num):
    limit, offset = default_limit_offset(page_num)
    arts = select(f'select id, title, created, updated from articles order by id desc limit {limit} offset {offset}')
    arts = [article2dic(art) for art in arts]
    aids = [art['id'] for art in arts]
    aid_tag_names = select(f'select m.aid,t.name,t.id from merge_article_tag as m left join tags as t on m.tid = t.id where m.aid in({number_list_to_sql_in_function_param(aids)})')
    aid_tag_names = aid_tag_names_to_dic(aid_tag_names)
    arts = [{**art, **{'tags': select_from_aid_tag_names(aid_tag_names, art)}} for art in arts]
    return json.dumps(arts)


@route('/ajax-articles-by-tag/tag/<tid>/page/<page_num>')
def ajax_articles_by_tag(tid, page_num):
    limit, offset = default_limit_offset(page_num)
    merges = select(f'select m.id, a.title, a.id from merge_article_tag as m left join articles as a on m.aid = a.id where m.tid = {tid} order by m.id desc limit {limit} offset {offset}')
    arts = [{'id': aid, 'mid': mid, 'title': title} for mid, title, aid in merges]
    aids = [art['id'] for art in arts]
    aid_tag_names = select(f'select m.aid,t.name,t.id from merge_article_tag as m left join tags as t on m.tid = t.id where m.aid in({number_list_to_sql_in_function_param(aids)})')
    aid_tag_names = aid_tag_names_to_dic(aid_tag_names)
    arts = [{**art, **{'tags': select_from_aid_tag_names(aid_tag_names, art)}} for art in arts]
    return json.dumps(arts)


@route('/ajax-tags/page/<page_num>')
def ajax_tags(page_num):
    limit, offset = default_limit_offset(page_num)
    tags = select(f'select * from tags order by id desc limit {limit} offset {offset}')
    return json.dumps([tag2dic(tag) for tag in tags])


@route('/ajax-tags-recently')
def ajax_tags_recently():
    tags = select(f'select t.id, t.name, m.aid from merge_article_tag as m left join tags as t on m.tid = t.id order by m.id desc limit 10')
    tags = [{'tid':tid, 'name': name, 'aid': aid} for tid, name, aid in tags]
    return json.dumps(tags)

@route('/ajax-article/id/<aid>')
def ajax_article(aid):
    arts = select(f'select id, title, body, created, updated from articles where id = {aid}')
    art = arts[0]
    idx, title, body, created, updated = art
    body = decompress(body)
    art = {'id': idx, 'title': title, 'body': body, 'created': created, 'updated': updated}
    tags = select(f'select t.id, t.name, m.aid from merge_article_tag as m left join tags as t on m.tid = t.id where m.aid = {idx}')
    tags = [{'tid': tag[0], 'name': tag[1], 'aid': tag[2]} for tag in tags]
    res = {**art, **{'tags': tags}}
    return json.dumps(res)

@route('/favicon.ico')
def favicon():
    redirect('/static/favicon.ico')

run(host='localhost', port=8080)

