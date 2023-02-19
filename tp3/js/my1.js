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
              }



          },
 		        error: function (data){
                //alert(data)
                    document.location.href='login.html';
                }

        })

    // id = sessionStorage.getItem('sjId')

    // if( id != '' && id != null && id != 'null'){
    //     $('#fk').text(id)
    //
    // }

    //#fk
    //.btn btn-link-1 launch-modal
    // $('#btnn').click(function (){
    //
    //     setTimeout(function(){
    //                         //$('#btnn').attr('disabled',"true");添加disabled属性
    //                         $('#btnn').parent().attr('style',"display:none")
    //                         },500);
    //     //alert(1)
    //     sjId = $('input[name="sjId"]').val();
    //     if (sjId == ''){
    //         $('#fk').text('突破编号可能填写错误！')
    //         setTimeout(function(){
    //                         $('#fk').text('请输入突破id进行操作')
    //                           //$('#btnn').removeAttr("disabled"); 移除disabled属性
    //                             $('#btnn').parent().attr('style',"display:block")
    //                         },5000);
    //         return
    //     }
    //     //alert(sjId)
    //     $.ajax({
    //           type: 'POST',
    //           url: 'http://119.91.20.121:55555/go',
    //           data:{ sjId:sjId},
    //         beforeSend: function(request) {
    //                     request.setRequestHeader('Authorization', token1);
    //                 },
    //           success:function(response,status,xhr){
    //               if(response == 'null'){
    //                   $('#fk').text('突破编号可能填写错误！')
    //                   setTimeout(function(){
    //                         $('#fk').text('请输入突破id进行操作')
    //                           //$('#btnn').removeAttr("disabled"); 移除disabled属性
    //                             $('#btnn').parent().attr('style',"display:block")
    //                         },5000);
    //                   return
    //               }
    //               data = eval(response)
    //               if(data[1] == '1' || data[1] == 1){
    //                   $('#dqd').text('没有多渠道信息！')
    //               }else {
    //                   $('#dqd').text(data[1])
    //               }
    //
    //               if(data[0] == 'null'||data[0] == null || data[0] == 'None'){
    //                 $('#fk').text('突破编号可能填写错误！')
    //               }else {
    //                   if(data[0] == '1'||data[0] == '0'){
    //                     $('#fk').text('操作未完成，请等待......')
    //                 }else {
    //                       $('#fk').text(data[0])
    //
    //
    //
    //                 }
    //
    //               }
    //                 setTimeout(function(){
    //                         $('#fk').text('请输入突破id进行操作')
    //                           //$('#btnn').removeAttr("disabled"); 移除disabled属性
    //                             $('#btnn').parent().attr('style',"display:block")
    //                         },5000);
    //
    //
    //           },
    // error: function (XMLHttpRequest, textStatus, errorThrown) {
    //     console.log("请求失败"+XMLHttpRequest.status);
    //     console.log("请求失败"+textStatus);
    //     console.log("请求失败"+errorThrown);
    //     if (XMLHttpRequest.status == 401){
    //         document.location.href='login.html';
    //     }else{
    //         console.log(2);
    //     }
    //
    // }
    //
    //     })
    // })




})