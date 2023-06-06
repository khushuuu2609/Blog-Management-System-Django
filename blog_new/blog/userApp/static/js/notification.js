$(document).ready(function(){
    $(document).on('click','.notification',function(){
        alert($(this).attr('notification_data'))
        var n_id = $(this).attr('notification_data');
        console.log(n_id)

    })
});
  