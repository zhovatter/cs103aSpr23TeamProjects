const mongoose = require('mongoose');
const Schema = mongoose.Schema;
const ObjectId = mongoose.Schema.Types.ObjectId;

var transactionsSchema = Schema( {
    // item: String,
    // completed: Boolean,
    // createdAt: Date,
    // priority: Number,
  
  
    description: String,
    amount: Number,
    category: String,
    date: Date,
    userId: {type:ObjectId, ref:'user' }
  } );
  
  module.exports = mongoose.model( 'Transactions', transactionsSchema );
  