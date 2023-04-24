'use strict';
const mongoose = require('mongoose');
const Schema = mongoose.Schema;
const ObjectId = mongoose.Schema.Types.ObjectId;

const transactionSchema = Schema({
user: { type: ObjectId, ref: 'User' },
amount: Number,
description: String,
createdAt: Date,
});

module.exports = mongoose.model('Transaction', transactionSchema);