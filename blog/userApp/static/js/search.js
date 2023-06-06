$(document).ready(function(){
    $('#search').keyup(function() {
        $.ajax({
            type: "GET",
            url: "/userApp/search_ajax_view",
            data: {
                'search_text' : $('#search').val(),
                'csrfmiddlewaretoken' : $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(data){
                
                    
                $('#search-results').html(data)

                $('#main_content').hide()
            }
          
        });
    });
    });
    