from db import insert_article, create_tags_if_not_exist_return_tags, insert_article_with_tids, empty_tables, compress
from os import walk

def read_markdown_file(name):
    name = name.strip('.md')
    f = open(f'markdown/{name}.md')
    text = f.read()
    f.close()
    return text

def read_meta(text):
    lines = [line for line in text.split('\n') if len(line) > 0]
    possible_meta = lines[-1]
    if possible_meta.startswith('meta:'):
        metas = possible_meta.strip('meta:').strip()
        metas = [meta.strip() for meta in metas.split(',')]
        key_values = [meta.split(' ') for meta in metas]
        dic = {}
        for item in key_values:
            dic[item[0]] = item[1:]
        return dic
    else:
        return {}

def test(name):
    body = read_markdown_file(name)
    meta = read_meta(body)
    return meta

def store_md_to_db(name):
    body = read_markdown_file(name)
    meta = read_meta(body)
    if 'tags' in meta:
        tag_names = [name.strip() for name in meta['tags']]
        tags = create_tags_if_not_exist_return_tags(tag_names)
        tids = [tag['id'] for tag in tags]
        insert_article_with_tids(name, compress(body), tids)
    else:
        insert_article(name, compress(body))

def reload_all_md():
    empty_tables()
    mypath = './markdown'
    filenames = next(walk(mypath), (None, None, []))[2]  # [] if no file
    filenames = [name.strip('.md') for name in filenames if name.endswith('.md')]
    for filename in filenames:
        store_md_to_db(filename)



