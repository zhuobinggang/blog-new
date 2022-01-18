var app = new Vue({
  el: '#app',
  data: {
    article: {
        title: 'loading...',
        body: 'loading...',
        created: 'loading...',
        updated: 'loading...',
        tags: [],
    }
  }
})

const default_get_opt = {method: 'GET', headers: {}}

function json(res){
    return res.json()
}

function load_article(id){
    fetch(`/ajax-article/id/${id}`, default_get_opt).then(json).then((art) => {
      const c = new showdown.Converter()
      art.body = c.makeHtml(art.body)
      return art
    }).then((art) => {
      app.article = art
    })
}

let urlParams = new URLSearchParams(window.location.search);
load_article(urlParams.get('aid'))

