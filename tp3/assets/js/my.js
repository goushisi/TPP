$(function (){
    var token1 ='Bearer '+ window.sessionStorage.token;
    $.ajax({
          type: 'get',
          url: 'http://119.91.20.121:55555/out',
        //containType: { cookie: 'session="qwerq111"'},
        //data:{ aa:1122},
        async:true,
        cache: false,
        contentType: false,
        processData: false,
        beforeSend: function(request) {
                        request.setRequestHeader('Authorization', token1);
                    },
          success:function(res){
              console.log(res)
                if (res == ''||res == null||res == 'null'||res == '"null"'||res == false){
                document.location.href='login.html';
              }else {
                    s = res.substring(1,res.length-1)
                    $('#dqqq').text('欢迎登录：'+s+'，这是一个突破发货以及锁仓的网站')
                }



          },
 		        error: function (data){
                console.log(data)
                    document.location.href='login.html';
                }

        })


    $('#btnn').click(function (){
        var sku = $('input[name="sku"]').val();
        var guojia = $('input[name="guojia"]').val();
        var suocang = $('input[name="suocang"]').val();
        var dqd = $('input[name="dqd"]').val();
        var addr = $('input[name="addr"]').val();
        var cookie = $('textarea[name="cookie"]').val();

        if (sku == '' && guojia =='' && suocang == '' && cookie == '' && dqd == ''){
            return
        }
        $.ajax({
          type: 'POST',
          url: 'http://119.91.20.121:55555/gogo', //119.91.20.121
          data:{ sku:sku,guojia:guojia,suocang:suocang,cookie:cookie,dqd:dqd,addr:addr},
            beforeSend: function(request) {
                        request.setRequestHeader('Authorization', token1);
                    },
          success:function(res){
              //alert(res)
              if (res == 0){
                  return
              }
                sessionStorage.setItem('sjId',res)
                document.location.href="fankui.html";

          },error: function (XMLHttpRequest, textStatus, errorThrown){
                console.log("请求失败"+XMLHttpRequest.status);
        console.log("请求失败"+textStatus);
        console.log("请求失败"+errorThrown);
        if (XMLHttpRequest.status == 401){
            document.location.href='login.html';
        }else{
            console.log(2);
        }
                }

        })
    })
})