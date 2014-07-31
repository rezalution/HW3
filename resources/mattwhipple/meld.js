//Copyright 2013 Matt Whipple

//Licensed under the Apache License, Version 2.0 (the "License");
//you may not use this file except in compliance with the License.
//You may obtain a copy of the License at

//    http://www.apache.org/licenses/LICENSE-2.0

//Unless required by applicable law or agreed to in writing, software
//distributed under the License is distributed on an "AS IS" BASIS,
//WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//See the License for the specific language governing permissions and
//limitations under the License.

(function(module) {
	
	module.factory('MeldService', ['$timeout',
	                       function($timeout) {

		var registry = {}; //registry of callbacks
		var service = {};
		
		var callWhenIdle = function(key) {
			if (new Date() - registry[key].touched >= registry[key].delay) {
				registry[key]();
				registry[key] = undefined; 
			}
			else {
				$timeout(function() {
					callWhenIdle(key);
				}, registry[key].delay / 2);
			}
		};
		
		service.meld = function(callback, key, delay) {
			if (registry[key]) {
				registry[key].touched = new Date();
			}
			else {
				callback.delay = delay;
				callback.touched = new Date();
				registry[key] = callback;
				
				$timeout(function() {
					callWhenIdle(key);
				}, delay);
			}
		};
		
		return service;
	}]);
	
})(angular.module('mattwhipple.meld', []));	
