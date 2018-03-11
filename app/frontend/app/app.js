/**
* You must include the dependency on 'ngMaterial'
*/

var app = angular.module('StarterApp', ['ngMaterial',
  'ngMdIcons',
  'ngResource',
  'ngAnimate',
  'angular-loading-bar',
  'ui.router',
  'satellizer',
  'infinite-scroll',
  'angular-google-analytics']);

angular.module('infinite-scroll').value('THROTTLE_MILLISECONDS', 250)

app.config(['$interpolateProvider', function ($interpolateProvider) {
  $interpolateProvider.startSymbol('[[');
  $interpolateProvider.endSymbol(']]');
}]);

app.config(['AnalyticsProvider', function (AnalyticsProvider) {
   // Add configuration code as desired
   AnalyticsProvider.setAccount('UA-88644810-1');  //UU-XXXXXXX-X should be your tracking code

  // Track all routes (default is true).
  AnalyticsProvider.trackPages(true);

  // Track all URL query params (default is false).
  AnalyticsProvider.trackUrlParams(true);

  // Change the default page event name.
  // Helpful when using ui-router, which fires $stateChangeSuccess instead of $routeChangeSuccess.
  AnalyticsProvider.setPageEvent('$stateChangeSuccess');

  // RegEx to scrub location before sending to analytics.
  // Internally replaces all matching segments with an empty string.
  AnalyticsProvider.setRemoveRegExp(/\/\d+?$/);

  // Activate reading custom tracking urls from $routeProvider config (default is false)
  // This is more flexible than using RegExp and easier to maintain for multiple parameters.
  // It also reduces tracked pages to routes (only those with a templateUrl) defined in the
  // $routeProvider and therefore reduces bounce rate created by redirects.
  // NOTE: The following option requires the ngRoute module
  AnalyticsProvider.readFromRoute(true);
  // Add custom routes to the $routeProvider like this. You can also exclude certain routes from tracking by
  // adding 'doNotTrack' property


}]).run(['Analytics', function(Analytics) { }]);

app.run(function ($http) {
    $http.get('api/public/version').success(function (data) {
        console.log(data)
    });
});

app.config(function($stateProvider, $urlRouterProvider, $authProvider) {

    /**
     * Helper auth functions
     */
    var skipIfLoggedIn = ['$q', '$auth', function($q, $auth) {
      var deferred = $q.defer();
      if ($auth.isAuthenticated()) {
        deferred.reject();
      } else {
        deferred.resolve();
      }
      return deferred.promise;
    }];

    var loginRequired = ['$q', '$location', '$auth', function($q, $location, $auth) {
      var deferred = $q.defer();
      if ($auth.isAuthenticated()) {
        deferred.resolve();
      } else {
        $location.path('/login');
      }
      return deferred.promise;
    }];

    /**
     * App routes
     */
    $stateProvider
      .state('home', {
        url: '/',
        controller: 'HomeController',
        templateUrl: 'partials/home.html'
      })
      .state('login', {
        url: '/login',
        templateUrl: 'partials/login.html',
        controller: 'AuthController',
        resolve: {
          skipIfLoggedIn: skipIfLoggedIn
        }
      })
      .state('logout', {
        url: '/logout',
        template: null,
        controller: 'AuthController'
      })
      .state('me', {
        url: '/profile/me',
        templateUrl: 'partials/profile.html',
        controller: 'MeController',
        resolve: {
          loginRequired: loginRequired
        }
      })
      .state('profile', {
        url: '/profile/:key',
        templateUrl: 'partials/profile.html',
        controller: 'ProfileController',
        resolve: {
          loginRequired: loginRequired
        }
      })
      .state('ranking', {
        url: '/ranking',
        templateUrl: 'partials/ranking.html',
        controller: 'RankingController',
        resolve: {
          loginRequired: loginRequired
        }
      })
      .state('search', {
        url: '/search/:key',
        templateUrl: 'partials/search.html',
        controller: 'SearchController',
        resolve: {
          loginRequired: loginRequired
        }
      });
    $urlRouterProvider.otherwise('/');

    $authProvider.google({
      url: '/api/auth/google',
      optionalUrlParams: ['access_type', 'approval_prompt'],
      accessType: 'offline',
      approvalPrompt: 'auto',
      clientId: '538169971233-t8dacq4m7sa08j0e84vveenu6k29i1fl.apps.googleusercontent.com'
    });

});

// config theme colors

app.config(function($mdThemingProvider) {
  var customBlueMap =     $mdThemingProvider.extendPalette('light-blue', {
  'contrastDefaultColor': 'light',
  'contrastDarkColors': ['50'],
  '50': 'ffffff'
});

$mdThemingProvider.definePalette('customBlue', customBlueMap);

$mdThemingProvider.theme('default').primaryPalette('customBlue', {
  'default': '500',
  'hue-1': '50'
}).accentPalette('pink');

$mdThemingProvider.theme('input', 'default')
    .primaryPalette('grey')
});


app.directive('ngEnter', function() {
    return function(scope, element, attrs) {
        element.bind("keydown keypress", function(event) {
            if(event.which === 13) {
                console.log("key enter - exec " + attrs.ngEnter)
                scope.$apply(function(){
                    scope.$eval(attrs.ngEnter, {'event': event});
                });

                event.preventDefault();
            }
        });
    };
});

app.filter('range', function() {
  return function(input, total) {
    total = parseInt(total);
    for (var i=0; i<total; i++)
      input.push(i);
    return input;
  };
});
