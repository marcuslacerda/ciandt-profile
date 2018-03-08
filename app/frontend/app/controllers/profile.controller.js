app.controller('ProfileController', function($scope, $auth, $stateParams, Account, $resource) {

    $scope.key = $stateParams.key

    console.log ('profile controller')
    console.log($scope.key)

    var AccountAPI = $resource('api/profiles/:userId', {userId:'@id'});

    AccountAPI.get({userId:$scope.key}, function(data){
      console.log(data)
      $scope.user = data;
    });
  });
