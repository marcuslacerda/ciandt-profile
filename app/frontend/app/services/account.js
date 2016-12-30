app.factory('Account', function($http) {
  return {
    getProfile: function() {
      return $http.get('/api/users/me');
    }
  };
});