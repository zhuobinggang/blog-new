var app = new Vue({
  el: '#app',
  data: {
    articles: [],
    tags_recently: [],
    tag_name: '',
  }
})

const default_get_opt = {method: 'GET', headers: {}}

function json(res){
    return res.json()
}

function get_articles_by_tag(tid = 1, page = 1){
    fetch(`/ajax-articles-by-tag/tag/${tid}/page/${page}`, default_get_opt).then(json).then((articles) => {
      app.articles = articles
    })
}


let urlParams = new URLSearchParams(window.location.search);
get_articles_by_tag(urlParams.get('tid'))
app.tag_name = urlParams.get('name')
