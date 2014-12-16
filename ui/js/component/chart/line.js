'use strict';

var d3   = require('d3');
var Vue  = require('vue');

var util = require('../../util/data');

module.exports = Vue.extend({
	paramAttributes: [
		'data-lines',
		'data-areas',
		'data-width',
		'data-height'
	],

	mixins: [
		require('./yGrid'),
		require('./xAxis')
	],

	data: function () {
		return {
			lines : [],
			areas : [],
			width : 100,
			height: 100,
			x     : d3.scale.linear(),
			y     : d3.scale.linear()
		};
	},

	created: function () {
		if (!this.$options.hasOwnProperty('x')) {
			this.$options.x = d3.time.scale();
		}

		if (!this.$options.hasOwnProperty('y')) {
			this.$options.y = d3.scale.linear();
		}
	},

	methods: {
		draw: function () {
			function getX(d) { return d.x; }

			function getY(d) { return d.y; }

			function getScaledX(d) { return x(getX(d)); }

			function getScaledY(d) { return y(getY(d)); }

			function defined(d) { return util.defined(getY(d)); }

			function getPoints(d) { return d.points; }

			var self    = this;
			var svg     = d3.select(this.$el);

			var dataset = [this.lines.map(getPoints), this.areas.map(getPoints)];
			var start   = this.domain ? this.domain[0] : util.min(dataset, getX);
			var end     = this.domain ? this.domain[1] : util.max(dataset, getX);
			var lower   = Math.min(0, util.min(dataset, getY));
			var upper   = util.max(dataset, getY) * 1.1;

			var x       = this.x;
			var y       = this.y;

			x.domain([start, end])
				.range([0, this.width]);
			y.domain([lower, upper])
				.range([this.height, 0]);

			var area = d3.svg.area()
				.defined(defined)
				.x(getScaledX)
				.y(getScaledY);

			var areas = svg.selectAll('.area').data(this.areas);

			areas.enter().append('path')
				.attr('class', 'area');

			areas.attr({
				d: area
			});

			var line = d3.svg.line()
				.defined(defined)
				.x(getScaledX)
				.y(getScaledY);

			var lines = svg.selectAll('.line').data(this.lines);

			lines.enter().append('path')
				.attr('class', 'line');

			lines.attr('d', function (d) {
				return line(getPoints(d));
			})
				.style('stroke', function (d) { return d.color; });

			var hover = svg.selectAll('.hover').data(this.lines);
			hover.enter().append('g').attr('class', 'hover');

			var point = hover.selectAll('.point')
				.data(function (d) { return d.points; });

			point.enter().append('circle')
				.attr({
					'class': 'point',
					'r'    : 3,
				})
				.style('opacity', '0')
				.on('mouseover', function (d) {
					var s = getY(d);
					var attr = {
						'x'          : getScaledX(d),
						'y'          : getScaledY(d),
						'dx'         : '-4',
						'text-anchor': 'end',
						'class'      : 'hover-label'
					};

					if (self.yFmt) {
						s = self.yFmt(s);
					}

					d3.select(this)
						.style('opacity', '1');

					svg.append('text').attr(attr)
						.attr('dy', '1.1em')
						.style('opacity', '0')
						.text(s);

					var seriesData = d3.select(this.parentNode).datum();

					if (seriesData && seriesData.name) {
						svg.append('text').attr(attr)
							.attr('dy', '-.2em')
							.style('opacity', '0')
							.text(seriesData.name);
					}

					svg.selectAll('.hover-label')
						.transition().duration(300)
						.style('opacity', '1');
				})
				.on('mouseout', function () {
					d3.select(this)
						.transition().duration(300)
						.style('opacity', '0');

					svg.selectAll('.hover-label')
						.transition().duration(300)
						.style('opacity', '0')
						.remove();
				});

			point.attr({
				'cx': getScaledX,
				'cy': getScaledY
			});

			this._callHook('drawn');
		}
	},

	on: {
		'hook:attached': 'draw'
	},

	watch: {
		'lines' : 'draw',
		'areas' : 'draw',
		'width' : 'draw',
		'height': 'draw'
	}
});