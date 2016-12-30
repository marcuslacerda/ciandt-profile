'use strict';

app.config(['$httpProvider', function($httpProvider) {
  $httpProvider.interceptors.push(['$q', '$location', '$injector', function($q, $location, $injector) {

    return {
      responseError: function(response) {
        console.log('STATUS => ' + response.status)
        if (response.status === 401 || response.status === 403) {
          var $auth = $injector.get('$auth')
          $auth.logout()
          $location.path('/login')
        }
        return $q.reject(response);
      }
    };

  }]);

}]);

