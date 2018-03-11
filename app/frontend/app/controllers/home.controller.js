app.controller('HomeController', ['$scope', '$http', '$auth', '$q', '$log', '$resource', '$location',
  function($scope, $http, $auth, $q, $log, $resource, $location) {

      var self = this;

      self.simulateQuery = false;
      self.isDisabled    = false;

      self.querySearch   = querySearch;
      self.selectedItemChange = selectedItemChange;
      self.searchTextChange   = searchTextChange;

      var ProfileAPI = $resource('api/profiles/:action',
          { q : '@q' },
          {
            search : { method : 'POST', params : {action : '_search'}, isArray: true }
          }
      );

      /**
       * Search for repos... use $timeout to simulate
       * remote dataservice call.
       */
      function querySearch (text) {

        $log.info('querySearch ' + text);

        if (text != "" && text.length > 3) {

            var query = {
              "query": {
                "query_string": {
                  "query": text
                }
              }
            }

            return ProfileAPI.search(query).$promise;

            return items;
        } else {
          return "";
        }
      }

      $scope.isAuthenticated = function() {
        return $auth.isAuthenticated();
      };

      function keyPress(event) {
        $log.info('Goto search page ' + text);
        console.log(event.keyCode + ' - ' + event.altKey);
      }

      $scope.submitSearch = function() {
        $log.info("submit Query: " + $scope.query_string);
        $location.path('/search/' + $scope.query_string);
      }

      function searchTextChange(text) {
        $log.info('Text changed to ' + text);
      }

      function selectedItemChange(item) {
        $log.info('Item changed to ' + JSON.stringify(item));
      }
  }

]);
