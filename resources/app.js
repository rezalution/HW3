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
	
	module.controller('FilterController', ['$scope', 'TaskService',
	                               function($scope,   TaskService) {
		$scope.filters = TaskService.getTaskModel();
	}]);
	
	module.controller('NavController', ['$scope', 'TaskService',
	                            function($scope,   TaskService) {
		$scope.addNewTask = function() {
			TaskService.getTaskModel().taskList.unshift(TaskService.newTask());
		};
	}]);
	
	module.controller('TaskListController', [ '$scope', 'TaskService',
	                                  function($scope,   TaskService) {
		
		$scope.filterDone = function(task) {
			return task.status !== 'Done' || TaskService.getTaskModel().showDone;
		};
		
		$scope.taskModel = TaskService.getTaskModel();
		
		$scope.updateListWithTask = function(updatedTask) {
			$scope.tasks.forEach(function(thisTask, taskIndex) {
				if (thisTask.id == updatedTask.id) {
					$scope.tasks[taskIndex] = updatedTask;
					return;
				}
			});
		};

	}]);

	module.controller('TaskRowController', ['$scope', 'TaskService', 'MeldService',
	                                function($scope,   TaskService ,  MeldService) {
		
		
		$scope.$watch('task', function(newValue, oldValue) {
			if (newValue == oldValue) { return; }
			if (!$scope.task.id) { return; }
			MeldService.meld(function() {
				$scope.task.$update();
			}, $scope.task.id, 1000);
		}, true);
		
		$scope.markDone = function() {
			$scope.task.status = "Done";
			$scope.task.$update();
		};
	}]);
	
	module.factory('TaskService', ['$http', '$resource',
	                       function($http ,  $resource) {
		
		var service = {};
		
		var Task = $resource('/api/tasks/:id',
				{id:'@id'},
				{update: {method: 'PUT'}});
		
		var taskModel = {
			taskList: Task.query()
		};
		
		service.getTaskModel = function() {
			return taskModel;
		};
		
		service.newTask = function() {
			var newTask = new Task();
			newTask.$save();
			return newTask;
		};
		return service;
	}]);


})(angular.module('concrastinate', ['ui.bootstrap', 'ngRoute', 'ngResource', 'contenteditable', 'mattwhipple.meld']));