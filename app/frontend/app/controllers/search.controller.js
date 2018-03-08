app.controller('SearchController', ['$scope', '$http', '$auth', '$q', '$log', '$resource', '$location', '$stateParams',
  function($scope, $http, $auth, $q, $log, $resource, $location, $stateParams) {

    // TODO - mover para services
    var ProfileAPI = $resource('api/profiles/:action',
        { q : '@q' },
        {
          search : { method : 'POST', params : {action : '_search'}, isArray: true }
        }
    );

    $scope.query_string = $stateParams.key;

    if ($scope.query_string != "*" || $scope.query_string != "") {

      $log.info('query: ' + $scope.query_string);

      var query = {
        "query": {
          "query_string": {
            "query": $scope.query_string + " AND status:A"
          }
        }
      }

      ProfileAPI.search(query, function(data) {
        $scope.items =  data
      })
    }

    $scope.submitSearch = function() {
      $log.info("submit Query");
      $location.path('/search/' + $scope.query_string);
    }


    $scope.imageProfile = function(item) {
      return "https://citweb.cit.com.br/ipeople/photo?cdLogin=" + item.login;
    }

    $scope.email = function(person) {
      return person.login + "@ciandt.com"
    }

    $scope.show = function(person) {
      $location.path("/profile/" + person.login);
    }
  }

]);
