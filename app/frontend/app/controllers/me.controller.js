app.controller('MeController', function($scope, $auth, Account) {

    $scope.getProfile = function() {
      Account.getProfile()
        .then(function(response) {
          console.log(response.data)
          $scope.user = response.data;
        })
        .catch(function(response) {
          console.log('ERROR')
          console.log(response)
        });
    };

    $scope.getProfile();
  });
