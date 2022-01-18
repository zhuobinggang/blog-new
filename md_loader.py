from db import insert_article

def read_markdown_file(name):
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
        tags = meta['tags']
    insert_article(name, body)

