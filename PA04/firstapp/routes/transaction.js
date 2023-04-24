/*
  transaction.js -- Router for the Transaction
*/
const express = require('express');
const router = express.Router();
const Transaction = require('../models/Transaction')
const User = require('../models/User')


/*
this is a very simple server which maintains a key/value
store using an object where the keys and values are lists of strings

*/

isLoggedIn = (req,res,next) => {
  if (res.locals.loggedIn) {
    next()
  } else {
    res.redirect('/login')
  }
}

// get the value associated to the key
router.get('/transaction/',
  isLoggedIn,
  async (req, res, next) => {
      const show = req.query.show
      const completed = show=='completed'
      let transactions=[]
      if (show) { // show is completed or todo, so just show some transactions
        transactions = 
          await Transaction.find({userId:req.user._id, completed})
                        .sort({completed:1,amount:1,date:1})
                        .populate('category');
      }else {  // show is null, so show all of the transactions
        transactions = 
          await Transaction.find({userId:req.user._id})
                        .sort({completed:1,amount:1,date:1})
                        .populate('category');

      }
      const categories = await Category.find({userId:req.user_id}); 
      res.render('toDoList',{items,show,completed});
});



/* add the value in the body to the list associated to the key */
router.post('/transaction',
  isLoggedIn,
  async (req, res, next) => {
      const todo = new Transaction(
        {description: req.body.description,
         amount: parseFloat(req.body.amount),
         date: req.body.date,
         completed: false,
         category: req.body.category,
         userId: req.user._id
        })
      await transaction.save();
      res.redirect('/transaction')
});

router.get('/transaction/remove/:transactionId',
  isLoggedIn,
  async (req, res, next) => {
      console.log("inside /transaction/remove/:transactionId")
      await Transaction.deleteOne({_id:req.params.transactionId});
      res.redirect('/transaction')
});

router.get('/transaction/complete/:transactionId',
  isLoggedIn,
  async (req, res, next) => {
      console.log("inside /transaction/complete/:transactionId")
      await Transaction.findOneAndUpdate(
        {_id:req.params.transactionId},
        {$set: {completed:true}} );
      res.redirect('/transaction')
});

router.get('/transaction/uncomplete/:transactionId',
  isLoggedIn,
  async (req, res, next) => {
      console.log("inside /transaction/uncomplete/:transactionId")
      await Transaction.findOneAndUpdate(
        {_id:req.params.transactionId},
        {$set: {completed:false}} );
      res.redirect('/transaction')
});

router.get('/transaction/edit/:transactionId',
  isLoggedIn,
  async (req, res, next) => {
      console.log("inside /todo/edit/:transactionId")
      const transaction = 
       await Transaction.findById(req.params.transactionId);
      //res.render('edit', { item });
      res.locals.transaction = transaction
      res.render('editTransaction', {categories});
      //res.json(item)
});

router.post('/transaction/updateTransaction',
  isLoggedIn,
  async (req, res, next) => {
      const {transactionId,item,priority} = req.body;
      console.log("inside /transaction/complete/:transactionId");
      await Transaction.findOneAndUpdate(
        {_id:transactionId},
        {$set: {item,priority}} );
      res.redirect('/transaction')
});

router.get('/transaction/byUser',
  isLoggedIn,
  async (req, res, next) => {
      let results =
            await ToDoItem.aggregate(
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
        res.render('summarizeByUser',{results})
});



module.exports = router;