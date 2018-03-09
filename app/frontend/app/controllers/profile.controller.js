app.controller('ProfileController', function($scope, $auth, $stateParams, Account, $resource) {

    $scope.key = $stateParams.key

    console.log ('profile controller')
    console.log($scope.key)
    //
    var User = $resource('api/profiles/:login');

    var SkillAPI = $resource('api/profiles/skill/:login',
        { login : '@login' },
        {
          list : { method : 'GET', isArray: true }
        }
    );

    User.get({login:$scope.key}, function(data){
      // console.log(data)
      $scope.user = data;
    });

    //
    SkillAPI.list({login:$scope.key}, function(data) {
      console.log(data)
      $scope.skils = data;
    })


    $scope.imageProfile = function(person) {
      if (person)
        return "https://citweb.cit.com.br/ipeople/photo?cdLogin=" + person.login;
    }

    $scope.email = function(person) {
      if (person)
        return person.login + "@ciandt.com"
    }

    $scope.imageAward = function(phone) {
      return "assets/icon/" + phone + ".jpeg"
    }

  });
