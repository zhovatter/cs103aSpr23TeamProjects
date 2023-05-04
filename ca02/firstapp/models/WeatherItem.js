'use strict';
const mongoose = require( 'mongoose' );
const Schema = mongoose.Schema;
const ObjectId = mongoose.Schema.Types.ObjectId;

var weatherItemSchema = Schema( {
  address: String,
  userId: {type:ObjectId, ref:'user' }
} );

module.exports = mongoose.model( 'WeatherItem', weatherItemSchema );
