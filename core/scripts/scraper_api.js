var auth = 'Token '+ api_key;
var api_url = window.location.origin + '/api/v1/'

var scraper_url_api = api_url + 'urls/';
var scraper_domains_api = api_url + 'domains/';
var scraper_scrapes_api = api_url + 'scrapes/';
var scraper_ipaddr_api = api_url + 'ip/';

function reload_on_success(res){
    location.reload();
}

function reload(res){
    location.reload();
}

function base_err_handler(err){
    if(err.status == 404){
        location.reload();
    }else{
        alert('Failed: ' + err.response.body.detail);
    }
}

function get_handlers(on_success, on_failure){
    if(on_success)
        success = on_success;
    else
        success = reload;

    if(on_failure)
        failure = on_failure;
    else
        failure = base_err_handler;

    return [success, failure]
}

function http_delete(url, on_success, on_failure){
    handlers = get_handlers(on_success, on_failure);
    superagent
        .delete(url)
        .set('Authorization',auth)
        .set('Content-type','application/json')
        .then(handlers[0])
        .catch(handlers[1]);
}

function http_patch(url, body, on_success, on_failure){
    handlers = get_handlers(on_success, on_failure);
    superagent
        .patch(url)
        .set('Authorization',auth)
        .set('Content-type','application/json')
        .send(body)
        .then(handlers[0])
        .catch(handlers[1]);
}

function http_post(url, body, on_success, on_failure){
    handlers = get_handlers(on_success, on_failure);
    superagent
        .post(url)
        .set('Authorization',auth)
        .set('Content-type','application/json')
        .send(body)
        .then(handlers[0])
        .catch(handlers[1]);
}

