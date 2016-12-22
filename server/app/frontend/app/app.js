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
  'angular-google-analytics']);

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
      .state('profile', {
        url: '/profile',
        templateUrl: 'partials/profile.html',
        controller: 'ProfileController',
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
      clientId: '146680675139-6fjea6lbua391tfv4hq36hl7kqo7cr96.apps.googleusercontent.com'
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
