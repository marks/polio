'use strict';

var _     = require('lodash');
var React = require('react');

var PolioCasesYTD = require('dashboard/management/PolioCasesYTD.jsx');
var ImmunityGap   = require('dashboard/management/ImmunityGap.jsx');

var Impact = React.createClass({

  propTypes : {
    campaign : React.PropTypes.object,
    data     : React.PropTypes.object,
    loading  : React.PropTypes.bool
  },

  getDefaultProps : function () {
    return {
      loading : false
    };
  },

  render : function () {
    var data     = this.props.data;
    var campaign = this.props.campaign;
    var loading  = this.props.loading;

    return (
      <div className='medium-2 columns'>
        <h3>Impact</h3>
        <PolioCasesYTD data={data.polioCasesYtd} campaign={campaign} loading={loading} />
        <ImmunityGap data={data.underImmunizedChildren} campaign={campaign} loading={loading} />
      </div>
    );
  },
});

module.exports = Impact;
