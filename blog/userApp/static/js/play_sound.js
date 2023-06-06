$(document).ready(function(){
    $(document).on('click','#play',function(){
        $.ajax({
            type: "GET",
            url: "/userApp/play_sound",
        });
    });

})