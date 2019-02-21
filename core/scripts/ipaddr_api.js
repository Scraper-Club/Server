function delete_ip(id){
    if(confirm('This will remove IP address and its configuration. Are you sure?')){
         http_delete(scraper_ipaddr_api + id + '/');
    }
}

function patch_ip(id, rate_type, rate_limit){
    http_patch(scraper_ipaddr_api + id + '/',JSON.stringify({'rate_type':rate_type,'rate_limit':rate_limit}));
}