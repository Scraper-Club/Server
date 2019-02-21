function create_actions(actions){
            if (actions.size == 0)
                return;
            actions.forEach(function(val, key, map){
                if(val.elem){
                    elem=val.elem;
                }else{
                    elem='a';
                }

                var action = $('#actions').append('<'+elem+'>'+key+'</'+elem+'>').children().last();
                if(val.href){
                    $(action).attr('href', val.href);
                }
                if(val.class){
                    $(action).attr('class', 'btn btn-block m-1 ' + val.class);
                }
                if(val.onclick){
                    $(action).attr('onclick', val.onclick);
                }
            });
        }