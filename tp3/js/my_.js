$(function() {
  const token1 = 'Bearer ' + window.sessionStorage.token;

  $.ajax({
    type: 'get',
    url: 'http://119.91.20.121:55555/out',
    async: true,
    cache: false,
    contentType: false,
    processData: false,
    beforeSend: function(request) {
      if (!token1) {
        // 处理未提供 token 的情况
      }
      request.setRequestHeader('Authorization', token1);
    },
    success: function(res) {
      console.log(res)
      if (!res) {
        document.location.href = 'login.html';
        window.parent.location.href = 'Login.html';
      } else {
        // s = res.substring(1,res.length-1)
        // $('#dqqq').text('欢迎登录：'+s+'，这是一个突破发货以及锁仓的网站')
      }
    },
    error: function(data) {
      console.log(data)
      document.location.href = 'login.html';
      window.parent.location.href = 'Login.html';
    }
  });

  $('#btnn').click(function() {
    $('#btnn').parent().attr('style', 'display:none');

    const sku = $('input[name="sku"]').val();
    const guojia = $('input[name="guojia"]').val();
    const suocang = $('input[name="suocang"]').val();
    const dqd = $('input[name="dqd"]').val();
    const addr = $('input[name="addr"]').val();
    const cookie = $('textarea[name="cookie"]').val();

    if (!sku || !guojia || !suocang || !cookie || !dqd || !addr) {
      alert('请填写完整数据!');
      handleInvalidData();
      return;
    }

    const yesorno = ersku(sku);
    if (yesorno === 0) {
      alert('sku填写错误！');
      handleInvalidData();
      return;
    }

    $.ajax({
      type: 'POST',
      url: 'http://119.91.20.121:55555/gogo',
      data: { sku: sku, guojia: guojia, suocang: suocang, cookie: cookie, dqd: dqd, addr: addr },
      beforeSend: function(request) {
        if (!token1) {
          // 处理未提供 token 的情况
        }
        request.setRequestHeader('Authorization', token1);
      },
      success: function(res) {
        if (res === 0) {
          res = '添加失败!';
        } else {
          alert(res);
          $('input[name="sku"]').val('');
          $('input[name="guojia"]').val('');
          $('input[name="suocang"]').val('');
          $('input[name="dqd"]').val('');
          $('input[name="addr"]').val('');
          $('textarea[name="cookie"]').val('');
        }

        setTimeout(handleInvalidData, 1000);
      },
      error: function(XMLHttpRequest, textStatus, errorThrown) {
        console.log('请求失败' + XMLHttpRequest.status);
        console.log('请求失败' + textStatus);
        console.log('请求失败' + errorThrown);

        if (XMLHttpRequest.status === 401) {
          document.location.href = 'login.html';
        } else {
          console.log(2);
        }

        setTimeout(handleInvalidData, 1000);
      }
    });
  });
  function handleInvalidData() {
    setTimeout(function() {
      $('#btnn').parent().attr('style', 'display:block;margin:0 auto;width:50%;text-align: center');
    }, 1000);
  }

  function ersku(skus) {
    const regex = /(B[A-Z0-9][^￥]+)￥([^￥]+)￥([^￥][^,|^，]?)/g;
    let match;
    const match_list = [];
    while ((match = regex.exec(skus)) !== null) {
      const asin = match[1];
      const sku = match[2];
      const count = match[3];
      console.log(`Asin: ${asin}，SKU: ${sku}， Count: ${count}`);
      const data = {
        asin: match[1],
        sku: match[2],
        count: match[3],
      };
      match_list.push(data);
    }
    if (match = regex.exec(skus) != null) {
      console.log(match_list);
      return 1;
    } else {
      console.log(1111);
      return 0;
    }
  }
});