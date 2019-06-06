
var follow_status = {active: STATUS_PUBLISHED, pending: STATUS_PENDING, delete: STATUS_DELETED, reject: STATUS_REJECTED, draft: STATUS_DRAFT};
var love_status = {active: STATUS_PUBLISHED, pending: STATUS_PENDING, delete: STATUS_DELETED, reject: STATUS_REJECTED, draft: STATUS_DRAFT};
var notification_status = {active: STATUS_PUBLISHED, pending: STATUS_PENDING, delete: STATUS_DELETED, reject: STATUS_REJECTED, draft: STATUS_DRAFT};


function getUrlVars() {
    var vars = {};
    var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi,
    function(m,key,value) {
        vars[key] = value;
    });
    return vars;
}
var topicsSearch = getUrlVars()["topics"];


var asipApp = angular.module('asipApp', ['ui.bootstrap', 'ngTouch', 'ui.utils', 'duScroll', 'ngSanitize', 'ngRoute']);
asipApp.config(function($interpolateProvider, $locationProvider, $httpProvider, $sceDelegateProvider) {
    $interpolateProvider.startSymbol('{[{');
    $interpolateProvider.endSymbol('}]}');
    // $locationProvider.html5Mode(false).hashPrefix('!');

    // $sceDelegateProvider.resourceUrlWhitelist([
    //     'self',
    //     '*://www.youtube.com/**'
    // ]);

    $httpProvider.interceptors.push('authInterceptor');
}).run(function($rootScope) {
    $rootScope.notification_status = notification_status;
    $rootScope.love_status = love_status;
    $rootScope.follow_status = follow_status;

    if (navigator.userAgent.match(/Mobi/)) {
        $('.dropdown-toggle').click();
        $('.dropdown-toggle').click();

        $('.icon-search.hidden-sm.hidden-md.hidden-lg').click();
        $('.icon-search.hidden-sm.hidden-md.hidden-lg').click();

        if (!$('.icon-search.hidden-sm.hidden-md.hidden-lg.collapsed').length) {
            $('.icon-search.hidden-sm.hidden-md.hidden-lg').click();
        }
    }

    $rootScope.new_Day = function (time) {
        if (!time) {
            return new Date();
        }
        return new Date(time)
    }

    $rootScope.Math = Math;

});

asipApp.value('duScrollOffset', 5);


asipApp.filter("sanitize", ['$sce', function ($sce) {
    return function (htmlCode) {

        return String(htmlCode);
        //return $sce.trustAsHtml(String(htmlCode));
    };
}]);

function htmlToPlainText(text, allowedTags) {
    allowedTags = allowedTags || ['p', 'br'];

    var tmp = String(text);

    // For security issues. Remove all [open_tag], [close_tag] first.
    tmp = tmp.replace(/\[open_tag\:([^\s]*?)\:(.*?)\]/gm, '');
    tmp = tmp.replace(/\[close_tag:([^\s]*?)\]/gm, '');

    allowedTags.forEach(function (tag) {
        tmp = String(tmp).replace(new RegExp('<' + tag + '([^>]*)>', 'gm'), '[open_tag:' + tag + ':$1]');
        tmp = String(tmp).replace(new RegExp('<\/' + tag + '>', 'gm'), '[close_tag:' + tag + ']');
    });

    /**
     * Fixed nested <p>
     * @see: https://stackoverflow.com/questions/12015804/nesting-p-wont-work-while-nesting-div-will
     * We can use below implement, but this can't handle the nested-nested <p>.
     * ```javascript
     * tmp = String(tmp).replace(new RegExp(/\[open_tag\:p\:(.*?)\](.|\s|\S*?)\[open_tag\:p\:/, 'gm'), '[open_tag:div:$1]$2[open_tag:p:');
     * tmp = String(tmp).replace(new RegExp(/\[close_tag\:(p|div)\](((?!\[open_tag).|(?!\[open_tag)\s|(?!\[open_tag)\S)*?)\[close_tag\:p\]/, 'gm'), '[close_tag:p]$2[close_tag:div]');
     * ```
     */
    // So let use the simpler solution, change all <p> to <div>.
    tmp = tmp.replace(/\[open_tag:p:/g, '[open_tag:div:');
    tmp = tmp.replace(/\[close_tag:p\]/g, '[close_tag:div]');

    tmp = tmp.replace(/<([^>]+)>/gm, '&lt;$1&gt;');

    tmp = tmp.replace(/\[open_tag\:([^\s]*?)\:(.*?)\]/gm, '<$1$2>');
    tmp = tmp.replace(/\[close_tag:([^\s]*?)\]/gm, '</$1>');

    return tmp;
}


asipApp.filter("nlToBr", ['$sce', function ($sce) {
    return function (htmlCode) {
        //return String(htmlCode.replace(/\n/g, "<br />"));
        return String(htmlToPlainText(htmlCode.replace(/\n/g, "<br />"), ['br']));
    };
}]);



asipApp.filter('addText', function() {
    return function(item, additionText) {

        if (!item) {
            return "";
        }

        return item + additionText;
    };
});

asipApp.filter('maxDateIn', function() {
    return function(item, field) {
        var prepare_data = [];
        for (var i = 0; i < item.length; i++) {
            prepare_data.push(new Date(item[i][field]));
        }

        var maxDate = new Date(Math.max.apply(null, prepare_data));
        return maxDate;
    };
});

asipApp.filter('dashText', function() {
    return function(item) {
        item = item || '';
        var remove_dash = item.replace(/-/g, '');
        remove_dash = remove_dash.trim();
        return remove_dash;
    };
});

asipApp.filter('timeago', function() {
    return function(date) {
        return moment(new Date(date)).fromNow();
    };
});

asipApp.filter('gender', function() {
    return function(item) {

        var gender = "";
        if (item == "M") {
            gender = 'Male';
        } else if (item == "F") {
            gender = 'Female';
        }
        return gender;
    };
});

asipApp.filter('dateFormText', ['$filter', function($filter) {
    return function(dateText, dateFormat) {
        var date = "";
        dateFormat = dateFormat || "yyyy MMMM d";

        if (dateText) {
            date = $filter('date')(dateText, dateFormat);
        }

        return date;
    };
}]);

asipApp.filter('notMatch', ['$filter', function($filter) {
    return function(inputs, filter_value, filed) {

        var output = [];

        filter_value = filter_value || -1;
        filed = filed || "id";

        angular.forEach(inputs, function (input) {

            if (input[filed] != filter_value) {
                output.push(input);
            }

        });

        return output;
    };
}]);


asipApp.filter('notMatchArray', ['$filter', function($filter) {
    return function(inputs, filter_array, field) {

        var output = [];
        var filter_index = [];

        filter_array = filter_array || [];
        field = field || "id";

        angular.forEach(inputs, function (input, index) {
            for (var i = 0; i < filter_array.length; i++) {
                
                if (input[field] == filter_array[i]) {
                    filter_index.push(index);
                }
            };
        });
        
        angular.forEach(inputs, function (input, index) {
            if (filter_index.indexOf(index) == -1) {
                output.push(input);
            }
        });

        return output;
    };
}]);

asipApp.filter('dateEvent', ['$filter', function($filter) {
    return function(date1, date2) {

        var dateFormat = "MMMM d, yyyy";
        var startDate;
        var endDate;

        /*****************************
            think as combination text 
            eg. Jan 1 - 2 Feb 2014
            this will cut to 3 part
            'Jan 1'       part 1 use startDate
            '- 2 Feb'     part 2 use endDate
            '2014'        part 3 use endDate
        ******************************/

        var dateTextPart1;
        var dateTextPart2;
        var dateTextPart3;
        
        var dateFormatPart1 = "";
        var dateFormatPart2 = "";
        var dateFormatPart3 = ", yyyy";
        
        ////////////////////////////////////////////////////////////
        // return for same date and input only one date

        if (!date2) {
            return $filter('date')(date1, dateFormat);
        } else if (!date1) {
            return $filter('date')(date2, dateFormat);
        }

        // start and end in the same day
        if (moment(date1).isSame(date2, 'day') && moment(date1).isSame(date2, 'month') && moment(date1).isSame(date2, 'year')) {
            return $filter('date')(date1, dateFormat);
        }

        ////////////////////////////////////////////////////////////

        if (date1 < date2) {
            startDate = date1;
            endDate = date2;
        } else {
            startDate = date2;
            endDate = date1;
        }

        // part 1
        if (moment(date1).isSame(date2, 'year')) {
            dateFormatPart1 = "MMMM d";
        } else {
            dateFormatPart1 = "MMMM d, yyyy";
        }

        // part 2
        if (moment(date1).isSame(date2, 'month')) {
            dateFormatPart2 = " - d";
        } else {
            dateFormatPart2 = " - MMMM d";
        }

        dateTextPart1 = $filter('date')(startDate, dateFormatPart1);
        dateTextPart2 = $filter('date')(endDate, dateFormatPart2);
        dateTextPart3 = $filter('date')(endDate, dateFormatPart3);

        var dateTextArray = [dateTextPart1, dateTextPart2, dateTextPart3];
        return dateTextArray.join('');
    }
}]);


asipApp.factory('authInterceptor', function ($q, $location) {
    return {
      // Intercept 401s and redirect you to login
      responseError: function(response) {
        if (DEBUG) {
            return $q.reject(response);
        }

        if(response.status === 404 || response.status === 403 || response.status === 401) {
          window.location = '/404';
          // remove any stale tokens
          return $q.reject(response);
        } else if (response.status === 500) {
          window.location = '/500';
          // remove any stale tokens
          return $q.reject(response);
        }
        else {
          return $q.reject(response);
        }
      }
    };
  })

asipApp.service('ScrollService', function($location, $anchorScroll) {
    this.scrollToId = function (id, offset) {
        $location.hash(id);
        $anchorScroll.yOffset = offset;
        $anchorScroll();
        $location.hash('');        
    }
});

asipApp.service('SendMailService', function() {
    this.send_mail = function(email) {
        var link = "mailto:"+ email
        window.location.href = link;
    };
});

asipApp.service('ApiService', function($http) {
    this._scope = {};

    this.request_api = function(http_type, api, params, cb) {
        cb = cb || angular.noop;
        var req = {
             method: http_type,
             url: api,
             headers: {
               'Content-Type': 'application/json;charset=UTF-8'
             },
             data: params,
        }
        $http(req).success(function(data) {
            cb(data);
        });

    };

    this.get_scope = function() {
        return this._scope;
    };

    this.get_scope_for_api = function(api) {
        return this._scope[api];
    };

    this.set_scope_for_api = function(scope, api) {
        this._scope[api] = scope;
    };

    this.refresh_api = function(api, cb) {
        cb = cb || angular.noop;
        this._scope[api].refresh(function (party_list, data) {
            cb(party_list, data);      
        });
    };

});

asipApp.service('ModalService', function($sce) {

    this.modal_scope_service = function (scope) {
        this._scope = scope;
    }

    this.open_modal_portfolio = function (party, hide_previous, hide_next, party_portfolios_id, first_portfolio) {

        var current_portfolio = $.extend(true, {}, party);

        if (this._scope) {

            this._scope.set_data(current_portfolio);
            this._scope.should_hide_previous = hide_previous;
            this._scope.should_hide_next = hide_next;

            this._scope.params[this._scope.ordering] = party.ordering;
            this._scope.params.party_portfolios = party_portfolios_id;

            this._scope.first_portfolio = first_portfolio;

            $('#portfolio-popup').modal();
        }
    }

});

asipApp.directive('followButton', function($http) {
    return {
        scope: {
            party:"=?"
        },
        restrict: 'AE',
        templateUrl: function($node, tattrs) {
            if (tattrs.template == undefined) {
                return "follow_button.html";
            } else {
                return tattrs.template;
            }
        },
        replace: true,
        link: function(scope, element, attrs) {

            scope.title = "";
            scope.party = scope.party || "";
            scope.is_loading = false;

            var follow_api = "/api/v1/party_follow_party/";
            var text_stage_normal = "Follow"
            var text_stage_highlight = "Following";
            var text_stage_highlight_hove = "Unfollow";
            var click_follow = 'click-follow';

            if (!logged_in_party) {
                scope.title = text_stage_normal;
            }

            scope.$watch('party', function(newValue) {

                if (typeof logged_in_party.id != undefined && logged_in_party != 0 && logged_in_party.id == newValue.id) {
                    element.html("").show();
                    angular.element(element.parent()).addClass('is-me');
                    return;
                }
                if (typeof newValue == 'object' && newValue.can_following && !scope.is_loading) {
                    if (!scope.party.is_following) {
                        set_normal_stage();
                    } else {
                        set_highlight_stage();
                    }
                }
            }, true);


            scope.follow = function () {

                if (logged_in_party && scope.party && !scope.is_loading) {

                    var resource_uri = scope.party.party_resource_uri;

                    if (!scope.party.is_following) {

                        angular.element(element.find('.btn')).addClass(click_follow);
                        scope.is_loading = true;

                        $http.post(follow_api, {status: follow_status.active, dst: resource_uri}).success(function(data) {

                            scope.party.total_follower++;
                            set_highlight_stage();
                            scope.is_loading = false

                        }).
                        error(function(data, status, headers, config) {
                            scope.is_loading = false;
                        });
                    } else {

                        scope.is_loading = true;

                        $http.post(follow_api, {status: follow_status.delete, dst: resource_uri}).success(function(data) {
                            
                            scope.party.total_follower--;
                            set_normal_stage();
                            scope.is_loading = false

                        }).
                        error(function(data, status, headers, config) {
                            scope.is_loading = false;
                        });
                    }

                } else {
                    $('#login-pop').click();
                }
            }

            scope.mouse_enter = function () {
                if (logged_in_party && scope.party && scope.party.is_following) {
                    scope.title = text_stage_highlight_hove;
                }
            }

            scope.mouse_leave = function () {
                
                angular.element(element.find('.btn')).removeClass(click_follow);

                if (logged_in_party && scope.party && scope.party.is_following) {
                    scope.title = text_stage_highlight;
                }
            }

            scope.is_loading_class = function () {
                return scope.is_loading ? "loading" : "";
            }

            scope.is_follow_class = function () {
                return scope.party.is_following ? "following" : "";
            }

            var set_normal_stage = function () {
                scope.title = text_stage_normal;
                scope.party.is_following = false;
            }

            var set_highlight_stage = function () {
                scope.title = text_stage_highlight;
                scope.party.is_following = true;
            }
        },
    };
});

asipApp.directive('loveButton', function($http, $rootScope) {
    return {
        scope: {
            party: "=?",
            contentType: "@"
        },
        restrict: 'AE',
        templateUrl: function($node, tattrs) {
            if (tattrs.template == undefined) {
                return "love_button.html";
            } else {
                return tattrs.template;
            }
        },
        replace: true,
        link: function(scope, element, attrs) {

            scope.title = "";
            scope.party = scope.party || "";
            scope.is_loading = false;

            var api = "/api/v1/party_love/";
            var text_stage_normal = "Love"
            var text_stage_highlight = "Loved";
            var text_stage_highlight_hove = "Unlove";
            var click_love = 'click-love';
            var content_type = scope.contentType || "party";

            if (!logged_in_party) {
                scope.title = text_stage_normal;
            }

            scope.$watch('party', function(newValue) {

                if (typeof logged_in_party.id != undefined && logged_in_party != 0 && logged_in_party.id == newValue.id) {
                    element.html("").show();
                    return;
                }

                if (typeof newValue == 'object' && newValue.can_love && !scope.is_loading) {
                    if (!scope.party.is_love) {
                        set_normal_stage();
                    } else {
                        set_highlight_stage();
                    }
                }
            }, true);


            scope.love = function () {

                if (logged_in_party && scope.party && !scope.is_loading) {

                    var resource_uri = scope.party.party_resource_uri || scope.party.resource_uri;
                    if (!scope.party.is_love) {

                        angular.element(element.find('.btn')).addClass(click_love);
                        scope.is_loading = true;

                        $http.post(api, {status: love_status.active, dst: resource_uri}).success(function(data) {

                            scope.party.total_love++;
                            set_highlight_stage();
                            scope.is_loading = false

                        }).
                        error(function(data, status, headers, config) {
                            scope.is_loading = false;
                        });
                    } else {

                        scope.is_loading = true;

                        $http.post(api, {status: love_status.delete, dst: resource_uri}).success(function(data) {

                            scope.party.total_love--;
                            set_normal_stage();
                            scope.is_loading = false

                        }).
                        error(function(data, status, headers, config) {
                            scope.is_loading = false;
                        });
                    }

                } else {
                    $('#login-pop').click();
                }
            }

            scope.modal_list = function () {

                if (scope.party.total_love > 0) {
                    $rootScope.$broadcast('modal', { modal_id: 'love-popup', url: api, params: { limit: 10 , dst_id: scope.party.id, dst_content_type__model: content_type, offset: 0 }, field_name: 'src' } );
                }

            }

            scope.mouse_enter = function () {
                if (logged_in_party && scope.party && scope.party.is_love) {
                    scope.title = text_stage_highlight_hove;
                }
            }

            scope.mouse_leave = function () {

                angular.element(element.find('.btn')).removeClass(click_love);

                if (logged_in_party && scope.party && scope.party.is_love) {
                    scope.title = text_stage_highlight;
                }
            }

            scope.is_loading_class = function () {
                return scope.is_loading ? "loading" : "";
            }

            scope.is_love_class = function () {
                return scope.party.is_love ? "loved" : "";
            }

            var set_normal_stage = function () {
                scope.title = text_stage_normal;
                scope.party.is_love = false;
            }

            var set_highlight_stage = function () {
                scope.title = text_stage_highlight;
                scope.party.is_love = true;
            }
        },
    };
});

asipApp.directive('contentItem', function ($compile, $templateCache, SendMailService) {

    var getTemplate = function(contentType, scope) {
        var template = '';

        template = $templateCache.get(contentType);

        if (!template) {
            template = $templateCache.get('template_party_profile_item_style_text.html');
        } else {
            template = $templateCache.get(contentType);
        }

        if (scope.field) {
            template = template.replace(/title/g, scope.field);
        }

        return template;
    }

    var linker = function(scope, element, attrs) {

        scope.mail_service = SendMailService;

        element.html(getTemplate(scope.template, scope)).show();
        $compile(element.contents())(scope);

        scope.$watch('content.body', function (newValue) {

            if (typeof newValue == 'undefined') {
                //skip undefind for when data "process" binding
                // need to set variable to not undefined
                return;
            }

            if (!newValue || newValue.length == 0) {

                element.html("").show();
                $compile(element.contents())(scope);

            } else {

                element.html(getTemplate(scope.template, scope)).show();
                $compile(element.contents())(scope);

            }

        }, true);

    }

    return {
        restrict: "AE",
        scope: {
            content:'=?',
            template:'@',
            field:'@'
        },
        link: linker
    };
});

asipApp.directive('emptyText', function($http) {
    return {
        restrict: 'AE',
        link: function(scope, element, attrs, controllers) {

            // watch for dd element
            scope.$watch(
                function () { return element.find('dt').length; },
                    function (newValue, oldValue) {

                      if (newValue !== oldValue) {
                        if (newValue == 0) {
                            element.append('No data')
                        }
                    }
                }
            );

        },
    };
});


asipApp.directive('twitterShare', function($http) {
    return {
        restrict: 'AE',
        link: function(scope, element, attrs, controllers) {

            element.on('click', function () {

                var width  = 575,
                    height = 400,
                    left   = ($(window).width()  - width)  / 2,
                    top    = ($(window).height() - height) / 2,
                    url    = this.href,
                    opts   = 'status=1' +
                             ',width='  + width  +
                             ',height=' + height +
                             ',top='    + top    +
                             ',left='   + left;
                
                window.open(url, 'twitter', opts);
             
                return false;

            });

        },
    };
});

asipApp.directive('facebookShare', function($http) {
    return {
        scope: {
            method: '@',
            name: '@',
            link: '@',
            picture: '@',
            caption: '@',
            description: '@',
            message: '@'
        },
        restrict: 'AE',
        link: function(scope, element, attrs, controllers) {


            element.on('click', function () {

                var base_path = location.origin;

                var method = scope.method || 'feed';
                var name = scope.name || '';
                var link = scope.link || location.href;
                var picture = scope.picture || '/static/images/favicon.png';
                var caption = scope.caption || '';
                var description = scope.description || '';
                var message = scope.message || '';

                FB.ui(
                {
                    method: method,
                    name: name,
                    link: link,
                    picture: base_path + picture,
                    caption: caption,
                    description: description,
                    message: ''
                });

            });

        },
    };
});

asipApp.directive('loadData', function($http) {
    return {
        restrict: 'AE',
        scope: {
          url: '@',
          params: '@',
          items: '=?',
          control: '=?',
        },
        link: function(scope, element, attrs, controllers) {
            scope.control = scope.control || {};
            scope.control.items = scope.items;
            scope.control.params = scope.params || {};
            // scope.control.params.limit = scope.params.limit || 20;
            // scope.control.params.offset = scope.params.offset || 0;
            scope.control.url = scope.url || '';

            scope.control.load_data = function () {
                $http.get(scope.control.url, {params: scope.control.params}).success(function(data) {

                    scope.control.meta = data.meta;

                    scope.control.items = data.objects;

                });
            }
        },
    };
});


asipApp.directive('messagePopup', function($http) {
    return {
        link: function(scope, element, attrs) {
            if (logged_in_party) {
                attrs.$set('data-target', "#modal-message");
                attrs.$set('data-toggle', "modal");
            } else {
                element.on('click', function () {
                    $('#login-pop').click();
                });
            }
        }
    };
});

asipApp.directive('messageStaffPopup', function($http) {
    return {
        link: function(scope, element, attrs) {
            if (logged_in_party) {
                attrs.$set('data-target', "#modal-staffmessage");
                attrs.$set('data-toggle', "modal");
            } else {
                element.on('click', function () {
                    $('#login-pop').click();
                });
            }
        }
    };
});



asipApp.directive('reportMyHeight', function($timeout) {

    return {
        scope: {
            height: '=?'
        },
        link: function(scope, element, attrs) {


            $timeout(init, false);

            //Initialization
            function init(){
                scope.height = element[0].offsetHeight;

            }

        }
    }

});

asipApp.directive('focusMe', function($timeout) {
  return {
    link: function(scope, element, attrs) {
      scope.$watch(attrs.focusMe, function(value) {
        if(value === true) {
          //$timeout(function() {
            element[0].focus();
            scope[attrs.focusMe] = false;
          //});
        }
      });
    }
  };
});

asipApp.controller('PostPartyDataController', function ($scope, $document, ApiService, $timeout, $rootScope) {

    $scope.api_service = ApiService;

    $scope.http_to_api_with_party = function (http_request) {

        var params = http_request.params;
        var api = http_request.api;
        var party = http_request.party;
        var send_data = http_request.data;
        var update_total = http_request.update_total;
        var model_name = http_request.model_name;
        var reload_when_done = http_request.reload_when_done;
        var hide_modal = http_request.hide_modal;
        var http_request_type = http_request.type;
        var need_update_status = http_request.update_party;
        var status = http_request.status || 'status';

        if (!$scope[model_name] && http_request_type == 'POST') {
            return;
        }

        $scope.alert = [];
        $scope.alert[model_name] = {};

        $scope.is_posting = true;

        $scope.api_service.request_api(http_request_type, api, params, function (data) {
            http_request.data = "";
            send_data = "";
            $scope.is_posting = false;

            $rootScope.$broadcast(api, 'refresh');

            $scope[model_name] = "";

            if (need_update_status) {
                party[status] = data.status;
            }
            

            if (update_total) {
                party[update_total] = data.dst[update_total];
            }

            $scope.alert[model_name].type = 'success';
            $scope.alert[model_name].show = true;
            $scope.alert[model_name].msg = 'Thank you for your ' + model_name + '.';
            /*
             Use for receive Basic controller broadcast data when they done
             */
            if (reload_when_done && typeof(reload_when_done) != 'undefined') {
                if (typeof $scope.$$listeners[api + ":data"] == 'undefined') {
                    $scope.$on(api + ":data", function (event, data) {

                        $timeout(function () {
                            // scroll to id

                            if (data.meta && data.meta.limit > 1) {
                                var element = angular.element(document.getElementById('alert_'+model_name));
                                $document.scrollToElement(element);
                            }

                        }, 1);

                    });
                }
            }
            if (hide_modal && typeof(hide_modal) != 'undefined') {
                $('#modal-'+model_name).modal('hide');
            }
            

        });
    }
});


asipApp.controller('TapViewController', function ($scope, $timeout, $location) {

    $scope.tab_index = 1;

    if ($location.hash()) {
        $timeout(function () {
            if ($('#' + $location.hash())) {
                $('#' + $location.hash()).trigger('click');
            }
        }, 1)
    }

    $scope.selected_tab = function (index) {
        $scope.tab_index = index;

        $timeout(function () {
            $('#sidebar-sticky').trigger('scroll');
            $(window).resize();
        }, 1)

    }

    $scope.tab_active_class = function (index) {
        return index == $scope.tab_index ? "active" : "hidden";
    }

    $scope.tab_list_active_class = function (index) {
        return index == $scope.tab_index ? "active" : "";
    }

});

asipApp.controller('OrganizationDetailController', function ($scope, $http, $timeout, $location, $document, $controller, $rootScope) {

    var self = this;
    $.extend(this, $controller('TapViewController', {$scope: $scope}));
    $.extend(this, $controller('PostPartyDataController', {$scope: $scope}));

    $scope.financial = 0;
    $scope.full_profile_tab_index = 1;

    if ($location.hash()) {
        $timeout(function () {
            if ($('#' + $location.hash())) {
                $('#' + $location.hash()).trigger('click');
            }
        }, 1);
    }

    $('#sidebar-sticky').scrollToFixed({
        marginTop: $('.header').outerHeight(true) + 100,
        removeOffsets: true,
        limit: function() {
            var limit = 0;
            if ($('.full-profile').length) {
                limit = $('.full-profile').offset().top + $('.full-profile').height() - $(this).outerHeight(true) - 10;
            }
            return limit;
        },
        zIndex: 999
    });

    $scope.is_not_type_support = function () {

        if (!$scope.organization) {
            return false;
        }

        return $scope.organization.type_of_organization != 'supporter';
    }

    $scope.full_profile_tab_active_class = function (index) {
        return index == $scope.full_profile_tab_index ? "active" : "hidden";
    }

    $scope.full_profile_tab_list_active_class = function (index) {
        return index == $scope.full_profile_tab_index ? "active" : "";
    }

    $scope.next_selected_full_profile_tab_class = function () {
        return $scope.full_profile_tab_index == 5 ? "hidden" : "";
    }

    $scope.previous_selected_full_profile_tab_class = function () {
        return $scope.full_profile_tab_index == 1 ? "hidden" : "";
    }

    $scope.selected_full_profile_tab = function (index) {
        $scope.full_profile_tab_index = index;
        $scope.scrollToFullProfileTab();
    }

    $scope.next_full_profile_tab = function () {
        $scope.full_profile_tab_index++;
        $scope.scrollToFullProfileTab();
    }

    $scope.previous_full_profile_tab = function () {
        $scope.full_profile_tab_index--;
        $scope.scrollToFullProfileTab();
    }

    $scope.scrollToFullProfileTab = function() {

        var element = angular.element(document.getElementById('full-profile-tab-' + $scope.full_profile_tab_index));
        $document.scrollToElementAnimated(element);

    };

    $scope.modal_love_list = function () {
        if ($scope.organization.total_love > 0) {
            $rootScope.$broadcast('modal', { modal_id: 'love-popup', url: '/api/v1/party_love/', params: { limit: 10 , dst_id: $scope.organization_id, dst_content_type__model: 'party', offset: 0 }, field_name: 'src' } );
        }
    }

    $scope.organization_id = organization_id;

    $scope.support_list = {};
    $scope.params = {};

    $http.get('/api/v1/organization/' + organization_permalink, {cache: true}).success(function(data) {

        var demo_data = 
        {
            "report_start_date" : "",
            "report_end_date" : "",
            "name_of_the_organization" : "",
            "organization_web_address" : "",
            "year_founded" : "",
            "name_of_representative" : "",
            "gender_of_representataive" : "",
            "brief_bio_of_representative" : "",
            "team_information" : "",
            "legal_structure" : "",
            "location_of_organizations_headquarters" : "",
            "phone_number_of_organizations_headquarters" : "",
            "email_of_contact_person" : "",
            "location_of_organizations_operating_facilities" : "",
            "name_of_referring_organization" : "",
            "contact_information_of_referring_organization" : "",
            "sector_activities" : "",
            "target_beneficiary" : "",
            "company_description" : "",
            "mission_statement" : "",
            "productservice_type" : "",
            "productservice_detailed_type" : "",
            "productservice_description" : "",
            "definitoin_of_unit_of_measure_1" : "",
            "unit_of_impact_measurement_1" : "",
            "definitoin_of_unit_of_measure_2" : "",
            "unit_of_impact_measurement_2" : "",
            "definitoin_of_unit_of_measure_3" : "",
            "unit_of_impact_measurement_3" : "",
            "client_type" : "",
            "client_information" : "",
            "client_locations" : "",
            "top_3_major_investors_year_and_amount" : "",
            "top_3_major_donors_year_and_amount" : "",
            "annual_revenue" : "",
            "revenue_model" : "",
            "earned_revenue" : "",
            "cost_of_goods_sold" : "",
            "gross_profit" : "",
            "personnel_expense" : "",
            "selling_general_and_administration_expense" : "",
            "operating_expense" : "",
            "ebitda" : "",
            "interest_expense" : "",
            "depreciation_and_amortization_expense" : "",
            "taxes" : "",
            "net_income_before_donations" : "",
            "contributed_revenue" : "",
            "net_income" : "",
            "current_assets" : "",
            "total_value_of_loans_and_investments" : "",
            "financial_assets" : "",
            "fixed_assets" : "",
            "total_assets" : "",
            "retained_earnings" : "",
            "accounts_payable" : "",
            "accounts_receivable" : "",
            "current_liabilities" : "",
            "financial_liabilities" : "",
            "loans_payable" : "",
            "total_liabilities" : "",
            "equity_or_net_assets" : "",
            "cash_and_cash_equivalents_period_start" : "",
            "cash_flow_from_operating_activities" : "",
            "cash_flow_from_investing_activities" : "",
            "cash_flow_from_financing_activities" : "",
            "new_investment_capital" : "",
            "net_cash_flow" : "",
            "cash_and_cash_equivalents_period_end" : "",
            "revenue_growth" : "",
            "income_growth" : "",
            "gross_margin" : "",
            "operating_profit_margin" : "",
            "working_capital" : "",
            "return_on_assets" : "",
            "return_on_equity" : "",
            "fixed_costs" : "",
            "entrepreneur_investment" : "",
            "community_service_donations" : "",
            "board_of_directors" : "",
            "female_ownership" : "",
            "financial_statement_review" : "",
            "full_time_employees" : "",
            "full_time_employees_female" : "",
            "part_time_employees" : "",
            "part_time_employees_female" : "",
            "volunteer_hours_worked" : "",
            "client_individuals" : "",
            "client_organizations" : "",
            "possible_form_of_financial_support" : "",
            "potential_size_of_investment" : "",
            "potential_use_of_investment" : "",
            "possible_form_of_non_financial_support" : "",
        }


        $scope.organization = data;
        $scope.partner_list = [];

        // demo data 
        $scope.financial_list = [];
        $scope.none_financial_list = [];
        $scope.type_of_needs_incubation= [];
        $scope.type_of_needs_networking = [];
        angular.forEach($scope.organization.type_of_needs, function(value, key) {
            var permalink_topics = value.permalink 
            if (permalink_topics == 'grant-donation' || permalink_topics == 'loan' || permalink_topics == 'equity') {
                $scope.financial_list.push(value);
            } 
            else if (permalink_topics == 'incubation') {
                $scope.type_of_needs_incubation.push(value);
            }
            else if (permalink_topics == 'networking') {
                $scope.type_of_needs_networking.push(value);
            }
            else {
                $scope.none_financial_list.push(value);
            }
        });

        angular.forEach(demo_data, function(value, key) {
            
            if (typeof $scope.organization[key] == 'undefined') {
                $scope.organization[key] = value;
            }
        });

        $scope.params = {}
        $scope.params = $scope.organization.id;


    });

    $scope.hide_self_class = function () {

        if (typeof logged_in_party.id != undefined && logged_in_party != 0 && $scope.organization && logged_in_party.id == $scope.organization.id) {
            return 'hide';
        } else {
            return '';
        }
    }

});

asipApp.controller('PeopleDetailController', function ($scope, $http, $controller, $rootScope) {

    var self = this;
    $.extend(this, $controller('TapViewController', {$scope: $scope}));
    $.extend(this, $controller('PostPartyDataController', {$scope: $scope}));

    $scope.people_id = people_id;
    $scope.params_query = params_query;

    $http.get('/api/v1/user/' + username).success(function(data) {
        $scope.people = data;
    });

    $scope.modal_love_list = function () {
        if ($scope.people.total_love > 0) {
            $rootScope.$broadcast('modal', { modal_id: 'love-popup', url: "/api/v1/party_love/", params: { limit: 10 , dst_id: $scope.people_id, dst_content_type__model: 'party', offset: 0 }, field_name: 'src' } );
        }
    }

    $scope.hide_self_class = function () {

        if (typeof logged_in_party.id != undefined && logged_in_party != 0 && $scope.people && logged_in_party.id == $scope.people.id) {
            return 'hide';
        } else {
            return '';
        }
    }

});

asipApp.controller('NewsController', function ($scope, $http) {

    var title = $('.block.block-news .block-title').text();

    $scope.current_date_format = moment(new Date()).format('YYYY-MM-DD');
});

asipApp.controller('NewsDetailController', function ($scope, $http, SendMailService) {
    
    $scope.mail_service = SendMailService;
    $scope.news_id = news_id;
    $http.get('/api/v1/news/' + $scope.news_id, { cache: true}).success(function(data) {
        $scope.news = data;
    });

});

asipApp.controller('EventController', function ($scope, $http) {

    $scope.limit = 12;


    $scope.dayClass = function (data) {

        var date = moment(data.date).format('YYYY-MM-DD');
        return ($scope.summary && $scope.summary[date])? 'has-event': '';
    };
    /*
    $http.get('/api/v1/event/summary/').success(function(data) {
        $scope.summary = data;

        $scope.today = new Date();
        $scope.maxDate = new Date();
        $scope.maxDate.setDate($scope.maxDate.getDate() + 365);
    });
    */



    $scope.current_date_format = moment(new Date()).format('YYYY-MM-DD');
    $scope.forceLoadParams = {upcommingEvent: {end_date__gte: $scope.current_date_format}};

    $scope.$watch('current_date_format', function (newValue, oldValue) {
        if (newValue !== oldValue) {

            $scope.forceLoadParams.upcommingEvent = {end_date__gte: moment(new Date($scope.current_date_format)).format('YYYY-MM-DD')};
        }
    });
});

asipApp.controller('EventCalendarController', function ($scope, $http) {
    $scope.current_date_format = moment(new Date()).format('YYYY-MM-DD');
    $scope.clear = function() {
        $scope.dt = null;
    };



});

asipApp.controller('JobDetailController', function ($scope, $http, SendMailService, ApiService) {
    var api_job = "/api/v1/job/";
    $scope.job_id = job_id;
    $http.get(api_job + $scope.job_id, { cache: true}).success(function(data) {
        $scope.job = data;
        $scope.skills = $scope.job.skills.split(',');
        $scope.organization = $scope.job.organization_jobs[0];

        var scope = jQuery.extend(true, {}, ApiService.get_scope_for_api(api_job));
        var params = jQuery.extend(true, {}, scope.params );

        params.organization_jobs =  $scope.organization.id;

        scope.set_params(api_job, {limit: 10, offset: 0, organization_jobs: $scope.organization.id});

        ApiService.set_scope_for_api(scope, api_job);
        ApiService.refresh_api(api_job);
    });

});

asipApp.controller('EventDetailController', function ($scope, $http, SendMailService) {
    
    $scope.mail_service = SendMailService;
    $scope.event_id = event_id;
    $http.get('/api/v1/event/' + $scope.event_id, { cache: true}).success(function(data) {
        $scope.event = data;
    });

});

function party_add_item_class (self, data) {
    angular.forEach(data, function (party) {
        party.number = self.data.current_number;
        self.data.current_number++;

        party.item_class = function () {

            var result = '';

            if (this.number % 4 == 0) {
                result += ' large-clear';
            }
            if (this.number % 3 == 0) {
                result += ' medium-clear';
            }
            if (this.number % 2 == 0) {
                result += ' small-clear';
            }

            return result.trim();
        };

        party.item_class_row_three = function () {

            var result = '';
            if (this.number % 3 == 0) {
                result += ' large-clear';
            }
            if (this.number % 2 == 0) {
                result += ' medium-clear';
            }
            if (this.number % 2 == 0) {
                result += ' small-clear';
            }

            return result.trim();
        };

        self.data.party_list.push(party);
    });
}

asipApp.controller('PartyListController', function ($scope, $http, $location, $timeout) {

    var hash = $location.hash();

    $scope.init = function(promote_list_config, tab_list_config, promote_ipp, tab_ipp) {

        // config
        promote_ipp = promote_ipp || 3; //
        tab_ipp = tab_ipp || 12;

        $scope.promote_list = promote_list_config;

        var promote_params = {};
        jQuery.extend(true, promote_params, promote_list_config.api.default_params, {
            limit: promote_ipp,
        });

        // Get promote party list
        $http.get(promote_list_config.api.data, {params: promote_params}).success(function(data) {
            $scope.promote_party_list = data.objects;
        });

        // Check if use tab list with api request
        $scope.tab_list = [];

        if (tab_list_config.api) {

            if (!tab_list_config.api_default['default_params']) {
                tab_list_config.api_default['default_params'] = {};
            }

            // Async
            $http.get(tab_list_config.api).success(function(data) {
                angular.forEach(data.objects, function(tab) {


                    var api_extend_default = {};
                    jQuery.extend(true, api_extend_default, tab_list_config.api_default);
                    api_extend_default['default_params'][tab_list_config.api_default.filter] = tab.id;

                    tab = {
                        'title': tab.title,
                        'api': api_extend_default
                    };

                    tab_build(tab)
                    $scope.tab_list.push(tab);
                });
                $scope.tab_list[0].active();

            });
        }
        else {
            $scope.tab_list = tab_list_config;
            angular.forEach($scope.tab_list, function(tab) {
                tab_build(tab);
            });
            $scope.tab_list[0].active();

            click_tab_from_hash();
        }

        function click_tab_from_hash () {
            if (hash) {
                $timeout(function () {
                    $('#' + hash).trigger('click');
                }, 1)
            }
        }

        function tab_build(tab) {

            // Initial data for earch tab
            tab.data = {
                'last_ordering': 9999999999,
                'is_loading': true,
                'has_more': true,
                'is_active': false,
                'page': 0,
                'party_list': [],
                'current_number': 0,
                'current_params': {}
            };

            tab.has_filter = function () {
                return typeof this.api.options != 'undefined';
            };

            tab.load_filter = function () {

                var self = this;
                if (!self.has_filter()) {
                    return false;
                }

                $http.get(self.api.options).success(function (data) {
                    self.filter_list = data.objects;

                    angular.forEach(self.filter_list, function (filter) {

                        filter.active = function () {
                            var params = {};
                            params[self.api.filter] = filter.id;
                            self.load_data(params, true);

                        };
                    });

                    self.filter_list[0].active();
                    click_tab_from_hash();
                });
            };
            // Execute now
            tab.load_filter();

            tab.load_data = function (params, reset) {

                var self = this;
                params = params || {};

                self.data.is_loading = true;

                //console.log(params);
                //console.log(this.api.default_params);
                //console.log(self.data.current_params);

                self.data.current_params = {};
                jQuery.extend(true, self.data.current_params, params, this.api.default_params, {
                    limit: tab_ipp,
                    ordering__lt: reset ? 9999999999 : this.data.last_ordering,
                    order_by: '-ordering'
                });

                if (reset) {
                    self.data.party_list = [];
                    self.data.current_number = 0;
                }

                $http.get(this.api.data, {params: self.data.current_params}).success(function (data) {

                    if (data.objects.length) {

                        party_add_item_class (self, data.objects);

                        self.data.last_ordering = data.objects[data.objects.length - 1].ordering;

                        // Know has more before next load more request
                        if (data.objects.length < tab_ipp) {
                            self.data.has_more = false;
                        }
                    }
                    else {
                        self.data.has_more = false;
                    }
                    self.data.is_loading = false;
                });
            };
            // Execute now
            if (!tab.has_filter()) {
                tab.load_data();
            }


            tab.load_more = function () {
                tab.data.page++;
                tab.load_data();
            };

            tab.active = function () {
                angular.forEach($scope.tab_list, function(tab) {
                    tab.data.is_active = false;
                });
                this.data.is_active = true;
            };

            tab.content_class = function () {
                return this.data.is_active? 'show': 'hide';
            };

            tab.tab_class = function () {
                return this.data.is_active? 'active': '';
            };

            tab.load_more_class = function () {
                return this.data.has_more? 'show': 'hide';
            };

        };


    };

});

asipApp.controller('FollowerParamController', function ($scope, FollowerService) {
    $scope.FollowerService = FollowerService;
});
asipApp.controller('BasicPartyListController', function ($scope, $http, $location, $sce, ModalService, ScrollService, FollowerService, $document, ApiService, $rootScope, $controller) {
    $.extend(this, $controller('PostPartyDataController', {$scope: $scope}));
    $scope.FollowerService = FollowerService;

    var self = this;
    var class_hide = 'hide';
    $scope.init_loading = true;
    $scope.should_show_list = false;
    $scope.pager = 0;
    $scope.url = '';
    $scope.field_name = {};
    $scope.party_list = [];
    $scope.can_load_more = true;
    $scope.last_ordering = 9999999;
    $scope.total_count = 0;
    $scope.current_page = 0;
    $scope.current_page_party_list = [];
    $scope.params = {};
    $scope.next_text = "Next";
    $scope.previous_text = "";
    $scope.first_text = "";
    $scope.last_text = "Last";
    $scope.need_ordering = true;



    var default_url = '';
    var default_params = {};
    var default_order_by = "";
    var default_field_name = {};
    var default_put_extra = "";
    var init_loading = true;
    var should_show_list = false;
    var pager = 0;
    var party_list = [];
    var can_load_more = true;
    var last_ordering = 9999999;
    var total_count = 0;
    var current_page = 0;
    var current_page_party_list = [];
    var next_text = "Next";
    var previous_text = "";
    var first_text = "";
    var last_text = "Last";
    var need_ordering = $scope.need_ordering;


    var url_parameter = get_all_url_parameter();
    if (typeof article_category !== 'undefined') {
        $scope.article_category = article_category;
    }

    angular.forEach(url_parameter, function (parameter) {
        $scope.params[parameter.key] = parameter.value;
    });
    $scope.is_unread_class = function (relation) {
        if (relation.status == 0) {
            return 'unread';
        }
    }

    $scope.set_params = function (url, params, order_by, field_name, put_extra) {
        ApiService.set_scope_for_api($scope, url);

        default_url = url;        
        default_params = $.extend(true, {}, params);
        default_order_by = order_by;
        default_field_name = field_name;
        default_put_extra = put_extra;

        $scope.meta = {};
        $scope.url = url || $scope.params.api;
        $scope.field_name = field_name;
        $scope.params.limit = params.limit || $scope.params.limit || 8;
        $scope.put_extra = put_extra;

        if ($scope.params.api) {
            delete $scope.params.api;
        }

        if ($scope.params.tab_active) {
            delete $scope.params.tab_active;
        }

        angular.forEach(params, function (value, key) {
            $scope.params[key] = value;
        });

        if ($scope.params.hasOwnProperty('need_ordering')) {
            $scope.need_ordering = $scope.params.need_ordering;
            delete $scope.params.need_ordering;
        }

        if (order_by) {
            $scope.params.order_by = order_by;

            if ($scope.params.order_by.charAt(0) == "-") {
                $scope.ordering = $scope.params.order_by.substring(1) + '__lt';
            } else {
                $scope.ordering = $scope.params.order_by + '__gt';
            }

        }

    }

    $scope.init = function(url, params, order_by, field_name, put_extra, cb, code) {

        angular.forEach(params, function (value, key) {

            if (typeof value == 'string') {
                var matchVariable = value.match(/\{\[\{(.*)?\}\]\}/);
                if (matchVariable) {
                    var variable = matchVariable[1].trim();
                    params[key] = eval(variable);
                }
            }

        });


        if (code) {
            $scope.code = code;

            $scope.$watch('forceLoadParams.' + $scope.code, function (newValue, oldValue) {
                if (newValue !== oldValue) {

                    angular.extend(default_params, newValue);
                    $scope.refresh(cb, code)
                }
            });

        }

        $scope._init(url, params, order_by, field_name, put_extra, cb, code);
    }

    $scope._init = function(url, params, order_by, field_name, put_extra, cb, code) {



        cb = cb || angular.noop;
        params = params || {};
        $scope.set_params(url, params, order_by, field_name, put_extra);

        if (url && typeof $scope.$$listeners[url] == 'undefined') {
            $scope.$on(url, function (event, data) {
                // var url = this.url;
                if (data == 'load_more') {
                    
                    $scope.load_more(function (party_list, data) {

                        $rootScope.$broadcast(url + ":data", data);
                    });

                } else if (data == 'refresh') {
                    
                    $scope.refresh(function (party_list, data) {

                        $rootScope.$broadcast(url + ":data", data);
                    });

                }
            });
        }

        $scope.load_more(function (party_list, data) {

            $scope.init_loading = false;
            if (typeof data == 'undefined') {
                data = {};
                party_list = [];
                
                $scope.no_result_text = "Please fill keyword to search.";
                $scope.no_result_text = $sce.trustAsHtml($scope.no_result_text);
                $scope.can_load_more = false;

                return cb(party_list, data);
            }

            if (data.meta && data.meta.total_count) {
                $scope.total_count = data.meta.total_count;
            }
            if (party_list.length == 0) {
                $scope.should_show_list = false;

                if ($scope.params.q) {

                    $scope.no_result_text = "Your search \"<strong class='title'>" + $scope.params.q + "</strong>\" did not match any documents.";
                } else {
                    $scope.no_result_text = "Your search did not match any documents.";
                }

                $scope.no_result_text = $sce.trustAsHtml($scope.no_result_text);
            } else {
                $scope.should_show_list = true;
            }

            cb(party_list, data);
        });
    }

    $scope.load_more = function (cb) {
        cb = cb || angular.noop;

        if (!$scope.url) {
            return cb([]);
        }

        $scope.is_loading = true;

        angular.forEach($scope.params, function (value, key) {
            if (value == 'all' || value === '') {
                delete $scope.params[key];
            }

        });
        $http.get($scope.url, {params: $scope.params, cache: false}).success(function (data) {
            $scope.is_loading = false;
            if ($scope.params.order_by) { 
                if ($scope.params.order_by.charAt(0) == "-") {
                    $scope.ordering_field = $scope.params.order_by.substring(1);
                } else {
                    $scope.ordering_field = $scope.params.order_by;
                }
            }
            // Set total followers and following
            if ($scope.params.is_followers) {
                FollowerService.total_followers = data.meta.total_count;
            }
            if ($scope.params.is_following) {
                FollowerService.total_following = data.meta.total_count;
            }

            self = this;
            self.data = {
                current_number: 0,
                party_list: []
            };

            var receive_party_list = jQuery.extend(true, {}, data.objects );
            if ($scope.field_name) {
                angular.forEach(receive_party_list, function (party, i) {
                    
                    var temp_party = $.extend(true, {}, party);
                    party = party[$scope.field_name];
                    if ($scope.put_extra) {
                        angular.forEach($scope.put_extra, function (value) {
                            party[value] = temp_party[value];
                        });
                    }

                    receive_party_list[i] = party;
                });
            }

            party_add_item_class (self, receive_party_list);

            $scope.current_page_party_list = self.data.party_list;
            $scope.party_list = $scope.party_list.concat(self.data.party_list);


            if ($scope.params.offset != null) {
                $scope.params.offset += data.objects.length;
                
                $scope.pager = Math.ceil($scope.params.offset / $scope.params.limit);
            }

            if (data.objects.length != 0) {
                $scope.last_ordering = data.objects[data.objects.length - 1][$scope.ordering_field];
            }

            if ($scope.params.order_by && $scope.need_ordering) {
                $scope.params[$scope.ordering] = $scope.last_ordering;
            }

            if (data.objects.length == 0 || data.objects.length < $scope.params.limit) {
                $scope.can_load_more = false;
            }

            if ($scope.params.page) {
                $scope.params.page++;
            }
            cb($scope.party_list, data);
        }).
        error(function(data, status, headers, config) {
            $scope.is_loading = false;
            $scope.can_load_more = false;
            cb([]);
        });
    }

    $scope.load_page = function (page, scrollToId) {

        scrollToId = scrollToId || 'main-content';

        $scope.current_page = page;
        $scope.params.offset = (page - 1) * $scope.params.limit;
        $scope.load_more(function (party_list , data) {

            var element = angular.element(document.getElementById(scrollToId));
            $document.scrollToElement(element, 0, 0);

            if (page == 1) {
                $scope.previous_text = "";
                $scope.first_text = "";
                $scope.next_text = "Next";
                $scope.last_text = "Last";
            }

            if (page > 1 && page != Math.ceil($scope.total_count / $scope.params.limit)) {
                $scope.previous_text = "Previous";
                $scope.first_text = "First";
                $scope.next_text = "Next";
                $scope.last_text = "Last";
            }

            if (page == Math.ceil($scope.total_count / $scope.params.limit)) {
                $scope.previous_text = "Previous";
                $scope.first_text = "First";
                $scope.next_text = "";
                $scope.last_text = "";
            }
        });

    }

    $scope.refresh = function (cb, code) {
        cb = cb || angular.noop;

        $scope.params = null;
        $scope.params = {};

        $scope.url = default_url;
        $scope.params = default_params;
        $scope.field_name = default_field_name;
        $scope.init_loading = init_loading;
        $scope.should_show_list = should_show_list;
        $scope.pager = pager;
        $scope.party_list = party_list;
        $scope.can_load_more = can_load_more;
        $scope.last_ordering = last_ordering;
        // $scope.total_count = total_count;
        $scope.current_page = current_page;
        // $scope.current_page_party_list = current_page_party_list;
        $scope.next_text = next_text;
        $scope.previous_text = previous_text;
        $scope.first_text = first_text;
        $scope.last_text = last_text;
        $scope.need_ordering = need_ordering;

        $scope._init(default_url, default_params, default_order_by, default_field_name, default_put_extra, function (party_list, data) {
            if ($scope.$parent && $scope.$parent.autocompletePartyList) {
                $scope.$parent.autocompletePartyList[code] = party_list;
            }
            cb(party_list, data);
        }, $scope.code);

    }

    $scope.load_more_class = function () {
        return $scope.can_load_more ? "" : class_hide ;
    }

    $scope.init_loading_class = function () {
        return $scope.init_loading ? class_hide : "";
    }

    $scope.should_show_list_class = function () {
        return (!$scope.init_loading && $scope.should_show_list) ? "" : class_hide;
    }

    $scope.open_modal_portfolio = function (party, hide_previous, hide_next) {
        var party_portfolios_id = $scope.params.party_portfolios;
        ModalService.open_modal_portfolio(party, hide_previous, hide_next, party_portfolios_id, $scope.party_list[0])
    }

});


asipApp.controller('TimerListController', function ($scope, $http, $timeout) {

    $scope.currentParty = null;

    var url, params, options;
    var itemList = [];
    var timeout;

    var offset = 0;

    $scope.isLoading = true;

    var loadPage = function (cb) {

        params.offset = offset;

        $http.get(url, {params: params}).success(function (data) {

            itemList = itemList.concat(data.objects);
            $scope.currentParty = itemList[0];

            offset = offset+params.limit;
            if (data.objects.length == 0) {
                offset = 0;
            }

            cb && cb();
            $scope.isLoading = false;

        });
    };


    $scope.startTimer = function() {

        if (itemList.length < params.limit/2) {
            loadPage()
        }

        $timeout.cancel(timeout);

        timeout = $timeout(function() {

            itemList.shift();
            $scope.currentParty = itemList[0];

            $scope.startTimer();

        }, options.duration);
    };

    $scope.stopTimer = function(){
        $timeout.cancel(timeout);
    };


    $scope.init = function (u, p, o) {

        url =u;
        params = angular.extend({limit: 20}, p);
        options = angular.extend({duration: 3000}, o);

        loadPage($scope.startTimer)
    };

});


asipApp.controller('PopupPortfolioListController', function ($scope, $http, $controller, ModalService, $sce, $timeout, $location, $element) {

    var self = this;
    var is_first_load_portfolio = true;
    $.extend(this, $controller('BasicPartyListController', {$scope: $scope}));

    $scope.modal_service = ModalService.modal_scope_service($scope);

    $scope.$watch(function() {
        return $('.portfolio-list li').length;
    }, function (newValue, oldValue) {
        if(newValue !== oldValue && newValue > 0 && is_first_load_portfolio) {
            is_first_load_portfolio = false;
            var hash = $location.hash().split('-');
            var portfolio_id = parseInt(hash[1]);

            if (hash[0] == "portfolio" && angular.isNumber(portfolio_id)) {
                portfolio_id--;
                $scope.params.ordering__gt = portfolio_id;
                $scope.params.party_portfolios = organization_id;
                $scope.params.order_by = 'ordering';

                $scope.load_more(function (party_list, data) {

                    if (party_list.length > 0) {

                        var should_hide_previous = false;
                        if (data.meta && (data.meta.next == null)) {
                            var should_hide_previous = true;
                        }
                        ModalService.open_modal_portfolio(party_list[party_list.length - 1], should_hide_previous, false, organization_id);
                    }

                });
            }

        }
    }, true);

    $scope.init_with_params = function (url, params, order_by, field_name, put_extra) {
        $scope.set_params(url, params, order_by, field_name, put_extra);
        self.order_by = $scope.params.order_by;
    }

    $scope.set_highlight_image_at_index = function (index) {
        $scope.highlight_image = $scope.current_portfolio.get_images[index];
    };

    $scope.next = function (cb) {
        cb = cb || angular.noop;
        $scope.next_ordering();
        
        $scope.load_more(function (party_list, data) {
            
            if (data.objects.length > $scope.params.limit - 1) {
                $scope.set_data(party_list[party_list.length - 1]);
                $location.hash('portfolio-' + party_list[party_list.length - 1].id);

                if (data.meta && (data.meta.next == null)) {
                    $scope.should_hide_next = true;
                }
                
                $scope.should_hide_previous = false;

            } else {
                $scope.should_hide_next = true;
            }

            if ($scope.params.order_by) {
                $scope.params[$scope.ordering] = $scope.last_ordering;
            }

        });
    }

    $scope.previous = function (cb) {
        cb = cb || angular.noop;

        $scope.previous_ordering();

        $scope.load_more(function (party_list, data) {

            if (data.objects.length > $scope.params.limit - 1) {
                $scope.set_data(party_list[party_list.length - 1]);
                $location.hash('portfolio-' + party_list[party_list.length - 1].id);

                $scope.should_hide_next = false;

                if (data.meta && (data.meta.next == null)) {
                    $scope.should_hide_previous = true;
                }


            } else {

                $scope.should_hide_previous = true;
            }

            if ($scope.params.order_by) {
                $scope.params[$scope.ordering] = $scope.last_ordering;
            }

        });
    }


    $scope.next_class = function () {
        return $scope.should_hide_next ? "hide" : "" ;
    }

    $scope.previous_class = function () {
        return $scope.should_hide_previous ? "hide" : "" ;
    }

    $scope.portfilo_link_class = function () {
        return $scope.should_hide_url ? "hide" : "" ;
    }

    $scope.previous_ordering = function () {
        
        if ($scope.params.order_by) {
            if (self.order_by.charAt(0) == "-") {
                $scope.ordering = self.order_by.substring(1) + '__gt';
                delete $scope.params[self.order_by.substring(1) + '__lt'];

                $scope.params.order_by = self.order_by.substring(1);

            } else {
                $scope.ordering = self.order_by + '__lt';
                delete $scope.params[self.order_by + '__gt'];

                $scope.params.order_by = "-" + self.order_by;
            }
            
            $scope.params[$scope.ordering] = $scope.last_ordering;

        }
    }


    $scope.next_ordering = function () {
        
        if ($scope.params.order_by) {
            if (self.order_by.charAt(0) == "-") {
                $scope.ordering = self.order_by.substring(1) + '__lt';
                delete $scope.params[self.order_by.substring(1) + '__gt'];

            } else {
                $scope.ordering = self.order_by + '__gt';
                delete $scope.params[self.order_by + '__lt'];

            }
            
            $scope.params.order_by = self.order_by;

            $scope.params[$scope.ordering] = $scope.last_ordering;

        }
    }

    $scope.set_data = function (data) {

        $scope.current_portfolio = data;

        if ($scope.current_portfolio) {
            $scope.current_portfolio.description = $sce.trustAsHtml($scope.current_portfolio.description);
            $scope.highlight_image = $scope.current_portfolio.get_images[0];

            $scope.last_ordering = $scope.current_portfolio.ordering;

            if (!$scope.current_portfolio.url || $scope.current_portfolio.url == '') {
                $scope.should_hide_url = true;
            } else {
                $scope.should_hide_url = false;
            }
        }

    }

});

asipApp.controller('PopupListController', function ($scope, $http, $controller) {

    var self = this;

    $.extend(this, $controller('BasicPartyListController', {$scope: $scope}));

    $scope.$on('modal', function (event, data) {

        $('#' + data.modal_id).modal();

        $scope.set_params(data.url, data.params, data.order_by, data.field_name, data.put_extra);
        $scope.refresh();

    });

});

asipApp.controller('TaxonomyListController', function ($scope, $http) {

    $scope.init = function(url, params) {

        $http.get(url, {params: params}).success(function (data) {
            $scope.taxonomy_list = data.objects;
            $scope.topics = topicsSearch;
        });
    }
});
asipApp.controller('SummaryController', function ($scope, $http) {

    $scope.init = function(url, params) {

        $http.get(url, {params: params}).success(function (data) {
            $scope.summary = data;
        });
    }
});

asipApp.controller('SearchFormController', function ($scope, $http) {

    $scope.tab_list = [];
    $scope.filter_list_config = {};

    var url_parameter = get_all_url_parameter();

    angular.forEach(url_parameter, function (parameter) {
        $scope[parameter.key] = parameter.value;
    });

    $scope.loading_class = function () {
        return $scope.is_loading ? "loading" : "";
    }    

    $scope.init = function(config) {
        
        $scope.tab_list = config.tab_list_config;
        $scope.filter_list_config = config.filter_list_config;

        if (!$scope['tab_active']) {
            $scope.tab_list[0].is_active = true;
        }

        var path = window.location.pathname.toLocaleLowerCase().trim().replace(/ /, "-");
        var path_array = path.split('/');

        if (window.location.pathname == "/search/" || window.location.pathname == "/job/") {
            
            $scope.is_loading = true;

            $scope.filter_api_length = 0;
            $scope.filter_api_counter = 0;

            angular.forEach($scope.tab_list, function (tab) {
                $scope.filter_api_length += tab.filters.length;
            })
        }

        function setFieldTo(array, field, data) {
            for (var i = 0; i < array.length; i++) {
                array[i][field] = data;
            };
        }

        angular.forEach($scope.tab_list, function (tab, tab_index) {
            
            tab.current_index = tab_index + 1;


            for (var j = $scope.tab_list.length - 1; j >= 0; j--) {

                var lower_case_tab_title = $scope.tab_list[j].title.toLocaleLowerCase().trim().replace(/ /, "-");

                for (var i = path_array.length - 1; i >= 0; i--) {

                    if (path_array[i] == lower_case_tab_title) {
                        setFieldTo($scope.tab_list, 'is_active', false);
                        $scope.tab_list[j].is_active = true;
                    }
                }
            }

            if ($scope['tab_active'] - 1 == tab_index) {
                tab.is_active = true;
            }

            tab.click_active = function () {
                angular.forEach($scope.tab_list, function (tab, i) {
                    tab.is_active = false;
                });
                tab.is_active = true;
            }

            tab.active_class = function () {
                return tab.is_active ? "active" : "";
            }

            angular.forEach(tab.filters, function (filter, i) {

                var filter_name = filter;

                if (typeof(filter) == 'object') {
                    filter_name = filter[0];
                    filter = filter[1];
                }

                var filter_list_name = angular.extend([], tab.filters);
                var filter_config = $scope.filter_list_config[filter];
                var params = filter_config.params || {};
                var init_filter_data = {title: filter_config.title, permalink: 'all'};
                tab.filters[i] = {};
                tab.filters[i].current_filter_data = {};
                tab.filters[i].title = filter_config.title;
                tab.filters[i].name = filter_name;
                tab.filters[i].route = filter_config.route;
                tab.filters[i].current_filter_data = init_filter_data;

                $http.get(filter_config.api, {params: params, cache: true}).success(function (data) {

                    $scope.filter_api_counter++;
                    
                    if ($scope.filter_api_counter == $scope.filter_api_length) {
                        $scope.is_loading = false;
                    }

                    var route = tab.filters[i].route || 'objects';
                    var data_list = eval("data." + route);
                    
                    var origin_data_list = [];
                    angular.forEach(data_list, function(origin_data) {
                    
                        if (!angular.isArray(origin_data)) {
                            data = origin_data;
                        } else {
                            data = {permalink: origin_data[0], title: origin_data[1]};
                        }
                        origin_data_list.push(data);
                    })

                    data_list = origin_data_list;

                    data_list.unshift(init_filter_data);

                    tab.filters[i].data = data_list;
                    

                    angular.forEach(data_list, function(data) {

                        if (tab.is_active && data.permalink == $scope[tab.filters[i].name]) {
                            tab.filters[i].title = data.title;
                            tab.filters[i].current_filter_data = data;
                        }

                        data.selected_filter = function () {
                            tab.filters[i].current_filter_data = data;
                        }
                    });
                
                });
            });
        });
    };
});


asipApp.controller('CounterController', function ($scope, $http, $timeout) {
    $scope.init = function(config) {
        angular.forEach(config, function (api, variable_name) {

            $timeout(function () {
                $http.get(api).success(function (data) {
                    $scope[variable_name] = data
                });
            }, 1000);

        });
    }
});

asipApp.controller('RequestController', function ($scope, $http, $timeout) {

    $scope.filters_choice = [];

    if (logged_in_user && logged_in_party && (logged_in_user.id == logged_in_party.id)) {
        // user
        $scope.filters_choice = ['Add people to organization', 'Message', 'Follow', 'Invite testimonial', 'Love', 'Partner'];

    } else if (logged_in_user && logged_in_party && (logged_in_user.id != logged_in_party.id)) {
        // organiz
        $scope.filters_choice = ['Message', 'Follow', 'Invite testimonial', 'Love', 'Experience'];

    }
});

asipApp.controller('FilterController', function ($scope, $location, $window, $timeout, $http) {

    var options = {
        live: true,
        successFilterCount: 0,
        single: false,
        orderByFiltersFields: [],
        extraParams: {
        }
    };


    var successFilterMap = {};
    var filterMap = {};
    var queryString = '';

    var qTimeout = null;

    $scope.init = function(o) {
        options = angular.extend(options, o);
    };

    $scope.filters=[];
    $scope.filtersMap = {}; // User in single mode

    $scope.loadAllFilter = {'success': false};

    $scope.current = {page: $location.search().page || 1};
    $scope.maxSize = 5;
    $scope.params = {};

    $scope.autocompletePartyList = {};

    $scope.current_date_format = moment(new Date()).format('YYYY-MM-DD');
    $scope.logged_in_party = logged_in_party; // Global


    $scope.initFilter = function(fieldName, filter) {

        filter = {
            permalink: fieldName + '=' + (filter.permalink || filter.name),
            title: filter.title || filter.name,
            summary: filter.summary || '',
            absolute_url: filter.absolute_url || ''
        };

        filterMap[filter.permalink] = filter;
        $scope.successFilter(fieldName);
    };

    $scope.addFilter = function(fieldName, permalink, freeform) {

        $scope[fieldName + 'FocusMe'] = true;
        $scope[fieldName + 'Value'] = '';

        filter = filterMap[fieldName + '=' + permalink];

        if (!filter && !freeform) {
            return;
        }

        if (freeform) {
            filter = {'title': permalink};
            filter['permalink'] = fieldName + '=' + permalink;
        }

        var allowAdd = true;
        angular.forEach($scope.filters, function (f, index) {
            if (filter.permalink == f.permalink) {
                allowAdd =false;
                return;
            }
        });


        if (allowAdd) {
            if (options.single || fieldName == 'q') {
                $scope.filters = $scope.filters.filter(function (obj) {
                    return obj.permalink.split('=')[0] != fieldName;
                })
                $scope.filtersMap[fieldName] = filter;
            }
            $scope.filters.push(filter);
        }

        if (fieldName == 'q') {
            if (!permalink.trim()) {
                $scope.removeFilter({permalink: 'q='});
            }
        }

        if (options.live) {
            if (fieldName == 'q') {

                $scope.liveLoading = true;

                $timeout.cancel(qTimeout);

                qTimeout = $timeout(function () {
                    $scope.submit();
                }, 1000);
            }
            else {
                $scope.submit();
            }
        }



    };

    $scope.addFilterDelay = function(fieldName, key, freeform) {

        $timeout(function () {

            var permalink = $scope;
            angular.forEach(key.split('.'), function (k) {
                permalink = permalink[k];
            });

            $scope.addFilter(fieldName, permalink, freeform);
        }, 2000)
    };

    $scope.removeFilter = function(filter) {

        var fieldName = filter.permalink.split('=')[0];

        angular.forEach($scope.filters, function (f, index) {


            var canDelete = options.single ? fieldName == f.permalink.split('=')[0]: filter.permalink == f.permalink;
            if (canDelete) {
                $scope.filters.splice(index, 1);
                delete($scope.filtersMap[fieldName]);
                return;
            }
        });

        if (options.live) {
            $scope.submit();
        }
    };

    $scope.clearFilters = function (filters) {
        $scope.filters = $scope.filters.filter(function (f) {
            var fieldName = f.permalink.split('=')[0];
            if ($.inArray( fieldName, filters) < 0) {
                return true;
            }
            else {
                delete($scope.filtersMap[fieldName]);
                return false;
            }
        });
    };

    $scope.submit = function() {

        $scope.current.page = 1;

        $scope.submitFilters = angular.copy($scope.filters);
        var params = $scope.filters.map(function (f) { return f.permalink; });

        if (params.length) {
            $location.search(params.join('&'));
        }
        else {
            history.pushState(null, null, $window.location.pathname);
        }

        $scope.liveLoading = false;

    };


    $scope.orderByObjects = function(_items, objects) {
        var items = angular.copy(_items);

        var res = [];
        angular.forEach(objects, function (obj, i) {
            angular.forEach(items, function (item, j) {
                if (obj.title == item.title) {

                    res.push(item);

                    items.splice(j, 1);

                }

            });
        });

        res = res.concat(items);


        return res;
    }

    $scope.orderByObjectsList = function (data) {

        if ((!data && !data.objects)) {
            return;
        }
        angular.forEach(data.objects, function(obj) {
            angular.forEach(options.orderByFiltersFields, function(field) {
                obj[field] = $scope.orderByObjects(obj[field], $scope.filters);
                obj[field + 'OrderFilters'] = false;
            });
        });

        if (!$scope.filters.length) {
            $timeout(function () {
                angular.forEach(data.objects, function(obj) {
                    angular.forEach(options.orderByFiltersFields, function(field) {
                        obj[field + 'OrderFilters'] = true;
                    });
                });
            }, 200)

            return;
        }

        $timeout(function () {

            angular.forEach(data.objects, function(obj) {
                angular.forEach(options.orderByFiltersFields, function(field) {
                    obj[field] = $scope.orderByObjects(obj[field], $scope.filters);
                    obj[field + 'OrderFilters'] = true;
                });
            });
        }, 200);

    };

    $scope.successFilter = function(key, force) {
        successFilterMap[key] = true;

        if (Object.keys(successFilterMap).length >= options.successFilterCount || force) {
            if (!$scope.loadAllFilter.success || force) {
                $scope.loadAllFilter.success = true;

                $timeout(function () {
                    $scope.filters = queryString.map(function (permalink) { return filterMap[permalink]; }).filter(function (v) { return v});
                    $scope.submitFilters = angular.copy($scope.filters);


                    $scope.orderByObjectsList($scope.result);

                    if (options.single) {

                        angular.forEach($scope.filters, function (filter) {
                            var fieldName = filter.permalink.split('=')[0];
                            $scope.filtersMap[fieldName] = filter;
                        });

                    }

                }, 500);
            }
        }
    };

    $scope.$watch('current.page', function (newValue, oldValue) {
        if (newValue !== oldValue) {
            $location.search('page', newValue);
        }
    });


    $scope.result = {};




    $scope.$on('$locationChangeSuccess', function(event) {


        var hash = $window.location.hash.replace('#', '');

        queryString = hash.replace('?', '').split('&').filter(String);

        $scope.loadAllFilter.locationChangeSuccess = hash;
        $scope.isLoading = true;

        var params = angular.extend({}, options.extraParams);
        params = angular.extend(params, $location.search());

        if (!params.q) {
            params.q = ''
        }

        $scope.preventQ = params.q;

        angular.extend($scope.params, params);



        $http.get(options.url, {params: params}).success(function(data) {
            $scope.orderByObjectsList(data);

            $scope.result = data;

            $scope.isLoading = false;

        }).
        error(function(data, status, headers, config) {
            $scope.isLoading = false;
        });
    });

    // autocomplete
    $scope.hideAutocompleteList = function (fieldName) {
        $scope[fieldName+'ShowTimeout'] = $timeout(function () {
            $scope[fieldName+'Show'] = false;
            $scope[fieldName+'Index'] = 0;
        }, 300);
    };

    $scope.showAutocompleteList = function (fieldName) {
        $timeout.cancel($scope[fieldName+'ShowTimeout']);
        $scope[fieldName+'Show'] = true;
        $scope[fieldName+'Index'] = 0;
    };

    $scope.isShowAutocompleteList = function (fieldName) {
        return $scope[fieldName+'Show'];
    };

    $scope.forceLoadParams = {};
    $scope.isUpdateAutocompleteListLoading = {};

    var updateAutocompleteListTimeout = null;
    $scope.updateAutocompleteList = function (fieldName) {
        $scope.isUpdateAutocompleteListLoading[fieldName] = true;

        updateAutocompleteListTimeout = $timeout(function () {

            $timeout.cancel(updateAutocompleteListTimeout);

            if (!$scope.forceLoadParams[fieldName]) {
                $scope.forceLoadParams[fieldName] = {'name__icontains': 'no-key-word-not-match-any-things', 'name__in':[]};
            }
            $scope.forceLoadParams[fieldName] = {'name__icontains': $scope[fieldName + 'Value']?$scope[fieldName + 'Value']: 'no-key-word-not-match-any-things', 'name__in':[]};
            $scope[fieldName+'Index'] = 0;

            $scope.isUpdateAutocompleteListLoading[fieldName] = false;

        }, 1000);

    };

    $scope.controlAutocompleteList = function (fieldName, event) {
        // enter
        if (event.keyCode == 13) {
            var party = $scope.autocompletePartyList[fieldName][$scope[fieldName + 'Index']];
            $scope.addFilter(fieldName, party.permalink||party.name)
        }
        // down
        else if (event.keyCode == 40) {
            $scope[fieldName+'Index'] = Math.max(Math.min($scope[fieldName+'Index']+1, $scope.autocompletePartyList[fieldName].length-1), 0);
        }
        // up
        else if (event.keyCode == 38) {
            $scope[fieldName+'Index'] = Math.max($scope[fieldName+'Index']-1, 0);;
        }
    };

    $scope.controlQ = function (event, clearFilters) {
        // enter
        if (event.keyCode == 13) {
            $scope.clearFilters(clearFilters || []);
            $scope.addFilter('q', $scope.params.q, true);
            $scope.submit();
        }
    };
});

function get_all_url_parameter()
{
    var url_parameter = [];
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++) 
    {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0]) {
            url_parameter.push({key: sParameterName[0], value : unescape(decodeURI(sParameterName[1]))});
        }
    }

    return url_parameter;
}          

asipApp.service('FollowerService', function() {

    this.total_followers = '';
    this.total_following = '';

});

