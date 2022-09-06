$( document ).ready(function() {

    function inputClickEvent() {
        $('html').on('click', ".reply-to", function(){
            console.log('clicked')
            let reply_text_field_id = event.target.classList[1]
            let reply_text_field = $(`.reply-form.reply.${reply_text_field_id}`)[0]
            reply_text_field.style.display = 'block'
        });
    };
    inputClickEvent();

    $('html').on('click', '[name="write-comment"]', ()=>{
        $.ajax({
            type: "POST",
            headers: {'X-CSRFToken': Cookies.get('csrftoken')},
            data: {'body': $('.comment-area').val()},
            success: function(data) {
                $('.comment-form').find('.comment-area')[0].value = ''
                $('.comments').html(data.result);
            }

        });
        event.preventDefault();
    });

    $('html').on('click', '[name="write-reply"]', ()=>{
        $.ajax({
            type: "POST",
            headers: {'X-CSRFToken': Cookies.get('csrftoken')},
            data: {'body': $('.reply-form.reply').find('.comment-area').val(),
                    'parent_id': $('[name="parent_id"]').attr('value')},
            success: function(data) {
                $('.reply-form').find('.comment-area')[0].value = ''
                $('.comments').html(data.result);
            }
        });
        event.preventDefault();
    });

})