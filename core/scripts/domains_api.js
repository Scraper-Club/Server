function delete_all(){
    if(confirm('This will remove all your domains and URLs from all pools. Are you sure?')){
         http_delete(scraper_domains_api);
    }
}

function delete_domain(id){
    if(confirm('This will remove all your URLs from this domain. Are you sure?')){
         http_delete(scraper_domains_api + id + '/');
    }
}