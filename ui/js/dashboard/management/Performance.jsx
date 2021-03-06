'use strict';

var _      = require('lodash');
var d3     = require('d3');
var moment = require('moment');
var React  = require('react');

var colors           = require('colors');

var Chart            = require('component/Chart.jsx');
var PieChartList     = require('component/PieChartList.jsx');

var DashboardActions = require('actions/DashboardActions');



function series(values, name) {
  return {
    name   : name,
    values : _.sortBy(values, _.result('campaign.start_date.getTime'))
  };
}

function indicatorForCampaign(campaign, indicator) {
  return d => d.campaign.id === campaign && d.indicator.id === indicator;
}

var Performance = React.createClass({

  propTypes : {
    campaign : React.PropTypes.object.isRequired,
    data     : React.PropTypes.object,
    loading  : React.PropTypes.bool
  },

  getDefaultProps : function () {
    return {
      data    : [],
      loading : false
    };
  },

  render : function () {
    var data     = this.props.data;
    var campaign = this.props.campaign;
    var upper    = moment(campaign.start_date, 'YYYY-MM-DD');
    var lower    = upper.clone().startOf('month').subtract(1, 'year');
    var loading  = this.props.loading;

    var stack = d3.layout.stack()
      .order('default')
      .offset('zero')
      .values(_.property('values'))
      .x(_.property('campaign.start_date'))
      .y(_.property('value'));

    var missed = _(data.missedChildren)
      .groupBy('indicator.short_name')
      .map(series)
      .thru(stack)
      .value();

    var missedScale = _.map(d3.time.scale()
        .domain([lower.valueOf(), upper.valueOf()])
        .ticks(d3.time.month, 1),
      _.method('getTime')
    );

    var conversions = _(data.conversions)
      .groupBy('indicator.short_name')
      .map(series)
      .value();

    var social = _.find(data.microplans, indicatorForCampaign(campaign.id, 28));
    var microplans = _.find(data.microplans, indicatorForCampaign(campaign.id, 27));

    var microplansText = function () {
      var num = _.get(social, '[0][0].value');
      var den = _.get(microplans, 'value');

      return _.isFinite(num) && _.isFinite(den) ?
        num + ' / ' + den + ' microplans incorporate social data' :
        '';
    }

    social = !_.isEmpty(social) ? [[social]] : [];

    var vaccinated = _.get(_.find(data.transitPoints, indicatorForCampaign(campaign.id, 177)), 'value');

    if (!_.isUndefined(vaccinated)) {
      var num = d3.format('n');

      vaccinated = (
        <p><strong>{num(vaccinated)}</strong> children vaccinated at transit points.</p>
      );
    } else {
      vaccinated = (<p>No vaccination data.</p>);
    }

    var planned    = _.get(_.find(data.transitPoints, indicatorForCampaign(campaign.id, 204)), 'value');
    var inPlace    = _.get(_.find(data.transitPoints, indicatorForCampaign(campaign.id, 175)), 'value');
    var withSM     = _.get(_.find(data.transitPoints, indicatorForCampaign(campaign.id, 176)), 'value');

    var transitPoints = [];
    if (!_.any([inPlace, planned], _.isUndefined)) {
      transitPoints.push([{
        title : inPlace + ' / ' + planned + ' in place',
        value : inPlace / planned
      }]);
    }

    if (!_.any([withSM, inPlace], _.isUndefined)) {
      transitPoints.push([{
        title : withSM + ' / ' + inPlace + ' have a social mobilizer',
        value : withSM / inPlace
      }]);
    }

    var pct = d3.format('%');

    var missedChildrenMap = data.missedChildrenByProvince;

    return (
      <div>
        <div className='medium-5 columns'>
          <h3>Performance of Front Line Workers</h3>
        </div>

        <div className='medium-2 columns'>
          <section>
            <h4>Missed Children</h4>
            <Chart type='ColumnChart' data={missed}
              loading={loading}
              options={{
                aspect  : 2.26,
                color   : _.flow(_.property('name'), d3.scale.ordinal().range(colors)),
                domain  : _.constant(missedScale),
                x       : d => moment(d.campaign.start_date).startOf('month').valueOf(),
                xFormat : d => moment(d).format('MMM YYYY'),
                yFormat : pct
              }} />
          </section>

          <section>
            <h4>Conversions</h4>
            <Chart type='LineChart' data={conversions}
              loading={loading}
              options={{
                aspect  : 2.26,
                domain  : _.constant([lower.toDate(), upper.toDate()]),
                yFormat : pct
              }} />
          </section>

          <section>
            <PieChartList
              loading={loading}
              keyPrefix='microplans'
              data={social}
              name={microplansText}
              emptyText='No microplan data available'
              options={{
                domain  : _.constant([0, _.get(microplans, 'value', 1)]),
                size    : 24,
                palette : colors
              }} />
          </section>
        </div>

        <section className='medium-2 columns'>
          <h4>Missed Children</h4>
          <Chart type='ChoroplethMap'
            data={missedChildrenMap}
            loading={loading}
            options={{
              domain : _.constant([0, 0.1]),
              value  : _.property('properties[475]'),
              format : d3.format('%'),
              onClick : d => { DashboardActions.navigate({ region : d }) }
            }} />
        </section>

        <section className='transit-points medium-1 column'>
          <h4>Transit Points</h4>

          {vaccinated}

          <PieChartList
            loading={loading}
            keyPrefix='transit-points'
            name={_.property('[0].title')}
            data={transitPoints}
            options={{
              domain  : _.constant([0, 1]),
              size    : 24,
              palette : colors
            }}
            emptyText='No transit point data available' />
        </section>
      </div>
    );
  },
});

module.exports = Performance;
