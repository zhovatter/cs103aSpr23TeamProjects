/*
  transactions.js -- Router for the Transactions
*/
const express = require('express');
const router = express.Router();
const Transactions = require('../models/Transactions');
const User = require('../models/User')


/*
this is a very simple server which maintains a key/value
store using an object where the keys and values are lists of strings

*/

// Checking if user is logged in 
isLoggedIn = (req,res,next) => {
  if (res.locals.loggedIn) {
    next()
  } else {
    res.redirect('/login')
  }
}

// get the value associated to the key
router.get('/transactions/',
  isLoggedIn,
  async (req, res, next) => {
    const transactions = await Transactions.find({ userId: req.user._id }).sort({ date: -1 });
    res.render('transactionsList', { transactions: transactions, user: req.user });
});

/* add a transaction */
router.post('/transactions/add',
  isLoggedIn,
  async (req, res, next) => {
    const{description, 
      amount, 
      category, 
      date} = req.body;
      const transaction = new Transactions(
        {description,
          amount,
          category,
          date,
          userId: req.user._id
        })
      await transaction.save();
      res.render('transactionsList', {description, amount, category, date, userId: req.user._id});
      res.redirect('/transactions');
});

// delete a transaction 
router.get('/transactions/remove/:transactionsId',
  isLoggedIn,
  async (req, res, next) => {
      await Transactions.deleteOne({_id:req.params.transactionsId});
      res.redirect('/transactions');
});

// updating a transaction
router.get('/transactions/update',
  isLoggedIn,
  async (req, res, next) => {
      //console.log("inside /transactions/complete/:itemId")
      const {transactionId, description, amount, category, date} = req.body;
      await Transactions.findOneAndUpdate(
        {_id:req.params.transactionsId},
        // {$set: {completed:false}} 
        {description, amount, category, date}
        );
      res.redirect('/transactions')
});

// route for editing 
router.get('/transactions/edit/:transactionsId',
  isLoggedIn,
  async (req, res, next) => {
    try {
      const transaction = await Transactions.findById(req.params.transactionsId);
      res.render('transactionEdit', { transaction }); // Pass transaction data as a local variable
    } catch (err) {
      // Handle any errors that occur while fetching transaction data
      console.error(err);
      res.redirect('/transactions');
    }
});

// may not need this part
router.get('/transactions/byUser',
  isLoggedIn,
  async (req, res, next) => {
      let results =
            await Transactions.aggregate(
                [ 
                  {$group:{
                    _id:'$userId',
                    total:{$count:{}}
                    }},
                  {$sort:{total:-1}},              
                ])
              
        results = 
           await User.populate(results,
                   {path:'_id',
                   select:['username','age']})

        //res.json(results)
        res.render('transactionsList',{results})
});



module.exports = router;