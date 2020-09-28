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
            header: 'Analyze your delivery'
        }
    ];

    mainCtrl.currentPage = mainCtrl.pages[0];

    mainCtrl.goToPage = function (pageId) {
        mainCtrl.currentPage = mainCtrl.pages.find(function (p) { return p.id === pageId });
    };
});

app.controller('playersController', ['$rootScope', function ($rootScope) {
    const ctrl = this;
    ctrl.players = [
        new Player({ id: 1, name: 'Virat Kohli', imageUrl: 'https://playerimages.platform.bcci.tv/generic/260x350/164.png', isCaptain: true }),
        new Player({ id: 2, name: 'Rohit Sharma', imageUrl: 'https://playerimages.platform.bcci.tv/generic/260x350/107.png' }),
        new Player({ id: 3, name: 'Ravindra Jadeja', imageUrl: 'https://playerimages.platform.bcci.tv/generic/260x350/9.png' }),
        new Player({ id: 4, name: 'Shikhar Dhawan', imageUrl: 'https://playerimages.platform.bcci.tv/generic/260x350/41.png' }),
        new Player({ id: 5, name: 'KL Rahul', imageUrl: 'https://playerimages.platform.bcci.tv/generic/260x350/1125.png' }),
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
        new Delivery({ id: 1, name: 'Delivery 1', videoUrl: 'http://techslides.com/demos/sample-videos/small.mp4' }),
        new Delivery({ id: 2, name: 'Delivery 2', videoUrl: 'http://techslides.com/demos/sample-videos/small.mp4' }),
        new Delivery({ id: 3, name: 'Delivery 3', videoUrl: 'http://techslides.com/demos/sample-videos/small.mp4' }),
        new Delivery({ id: 4, name: 'Delivery 4', videoUrl: 'http://techslides.com/demos/sample-videos/small.mp4' }),
        new Delivery({ id: 5, name: 'Delivery 5', videoUrl: 'http://techslides.com/demos/sample-videos/small.mp4' }),
        new Delivery({ id: 6, name: 'Delivery 6', videoUrl: 'http://techslides.com/demos/sample-videos/small.mp4' }),
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

app.controller('analyzeController', ['$resource', '$rootScope', function ($resource, $rootScope) {
    const ctrl = this;
    const analyzeResource = $resource('http://localhost:8080/analyse');

    analyzeResource.create({ player: $rootScope.selectedPlayer, delivery: $rootScope.selectedDelivery }).$promise.then(function(response) {
        if (response.success) {
            // Do your analysis logic here.            
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