'use strict';

var _  = require('lodash');
var d3 = require('d3');

var palette = require('colors');

var defaults = {
	hoverRadius : 5,
	onMouseOver : _.noop,
	onMouseOut  : _.noop,
	radius      : 3,
	x           : _.property('x'),
	xFormat     : d3.format('n'),
	xScale      : d3.scale.linear,
	y           : _.property('y'),
	yFormat     : d3.format('n'),
	yScale      : d3.scale.linear,

	margin : {
		top    : 0,
		right  : 0,
		bottom : 24,
		left   : 24
	}
}

function ScatterPlot () {}

_.extend(ScatterPlot.prototype, {
	defaults : defaults,

	update : function (data, options) {
		options    = _.assign(this._options, options);
		var margin = options.margin;

		var svg = this._svg;
		var w   = this._width - margin.left - margin.right;
		var h   = this._height - margin.top - margin.bottom;

		var domain = _.isFunction(options.domain) ?
			options.domain(data) :
			d3.extent(_.map(data, options.x));

		var xScale = options.xScale()
			.domain(domain)
			.range([0, w])
			.nice();

		var x = function (d) { return xScale(options.x(d)); }

		var range = _.isFunction(options.range) ?
			options.range(data) :
			d3.extent(_.map(data, options.y));

		var yScale = options.yScale()
			.domain(range)
			.range([h, 0])
			.nice();

		var y = function (d) { return yScale(options.y(d)); };

		var point = svg.select('.data').selectAll('.point').data(data, function (d, i) {
			return d.hasOwnProperty('id') ? d.id : i;
		});

		var attrs = {
			'cx'   : x,
			'cy'   : y,
			'r'    : options.radius
		};

		point.enter()
			.append('circle')
			.attr('class', 'point')
			.attr(attrs);

		point
			.style('cursor', _.isFunction(options.onClick) ? 'pointer' : 'default')
			.on('click', function (d, i) {
				_.get(options, 'onClick', _.noop)(d, i, this);
			})
			.on('mouseover', function (d, i) {
				d3.select(this)
					.transition()
					.duration(500)
					.ease('elastic')
					.attr('r', options.hoverRadius);

				options.onMouseOver(d, i, this);
			})
			.on('mouseout', function (d, i) {
				d3.select(this)
					.transition()
					.duration(500)
					.ease('elastic')
					.attr('r', options.radius);

				options.onMouseOut(d, i, this);
			});

		point.transition()
			.duration(300)
			.style('fill', palette[0])
			.attr(attrs);

		point.exit()
			.transition()
			.duration(300)
			.attr('r', 0)
			.remove();

		var xAxis = d3.svg.axis()
			.scale(xScale)
			.tickFormat(options.xFormat)
			.tickSize(-h)
			.tickPadding(5)
			.ticks(5)
			.orient('bottom');

		svg.select('.x.axis')
			.transition()
			.duration(300)
			.call(xAxis);

		var yAxis = d3.svg.axis()
			.scale(yScale)
			.tickFormat(options.yFormat)
			.tickSize(-w)
			.ticks(5)
			.orient('left');

		svg.select('.y.axis')
			.transition()
			.duration(300)
			.call(yAxis);
	}
});

module.exports = ScatterPlot;
