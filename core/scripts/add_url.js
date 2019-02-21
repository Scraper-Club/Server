function add_field(){

        if(!validate_last()){
            alert('Please check last entered URL, it is invalid');
            return;
        }

        var form = $("#form_fields");
        var fields_count = parseInt($("#count").val());
        fields_count = fields_count + 1;
        $("#count").val(fields_count);
        form.append(create_input_field(fields_count));
        form.scrollTop(fields_count * 100);
    }

function validate_url(str) {
    var pattern = new RegExp('^(https?:\\/\\/)'+ // protocol
        '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.?)+[a-z]{2,}|'+ // domain name
        '((\\d{1,3}\\.){3}\\d{1,3}))'+ // OR ip (v4) address
        '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*'+ // port and path
        '(\\?[;&a-z\\d%_.~+=-]*)?'+ // query string
        '(\\#[-a-z\\d_]*)?$','i'); // fragment locator

    return pattern.test(str);
}

function create_input_field(id){

    var field_id = "url_" + id;
    var placeholder = 'Enter URL for scraping';

    var form_field = $('<div></div>')
                        .addClass("form-group row");

    var label = $('<label></label>')
                    .attr("for", field_id)
                    .addClass("col-2 col-form-label")
                    .html("Url " + id);

    var input_wrap = $('<div></div>')
                    .addClass("col-sm-10");

    var input = $('<input></input>')
                    .attr("type", "text")
                    .attr("id", field_id)
                    .attr("name", field_id)
                    .attr("placeholder", placeholder)
                    .addClass("form-control");

    form_field
        .append(label)
        .append(
            input_wrap
                .append(input)
        );

    return form_field;
}

function validate_last(){
    var fields_count = parseInt($("#count").val());
    return validate(fields_count);
}

function validate(id){
    var url = $('#url_' + id).val();
    return validate_url(url);
}

function validate_all(){
    var fields_count = parseInt($("#count").val());
    for(i = 1; i <= fields_count; i++){
        if(!validate(i)){
            alert(i + ' URL is invalid')
            return false;
        }
    }
    return true;
}