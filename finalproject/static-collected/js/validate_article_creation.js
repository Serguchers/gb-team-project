$( document ).ready(function() {
    function validateElem(elem, cond, event){
        if ($(elem)[0].value.length <= cond){
            $(elem)[0].style.borderColor = 'red'
            event.preventDefault();
        };
    }

    $('html').on('click', 'input[name="create-article"]', () =>{
        validateElem('#id_title', 8 , event);
        validateElem('#id_text', 100 , event);
        validateElem('#id_tags', 0 , event);
        }
    )
})