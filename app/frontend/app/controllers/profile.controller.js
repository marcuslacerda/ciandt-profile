app.controller('ProfileController', function($scope, $auth, $stateParams, Account, $resource) {

    $scope.key = $stateParams.key

    console.log ('profile controller')
    console.log($scope.key)
    //
    var User = $resource('api/profiles/:login');

    var ProfileAPI = $resource('api/profiles/:action/:login',
        { login : '@login' },
        {
          skillList : { method : 'GET', params : {action : 'skill'}, isArray: true },
          stackList : { method : 'GET', params : {action : 'stack'}, isArray: true },
          strength : { method : 'GET', params : {action : 'strength'}}
        }
    );

    User.get({login:$scope.key}, function(data){
      $scope.user = data;
    });

    ProfileAPI.skillList({login:$scope.key}, function(data) {
      $scope.skills = data;
    })

    ProfileAPI.stackList({login:$scope.key}, function(data) {
      $scope.stacks = data;
    })

    ProfileAPI.strength({login:$scope.key}, function(data) {
      console.log('return strentgh profile')
      console.log(data)
      $scope.strength = data;
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

    $scope.tops = function(skill) {
      return (skill['skillLevel'] >= 3 && skill.endorsementsCount > 0)
    }

  });
