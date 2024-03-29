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
//   isLoggedIn,
//   async (req, res, next) => {
//     const transactions = await Transactions.find({ userId: req.user._id }).sort({ date: -1 });
//     res.render('transactionsList', { transactions: transactions, user: req.user });
// });
      isLoggedIn,
      async (req, res, next) => {
         // const show = req.query.show
          // const completed = show=='completed'
          let transactions=[];

          //show all of the transactions
          transactions = await Transactions.find({userId:req.user._id});//.sort({ date: -1 });
          //console.log(transactions);
          res.render('transactionsList', {transactions});
      });

/* add a transaction */
router.post('/transactions',
  isLoggedIn,
  async (req, res, next) => {
    //const{description, amount, category,  date} = req.body;
      const transaction = new Transactions(
        {description:req.body.description,
          amount: parseInt(req.body.amount),
          category: req.body.category,
          date: req.body.date,
          userId: req.user._id
        })
      await transaction.save();
      //res.render('transactionsList', {description, amount, category, date, userId: req.user._id});
      res.redirect('/transactions');
});

// delete a transaction 
router.get('/transactions/remove/:transactionsId',
  isLoggedIn,
  async (req, res, next) => {
      console.log("inside /transactions/remove/:transactionsId")
      await Transactions.deleteOne({_id:req.params.transactionsId});
      res.redirect('/transactions')
});

// updating a transaction
router.post('/transactions/update',
  isLoggedIn,
  async (req, res, next) => {
      //console.log("inside /transactions/complete/:itemId")
      const {transactionId, description, amount, category, date} = req.body;
      await Transactions.findOneAndUpdate(
        {_id:transactionId},
        {$set: {description, amount, category, date}} );
       {description, amount, category, date}
      res.redirect('/transactions')
});

// route for editing 
router.get('/transactions/edit/:transactionsId',
  isLoggedIn,
  async (req, res, next) => {
      console.log("inside /transactions/edit/:transactionsId")
      const transaction = await Transactions.findById(req.params.transactionsId);
      //res.render('transactionEdit', { transaction }); // Pass transaction data as a local variable
      // Handle any errors that occur while fetching transaction data
      //console.error(err);
      res.locals.transaction = transaction
      res.render('transactionEdit')
      //res.redirect('/transactions');
});

// may not need this part
router.get('/transactions/byCategory',
isLoggedIn,
async (req, res, next) => {
    let results =
          await Transactions.aggregate(
              [ 
                {$group:{
                  _id:'$category'
                  ,total:{$sum:'$amount'}
                  }},
                {$sort:{total:-1}},              
              ])
            
      results = 
      //use Transactions.populate!!
        //  await Transactions.populate(results,
        //          {path:'_id',
        //          select:['category','total']})

      // res.json(results)

      //use log prints to see what is being transferred!
      res.render('groupByCategory',{results})
     });



module.exports = router;