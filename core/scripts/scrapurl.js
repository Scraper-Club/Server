function move_to_private(id){
    http_patch(scraper_url_api + id +'/','{"pool":"private"}');
}

function move_to_public(id){
    http_patch(scraper_url_api + id +'/','{"pool":"public"}');
}

function move_to_waiting(id){
    http_patch(scraper_url_api + id +'/','{"pool":"waiting"}');
}

function delete_url(id){
    http_delete(scraper_url_api + id +'/');
}

function delete_all(){
    if(confirm('This will remove all your URLs from all pools. Are you sure?')){
         http_delete(scraper_url_api);
    }
}