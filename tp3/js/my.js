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
                window.parent.location.href = "Login.html";//让父页面一起跳转
              }else {
                    // s = res.substring(1,res.length-1)
                    // $('#dqqq').text('欢迎登录：'+s+'，这是一个突破发货以及锁仓的网站')
                }



          },
 		        error: function (data){
                console.log(data)
                    document.location.href='login.html';
                    window.parent.location.href = "Login.html";//让父页面一起跳转
                }

        })


    $('#btnn').click(function (){
        $('#btnn').parent().attr('style',"display:none")
        var sku = $('input[name="sku"]').val();
        var guojia = $('input[name="guojia"]').val();
        var suocang = $('input[name="suocang"]').val();
        var dqd = $('input[name="dqd"]').val();
        var addr = $('input[name="addr"]').val();
        var cookie = $('textarea[name="cookie"]').val();

        if (sku == '' || guojia =='' || suocang == '' || cookie == '' || dqd == '' || addr =='' ){
            alert('请填写完整数据!')
            setTimeout(function(){
                            //$('#fk').text('请输入突破id进行操作')
                              //$('#btnn').removeAttr("disabled"); 移除disabled属性
                                $('#btnn').parent().attr('style',"display:block;margin:0 auto;width:50%;text-align: center")
                            },1000);
            return
        }
        yesorno = ersku(sku)
        if(yesorno == 0){
            alert('sku填写错误！')
            setTimeout(function(){
                            //$('#fk').text('请输入突破id进行操作')
                              //$('#btnn').removeAttr("disabled"); 移除disabled属性
                                $('#btnn').parent().attr('style',"display:block;margin:0 auto;width:50%;text-align: center")
                            },1000);
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
                  res = '添加失败!'
              }else {
                  alert(res)
                  $('input[name="sku"]').val('');
                  $('input[name="guojia"]').val('');
                  $('input[name="suocang"]').val('');
                  $('input[name="dqd"]').val('');
                  $('input[name="addr"]').val('');
                  $('textarea[name="cookie"]').val('');
              }

                //sessionStorage.setItem('sjId',res)
                // document.location.href="fankui.html";
            setTimeout(function(){
                            //$('#fk').text('请输入突破id进行操作')
                              //$('#btnn').removeAttr("disabled"); 移除disabled属性
                                $('#btnn').parent().attr('style',"display:block;margin:0 auto;width:50%;text-align: center")
                            },1000);
          },error: function (XMLHttpRequest, textStatus, errorThrown){
                console.log("请求失败"+XMLHttpRequest.status);
        console.log("请求失败"+textStatus);
        console.log("请求失败"+errorThrown);
        if (XMLHttpRequest.status == 401){
            document.location.href='login.html';
        }else{
            console.log(2);
        }
        setTimeout(function(){
                            //$('#fk').text('请输入突破id进行操作')
                              //$('#btnn').removeAttr("disabled"); 移除disabled属性
                                $('#btnn').parent().attr('style',"display:block;margin:0 auto;width:50%;text-align: center")
                            },1000);

                }

        })
    })
})

function ersku(skus){

    var regex = /(B[A-Z0-9][^￥]+)￥([^￥]+)￥([^￥][^,|^，]?)/g;
    //var str = "B0B18FFMCV￥EL-WS/TN433-4P-MTPT-2106￥165,B0B3RBP6JN￥EL-WS/LC3013-5P-101-T3￥150";
    var match;
    let match_list = []
    while ((match = regex.exec(skus)) !== null) {
        var asin = match[1];
        var sku = match[2];
        var count = match[3];
        console.log("Asin: " + asin + "，SKU: " + sku + "， Count: " + count);
        data = {
            'asin' : match[1],
            'sku' : match[2],
            'count' : match[3]
        }
        match_list.push(data)
    }
    if (match = regex.exec(skus) != null) {
        console.log(match_list);
        return 1
    }else {
        console.log(1111);
        return 0
    }

}