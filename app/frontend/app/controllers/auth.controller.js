app.controller('AuthController', ['$scope', '$http', '$location', '$auth', '$mdToast', 'Account',
  function($scope, $http, $location, $auth, $mdToast, Account){

  $scope.isAuthenticated = function() {
    return $auth.isAuthenticated();
  };

  // TODO - use Account resources
  if ($auth.isAuthenticated()) {
    Account.getProfile()
      .then(function(response) {
        console.log(response.data)
        $scope.user = response.data;
      })
      .catch(function(response) {
        console.log('ERROR')
        console.log(response)
      });
  }

  $scope.authenticate = function(provider) {
    console.log('authenticate' + provider)
    $auth.authenticate(provider, {accessType: 'offline'})
      .then(function() {
        console.log('google authenticate')
        $auth.isAuthenticated()
        $mdToast.show(
          $mdToast.simple()
            .textContent('You have successfully signed in with ' + provider + '!')
            .position('top right')
            .hideDelay(3000)
        );
        $location.path('/');
      })
      .catch(function(error) {
        if (error.message) {
          // Satellizer promise reject error.
          $mdToast.show(
            $mdToast.simple()
              .textContent(error.message)
              .position('top right')
              .hideDelay(5000)
          );
        } else if (error.data) {
          // HTTP response error from server
          // toastr.error(error.data.message, error.status);
          $mdToast.show(
            $mdToast.simple()
              .textContent(error.data.message + ' - ' + error.status)
              .position('top right')
              .hideDelay(5000).toastClass('error')
          );
        } else {
          $mdToast.show(
            $mdToast.simple()
              .textContent(error)
              .position('top right')
              .hideDelay(5000)
          );
        }
      });
  };


  $scope.logout = function() {

    if (!$auth.isAuthenticated()) { return; }
    $auth.logout()
      .then(function() {
          $mdToast.show(
            $mdToast.simple()
              .textContent('You have been logged out')
              .position('top right')
              .hideDelay(3000)
          );

        // toastr.info('You have been logged out');
        $location.path('/');
      });

  }

}]);
