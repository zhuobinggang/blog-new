//var opts = {
//  method: 'GET',      
//  headers: {}
//};
//fetch('/get-data', opts).then(function (response) {
//  return response.json();
//})
//.then(function (body) {
//  //doSomething with body;
//});

var app = new Vue({
  el: '#app',
  data: {
    articles: [],
    tags_recently: [],
  }
})

const default_get_opt = {method: 'GET', headers: {}}

function json(res){
    return res.json()
}

function get_articles(page = 1){
    fetch(`/ajax-articles/page/${page}`, default_get_opt).then(json).then((articles) => {
      app.articles = articles
    })
}

function get_tags(page = 1){
    fetch(`/ajax-tags/page/${page}`, default_get_opt).then(json).then((tags) => {
      app.tags_recently = tags
    })
}

function get_tags_recently(){
    fetch(`/ajax-tags-recently`, default_get_opt).then(json).then((tags) => {
      dic = {}
      for(tag of tags){
        dic[tag['tid']] = tag
      }
      tags = []
      for(key in dic){
        tags.push(dic[key])
      }
      app.tags_recently = tags
    })
}

// when refreshed
get_articles(1)
get_tags_recently()
