token1 ='Bearer '+ window.sessionStorage.token;
$(function (){


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
                window.location.href='login.html';
                window.parent.location.href = "Login.html";//让父页面一起跳转
              }



          },
 		        error: function (data){
                //alert(data)
                     window.location.href='login.html';
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
        //$('#fk').text('请稍等。。。')
        $('#btnn').parent().attr('style',"display:none")
        // setTimeout(function(){
        //                     //$('#btnn').attr('disabled',"true");添加disabled属性
        //                     $('#btnn').parent().attr('style',"display:none")
        //
        //                     },100);

        //alert(1)
        sjId = $('input[name="sjId"]').val();
        sku = $('input[name="sku"]').val();
        addr = $('input[name="addr"]').val();
        suocang = $('input[name="suocang"]').val();
        // if (sjId == '' || sku == '' || addr == '' || suocang == ''){
        //     alert('填写错误！')
        //     setTimeout(function(){
        //                     //$('#fk').text('请输入突破id进行操作')
        //                       //$('#btnn').removeAttr("disabled"); 移除disabled属性
        //                         $('#btnn').parent().attr('style',"display:block")
        //                     },3000);
        //     return
        // }
        //alert(sjId)
        yesorno = ersku(sku)
        if(yesorno == 0){
            alert('sku填写错误！')
            setTimeout(function(){
                            //$('#fk').text('请输入突破id进行操作')
                              //$('#btnn').removeAttr("disabled"); 移除disabled属性
                                $('#btnn').parent().attr('style',"display:block")
                            },1000);
            return
        }
        $.ajax({
              type: 'POST',
              url: 'http://119.91.20.121:55555/xiugaisku',
              data:{ sjId:sjId,sku:sku,addr:addr,suocang:suocang},
            beforeSend: function(request) {
                        request.setRequestHeader('Authorization', token1);
                    },
              success:function(response,status,xhr){
                  data = eval(response)
                  if(data == 'null'||data == null){
                    alert('突破编号可能填写错误！')
                  }else {
                      //s = response.substring(2,response.length-2)
                      if(data == '0' || data == 0){
                        alert('没有找到此任务id')
                    }else {
                        alert(data)

                    $('input[name="sku"]').val('');
                    $('input[name="addr"]').val('');
                    $('input[name="suocang"]').val('');

                        //   $('#fk').oneTime('2s',function(){ //1das
                        //       $('#fk').text('请输入编号')
                        //
                        //
                        //     });
                        //   alert(response);

                    }
                  }
                setTimeout(function(){
                            //$('#fk').text('请输入突破id进行操作')
                              //$('#btnn').removeAttr("disabled"); 移除disabled属性
                                $('#btnn').parent().attr('style',"display:block")
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
                                $('#btnn').parent().attr('style',"display:block")
                            },3000);


    }

        })
    })

    $('#cx').click(function (){
        $('#record').empty()//删除所有子体
        $('#cx').parent().attr('style',"display:none")
        var sjId1 = $('input[name="sjId1"]').val();
        $.ajax({
              type: 'POST',
              url: 'http://119.91.20.121:55555/showuserdata',
            beforeSend: function(request) {
                        request.setRequestHeader('Authorization', token1);
                    },
            data:{ sjId1:sjId1},
              success:function(response,status,xhr){
                  datas = eval(response)
                  console.log(datas);
                  $.each(datas,function(i,item){
                      var shouquan = ''
                      if(item[9] == '1' || item[9] == '0'){
                          item[9] = 'null'
                      }
                      if(item[13] == '0' || item[13] == '1'){
                          item[13] = 'null'
                      }
                      if(item[3] == '0' || item[3] == '1'){
                          item[3] = 'null'
                      }
                      if(item[11] == '0' || item[11] == '1'){
                          item[11] = 'null'
                      }if(item[7] == '0' || item[8] == '0') {
                          shouquan = '未授权'
                      }else{
                          shouquan = '已授权'
                      }

                      //item[7]item[8]


                       $('#record').append('<tr>' +
                        '<td class="num" style="" id="sjId_'+i+'">'+item[1]+'</td>' +
                        '<td class="name" id="sku">'+item[2]+'</td>' +
                        '<td class="startdate" id="suocang">'+item[3]+'</td>' +
                        '<td class="enddate" id="guojia">'+item[4]+'</td>' +
                        '<td class="company" id="addr">'+item[13]+'</td>' +
                           '<td class="company" id="dqdfk">'+item[11]+'</td>' +
                           '<td class="shouquan" id="shouquan">'+shouquan+'</td>' +
                           '<td class="company" id="fk">'+item[9]+'</td>' +
                        '<td width="100" class="app"><input type="button" value="建&nbsp;&nbsp;仓" onclick="caozuo('+i+')"/></td>' +
                        '</tr>');

                  })


                setTimeout(function(){
                            //$('#fk').text('请输入突破id进行操作')
                              //$('#btnn').removeAttr("disabled"); 移除disabled属性
                                $('#cx').parent().attr('style',"display:block")
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

    }

        })













    })





})
function caozuo(i) {
    var sjId = $("#sjId_"+i).text();
    console.log(sjId)
    $.ajax({
              type: 'POST',
              url: 'http://119.91.20.121:55555/jiancang',
              data:{ sjId:sjId},
            beforeSend: function(request) {
                        request.setRequestHeader('Authorization', token1);
                    },
              success:function(response,status,xhr){
                  data = eval(response)
                  alert(data)
                  // if(data == 'null'||data == null){
                  //   $('#fk').text('突破编号可能填写错误！')
                  // }else {
                  //     //s = response.substring(2,response.length-2)
                  //     if(data == '0' || data == 0){
                  //       $('#fk').text('没有找到此任务id')
                  //   }else {
                  //       $('#fk').text(data)
                  //
                  //       //   $('#fk').oneTime('2s',function(){ //1das
                  //       //       $('#fk').text('请输入编号')
                  //       //
                  //       //
                  //       //     });
                  //       //   alert(response);
                  //
                  //   }
                  // }
                // setTimeout(function(){
                //             //$('#fk').text('请输入突破id进行操作')
                //               //$('#btnn').removeAttr("disabled"); 移除disabled属性
                //                 $('#btnn').parent().attr('style',"display:block")
                //             },3000);


              },
    error: function (XMLHttpRequest, textStatus, errorThrown) {
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

}
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