(function() {
  'use strict';
  window['counter'] = 0;
  var snackbarContainer = document.querySelector('#quit-info');
  var showToastButton = document.querySelector('#quit');
  var handler = function(event) {
    window.location.href='login.html';
  };
  showToastButton.addEventListener('click', function() {
    'use strict';
    var data = {
      message: '已退出登录',
      timeout: 2000,
      actionHandler: handler,
      actionText: '重新登陆'
    };
    snackbarContainer.MaterialSnackbar.showSnackbar(data);
  });
}());
