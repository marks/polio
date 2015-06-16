'use strict';

var _      = require('lodash');
var Reflux = require('reflux/src');
var moment = require('moment');

var api = require('data/api');

var DataActions = require('actions/DataActions');

function melt (d) {
	var base = _.omit(d, 'indicators');

	return _.map(d.indicators, function (i) {
		return _.assign({
				indicator : i.indicator,
				value     : i.value
			}, base);
	});
}

var DataStore = Reflux.createStore({

	listenables : [DataActions],

	init : function () {
		this.loading = false;
		this.data    = [];
	},

	getInitialState : function () {
		return {
			loading : this.loading,
			data    : this.data
		};
	},

	onClear : function () {
		this.loading = false;
		this.data    = [];

		this.trigger({
			loading : false,
			data    : []
		});
	},

	onFetch : function (campaign, region, indicators) {
		var m     = moment(campaign.start_date, 'YYYY-MM-DD');
		var end   = campaign.end_date;

		var promises = _.map(indicators, function (def) {
			var q = {
				indicator__in  : def.indicators,
				campaign_start : m.clone().startOf(def.startOf).subtract(def.duration).format('YYYY-MM-DD'),
				campaign_end   : end
			};

			switch (def.region) {
				case 'subregions':
					q.parent_region__in = region.id;
					break;
				default:
					q.region__in = region.id;
					break;
			}

			return api.datapoints(q);
		});

		Promise.all(promises).then(function (responses) {
			this.data = _(responses)
				.pluck('objects')
				.flatten()
				.map(melt)
				.flatten()
				.value();

			this.loading = false;

			this.trigger({
				loading : false,
				data    : this.data
			});
		}.bind(this));

		this.loading = true;
		this.data    = [];

		this.trigger({
			loading : true,
			data    : []
		});
	}

});

module.exports = DataStore;