app.controller('SearchController', ['$scope', '$http', '$auth', '$q', '$log', '$resource', '$location', '$stateParams',
  function($scope, $http, $auth, $q, $log, $resource, $location, $stateParams) {

    // TODO - mover para services
    var ProfileAPI = $resource('api/profiles/:action',
        { q : '@q' },
        {
          search : { method : 'POST', params : {action : '_search'}, isArray: true }
        }
    );

    $scope.busy = false;
    $scope.items = new Array();
    $scope.query_string = $stateParams.key;

    if ($scope.query_string != "*" && $scope.query_string != "") {
      fetchNext($scope.query_string, 0);
    }

    function fetchNext(text, from) {
      $log.info('query: ' + $scope.query_string);

      var query = {
        "from" : from, "size" : 6,
        "query": {
          "query_string": {
            "query": text + " AND status:A"
          }
        }
      }

      ProfileAPI.search(query, function(data) {
        $log.info(data.length);
        $scope.busy = false;
        angular.forEach(data, function(item, key) {
                    $scope.items.push(item);
                  });
      })
    }

    // ---- Functions --- /
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

    $scope.like = function(person) {
      $log.info(person)
      if (!person.like_count) {
        person.like_count = 1;
      } else {
        person.like_count += 1;
      }
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
      fetchNext($scope.query_string, last);
    }
  }

]);
