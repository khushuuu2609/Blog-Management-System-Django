$(document).ready(function(){
  
  
  $(document).on('click', '.like', function(){
    var id = $(this).attr('data');
    var totalLike = $('.total_like_display' + id).val();
  
    if(totalLike == undefined){
      totalLike = 0;
    }
  else{
    var total_like = Number(totalLike) + 1;
    var user_name = $('.user').val();
  }
    $.ajax({
      type:'GET',
      url :'/userApp/ajax_fetchdata',
      data :{
        'post_id':id,
      },
      success: function(data){
    
        $("#likedisplay" + id).html("<strong>"+data.post_detail+"<strong>");  
        $( '#like'+ id ).removeClass('like btn-default btn-sm');
        $( '#like'+ id ).addClass('dislike btn-success btn-sm');

        $('#like' + id).attr('Dislike')
        $('#icon'+ id).removeClass('fa fa-thumbs-up')
        $('#icon'+ id).addClass('fa fa-thumbs-down')              

      }
    });
  });
  
  
      $(document).on('click','.dislike',function(){
        var id = $(this).attr('data');
        $.ajax({
                  type:'GET',
                  url :'/userApp/ajax_fetchdata',
                  data :{
                    'post_id':id,
                  },
                  success: function(data){
                    console.log(parseInt(data.post_detail) , "$$$")
                    if(data.post_detail == 'NaN'){
                    $("#likedisplay" + id).html("<strong>"+0+"</strong>");
                  }
                  else{
                    var t = (data.post_detail)-1;
                    $("#likedisplay" + id).html("<strong>"+t+"</strong>");
                  }
                    $( '#like'+ id ).removeClass('dislike btn-success btn-sm');
                    $( '#like'+ id ).addClass('like btn-default btn-sm');

                    $('#icon'+ id).removeClass('fa fa-thumbs-down')
                    $('#icon'+ id).addClass('fa fa-thumbs-up')
                }
        })
      })
  
  
  
    $(document).on('click','.comment',function(){
      var id = $(this).attr('data1');
      $("#comment"+id).fadeToggle();
  
    });

    $(document).on('click','.reply',function(){
      var id = $(this).attr('data1');
      $("#reply"+id).fadeToggle();
  
    });
  
  
    $(document).on('click','.comment_btn',function(){
        
        var id = $(this).attr('data1');
        var date = new Date($.now());
        var total = $('.total_comment_display'+ id).val() ;
        console.log(total)
        if(total == undefined){
          total = 0
        }

        var total_comment = Number(total) + 1
        //console.log(total_comment)
        var comment = $('.comment'+ id).val();
        var user_name = $('.user').val();
        //check the comment text empty or not
        if( comment == ""){
          swal({
                text: "Please Insert the comment ",
                icon: "warning",
                button: "OK",
                dangerMode: true,
              })
        }
  
        else{
        $.ajax({
                  type:'GET',
                  url :'/userApp/ajax_add_comment',
                  data :{
                    'post_id':id,
                    'comment':comment
                  },
                  success: function(data){
  
                      $(".comment"+id).val("");
                      $("#comment_detail" + id).append("<span><strong>"+user_name+"-"+date+"</strong><br>"+data.comment+"</span><br><hr>");
                      $("#total_comment" + id).html("("+total_comment+")");
                      $('.total_comment_display'+ id).val(total_comment)
    
                }
          })
        }
      });

    
      $(document).on('click','.reply_btn',function(){
        

        var id = $(this).attr('data1');
        var reply_id = $('.reply_id').val();

        console.log(reply_id)
        var post = $('.post').val();
        var date = new Date($.now());
        var comment = $('.reply'+ id).val();
        var user_name = $('.user').val();
        //check the comment text empty or not
        if( comment == ""){
          swal({
                text: "Please Insert the Reply comment ",
                icon: "warning",
                button: "OK",
                dangerMode: true,
              })
        }
  
        else{
        $.ajax({
                  type:'GET',
                  url :'/userApp/ajax_add_reply',
                  data :{
                    'comment_id':id,
                    'post_id':post,
                    'reply':comment
                  },
                  success: function(data){
                      $(".reply"+id).val("");
                      console.log(id)
                      $("#reply_detail" + id).append("<span><strong>"+user_name+"-"+date+"</strong><br>"+data.reply+"<hr></span>");
                      
                }
          })
        }
      });
  
    });
  