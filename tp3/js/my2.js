$(function (){
    try {



    $("#login").click(function (){
        user_id = $('input[name="user_id"]').val();
        if(user_id == ''){
            $('#fk').text('请输入正确的用户ID！')
            return
        }
        //alert(sjId)
        $.ajax({
              type: 'POST',
              url: 'http://119.91.20.121:55555/login',
              data:{ user_id:user_id},
              success:function(res){
                  if(res == 'null'||res == '[null]'){
                    $('#fk').text('请输入正确的用户ID！')
                  }else {
                      sessionStorage.setItem('token',res);
                      //alert(res)
                      //s = res.substring(2,res.length-2)
                      //$('#fk').text(s,'，欢迎登录！')
                      document.location.href="index.html";
                  }



              }

        })
    })


}catch (e){
        console.log(e)
    }

})