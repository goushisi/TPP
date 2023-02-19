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
                if (res == ''||res == null||res == 'null'||res == '"null"'||res == false){
                document.location.href='login.html';
                window.parent.location.href = "Login.html";//让父页面一起跳转
              }



          },
 		        error: function (data){
                //alert(data)
                    document.location.href='login.html';
                    window.parent.location.href = "Login.html";//让父页面一起跳转
                }

        })

    // id = sessionStorage.getItem('sjId')
    // if( id != ''){
    //   $('#fk').text(id)
    // }

    //#fk
    //.btn btn-link-1 launch-modal
    $('#btnn').click(function (){
        setTimeout(function(){
                            //$('#btnn').attr('disabled',"true");添加disabled属性
                            $('#btnn').parent().attr('style',"display:none")
                            },500);

        //alert(1)
        sjId = $('input[name="sjId"]').val();
        sku = $('input[name="sku"]').val();
        suocang = $('input[name="suocang"]').val();
        dqd = $('input[name="dqd"]').val();
        addr = $('input[name="addr"]').val();

        yesorno = ersku(sku)
        if(yesorno == 0){
            alert('sku格式填写错误！')
            setTimeout(function(){
                            //$('#fk').text('请输入突破id进行操作')
                              //$('#btnn').removeAttr("disabled"); 移除disabled属性
                                $('#btnn').parent().attr('style',"display:block;margin:0 auto;width:50%;text-align: center")
                            },1000);
            return
        }
        if (sjId == '' || sku == '' || suocang == '' || dqd == '' || addr == ''){
            setTimeout(function(){
                            //$('#fk').text('请输入突破id进行操作')
                              //$('#btnn').removeAttr("disabled"); 移除disabled属性
                                $('#btnn').parent().attr('style',"display:block;margin:0 auto;width:50%;text-align: center")
                            },1000);
            return
        }

                $.ajax({
              type: 'POST',
              url: 'http://119.91.20.121:55555/zengjiahuojian',
              data:{ sjId:sjId,sku:sku,suocang:suocang,dqd:dqd,addr:addr},
            beforeSend: function(request) {
                        request.setRequestHeader('Authorization', token1);
                    },
              success:function(response,status,xhr){
                  datas = eval(response)
                  alert(datas)
                  $('input[name="sjId"]').val('');
                  $('input[name="sku"]').val('');
                  $('input[name="suocang"]').val('');
                  $('input[name="dqd"]').val('');
                  $('input[name="addr"]').val('');

                setTimeout(function(){
                            //$('#fk').text('请输入突破id进行操作')
                              //$('#btnn').removeAttr("disabled"); 移除disabled属性
                                $('#btnn').parent().attr('style',"display:block;margin:0 auto;width:50%;text-align: center")
                            },1000);


              },
    error: function (XMLHttpRequest, textStatus, errorThrown) {
        console.log("请求失败"+XMLHttpRequest.status);
        console.log("请求失败"+textStatus);
        console.log("请求失败"+errorThrown);
        if (XMLHttpRequest.status == 401){
            document.location.href='login.html';
            window.parent.location.href = "Login.html";//让父页面一起跳转
        }else{
            console.log(2);
        }
        setTimeout(function(){
                            //$('#fk').text('请输入突破id进行操作')
                              //$('#btnn').removeAttr("disabled"); 移除disabled属性
                                $('#btnn').parent().attr('style',"display:block;margin:0 auto;width:50%;text-align: center")
                            },3000);


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