/* global window, Promise */

'use strict';

var _        = require('lodash');
var moment   = require('moment');
var page     = require('page');
var Vue      = require('vue');

var api      = require('data/api');
var treeify  = require('data/transform/treeify');

// FIXME: simulating part of the dashboard definition that would be retrieved
// from the server
var dashboardData = [{
	'name'   : 'Polio Performance Dashboard',
	'slug'   : 'management-dashboard',
	'region' : 12907
}, {
	'name'   : 'NGA Country Office',
	'slug'   : 'nco-dashboard',
	'region' : 12907
}];

module.exports = {
	template: require('./template.html'),

	data: function () {
		return {
			region     : null,
			campaign   : null,
			dashboard  : null,

			regions    : [],
			campaigns  : [],
			dashboards : [],
		};
	},

	created: function () {
		function show(ctx) {
			self.dashboard = self._dashboardIndex[ctx.params.dashboard || 'management-dashboard'];
			self.region    = self._regionIndex[ctx.params.region];
			self.campaign  = self._campaignIndex[ctx.params.year + ctx.params.month];
		}

		var self = this;

		this._campaignIndex  = {};
		this._dashboardIndex = {};
		this._regionIndex    = {};

		page('/datapoints/:dashboard/:region/:year/:month', show);

		// FIXME: The dashboard data will eventually be stored on the server and
		// loaded dynamically
		this.dashboards = _.map(dashboardData, function (dashboard) {
			return {
				'title' : dashboard.name,
				'value' : dashboard.slug
			};
		});

		this._dashboardIndex = _.indexBy(dashboardData, 'slug');
		this.dashboard       = this._dashboardIndex['management-dashboard'];

		var regionPromise = api.regions().then(function (data) {
			var regions = _(data.objects);

			self._regionIndex = _.indexBy(data.objects, 'name');

			self.regions = regions
				.map(function (region) {
					return {
						'title'  : region.name,
						'value'  : region.name,
						'id'     : region.id,
						'parent' : region.parent_region_id
					};
				})
				.thru(_.curryRight(treeify)('id'))
				.value();

				return data;
		}, function () {
			window.alert('An error occurred loading regions from the server. Please refresh the page.');
			self.regions = [];
		});

		// FIXME: Filter campaigns by region (or maybe office?)
		var campaignPromise = api.campaign().then(function (data) {
			var campaigns = _(data.objects)
				.forEach(function (campaign) {
					campaign.start_date = moment(campaign.start_date, 'YYYY-MM-DD').toDate();
					campaign.end_date   = moment(campaign.end_date, 'YYYY-MM-DD').toDate();
				})
				.uniq(function (campaign) {
					return moment(campaign.start_date).format('YYYYMM');
				})
				.value();

			self._campaignIndex = _.indexBy(campaigns,
				function (campaign) {
					return moment(campaign.start_date).format('YYYYMM');
				});

			self.campaigns = _.map(campaigns,
				function (campaign) {
					var dt = moment(campaign.start_date);
					return {
						'title' : dt.format('MMMM YYYY'),
						'value' : dt.format('YYYYMM')
					};
				});

			return data;
		}, function () {
			window.alert('An error occurred loading campaign data from the server. Please refresh the page.');
			self.campaigns = [];
		});

		Promise.all([regionPromise, campaignPromise]).then(function (data) {
			page({ click: false });

			var dashboard, region, dt;
			if (!self.region) {
				region = _(data[0].objects)
					.filter(function (region) {
						// FIXME: this only works if the user has permissions to see country-
						// level regions
						return region.parent_region_id === null;
					})
					.sortBy('name')
					.first();
			} else {
				region = self.region;
			}

			if (!self.campaign) {
				var campaign = _(data[1].objects)
					.sortBy(function (campaign) {
						return moment(campaign.start_date).format('YYYYMMDD');
					})
					.last();

				dt = moment(campaign.start_date);
			} else {
				dt = moment(self.campaign.start_date);
			}

			if (!self.dashboard) {
				dashboard = 'management-dashboard';
			} else {
				dashboard = self.dashboard.slug;
			}

			if (dashboard && region && dt) {
				page('/datapoints/' + dashboard + '/' + region.name + '/' +
					dt.format('YYYY') + '/' +
					dt.format('MM'));
			}
		});
	},

	methods : {
		navigate : function (dashboard, region, campaign) {
			page('/datapoints/' +
				dashboard.slug + '/' +
				region.name + '/' +
				moment(campaign.start_date).format('YYYY/MM'));
		}
	},

	events: {
		'region-selected' : function (region) {
			this.navigate(
				this.dashboard,
				this._regionIndex[region],
				this.campaign);
		},

		'campaign-selected' : function (campaign) {
			this.navigate(
				this.dashboard,
				this.region,
				this._campaignIndex[campaign]);
		},

		'dashboard-selected' : function (dashboard) {
			this.navigate(
				this._dashboardIndex[dashboard],
				this.region,
				this.campaign);
		}
	},

	filters : {
		'date' : function (v, format) {
			return moment(v).format(Vue.util.stripQuotes(format));
		}
	},

	components: {
		'management-dashboard' : require('dashboard/management'),
		'nco-dashboard'        : require('dashboard/nco'),

		'chart-bar'            : require('component/chart/bar'),
		'chart-stacked-bar'    : require('component/chart/stacked-bar'),
		'chart-bullet'         : require('component/chart/bullet'),
		'chart-choropleth'     : require('component/chart/choropleth'),
		'chart-pie'            : require('component/chart/pie'),
		'chart-scatter'        : require('component/chart/scatter'),
		'chart-stacked-area'   : require('component/chart/stacked-area'),
		'chart-line'           : require('component/chart/line'),
		'chart-year-over-year' : require('component/chart/year-over-year'),
		'chart-ytd'            : require('component/chart/ytd'),
		'vue-dropdown'         : require('component/dropdown')
	},

	partials: {
		'loading-overlay': require('component/chart/partial/loading-overlay.html')
	}
};
