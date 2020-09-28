const app = angular.module('cricketApp', ['ngResource']);

app.config(['$resourceProvider', function ($resourceProvider) {
    $resourceProvider.defaults.actions = {
        create: { method: 'POST' },
        get: { method: 'GET' },
        getAll: { method: 'GET', isArray: true },
        update: { method: 'PUT' },
        delete: { method: 'DELETE' }
    };
}]);

app.controller('mainController', function () {
    var mainCtrl = this;
    mainCtrl.pages = [
        {
            id: 'players',
            header: 'Select your player'
        },
        {
            id: 'deliveries',
            header: 'Select your delivery'
        },
        {
            id: 'analyze',
            header: 'Analyzing your delivery.....'
        }
    ];

    mainCtrl.currentPage = mainCtrl.pages[1];

    mainCtrl.goToPage = function (pageId) {
        mainCtrl.currentPage = mainCtrl.pages.find(function (p) { return p.id === pageId });
    };
});

app.controller('playersController', ['$rootScope', function ($rootScope) {
    const ctrl = this;
    ctrl.players = [
        new Player({ id: 1, name: 'Ayush', imageUrl: '1.png', isCaptain: true }),
        new Player({ id: 2, name: 'Vivek', imageUrl: '2.png' }),
        new Player({ id: 3, name: 'Arka', imageUrl: '3.png' }),
        new Player({ id: 4, name: 'Hari', imageUrl: '4.png' }),
        new Player({ id: 5, name: 'Pratik', imageUrl: '5.png' }),
    ];

    ctrl.selectedPlayer = $rootScope.selectedPlayer ? ctrl.players.find(function (p) { return p.id === $rootScope.selectedPlayer.id }) : null;

    ctrl.selectPlayer = function (player) {
        ctrl.selectedPlayer = player;
        $rootScope.selectedPlayer = player;
    };
}]);

app.controller('deliveriesController', ['$rootScope', function ($rootScope) {
    const ctrl = this;
    ctrl.deliveries = [
        new Delivery({ id: 1, name: 'Delivery 1', videoUrl: 'fast1.webm' }),
        new Delivery({ id: 2, name: 'Delivery 2', videoUrl: 'fast2.webm' }),
        new Delivery({ id: 3, name: 'Delivery 3', videoUrl: 'legspin1.webm' }),
        new Delivery({ id: 4, name: 'Delivery 4', videoUrl: 'legspin2.webm' }),
        new Delivery({ id: 5, name: 'Delivery 5', videoUrl: 'offspin1.webm' }),
        new Delivery({ id: 6, name: 'Delivery 6', videoUrl: 'offspin2.webm' }),
    ];

    ctrl.selectedDelivery = $rootScope.selectedDelivery ? ctrl.deliveries.find(function (d) { return d.id === $rootScope.selectedDelivery.id }) : null;

    ctrl.selectDelivery = function (delivery) {
        ctrl.selectedDelivery = delivery;
        $rootScope.selectedDelivery = delivery;
    };

    ctrl.playPreview = function (delivery) {
        if (delivery.videoUrl) {
            $('#preview-' + delivery.id).get(0).play();
        }
    };

    ctrl.stopPreview = function (delivery) {
        if (delivery.videoUrl) {
            $('#preview-' + delivery.id).get(0).pause();
        }
    };
}]);


//app.controller('analyzeController', ['$resource', '$rootScope', function ($resource, $rootScope) {
//    const ctrl = this;
//    const analyzeResource = $resource('http://localhost:8080/analyse');

//    analyzeResource.create({ player: $rootScope.selectedPlayer, delivery: $rootScope.selectedDelivery }).$promise.then(function(response) {
//        if (response.success) {
//            // Do your analysis logic here.            
//        }
//    });
//}]);


app.controller('analyzeController', ['$resource', '$rootScope', function ($resource, $rootScope) {
    const ctrl = this;
    const analyzeResource = $resource('http://localhost:8080/analyse');

    // We are posting the values of the selected player and delivery to the server.
    analyzeResource.create({ player: $rootScope.selectedPlayer, delivery: $rootScope.selectedDelivery }).$promise.then(function(response) {
        if (response.success) {
            // We are redirecting the user to the same endpoint
            window.location.href = "http://localhost:8080/analyse"
        }
    });
}]);


const Player = function (args) {
    this.id = args.id || null;
    this.name = args.name || null;
    this.imageUrl = args.imageUrl || null;
    this.isCaptain = !!args.isCaptain;
};

const Delivery = function (args) {
    this.id = args.id;
    this.name = args.name;
    this.videoUrl = args.videoUrl;
};