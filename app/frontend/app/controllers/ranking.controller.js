app.controller('RankingController', ['$scope', '$http', '$auth', '$q', '$log', '$resource', '$location', '$stateParams',
  function($scope, $http, $auth, $q, $log, $resource, $location, $stateParams) {

    // TODO - mover para services
    var ProfileAPI = $resource('api/profiles/:action',
        { q : '@q' },
        {
          search : { method : 'POST', params : {action : 'ranking'}, isArray: true }
        }
    );

    $scope.busy = false;
    $scope.items = new Array();

    fetchNext(0);

    function fetchNext(from) {
      $log.info('query from : ' + from);

      var query = {
        "from" : from, "size" : 12,
        "query": {"match_all": {}}
      }

      ProfileAPI.search(query, function(data) {
        $log.info(data);
        $scope.busy = false;
        angular.forEach(data, function(item, key) {
                    $scope.items.push(item);
                  });
      })
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

    $scope.loadMore = function() {
      // this is a safeguard; the callback shouldn't actually be called
      if ($scope.busy) {
        $log.info('abort loadMore')
        return;
      }
      var last = $scope.items.length;
      if (last == 0) return;
      $scope.busy = true;
      $log.info('load more = ' + last + $scope.busy);
      fetchNext(last);
    }
  }

]);
