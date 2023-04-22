/*
  transactions.js -- Router for the Transactions
*/
const express = require('express');
const router = express.Router();
const Transactions = require('../models/Transactions')
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
router.get('/transactions/',
  isLoggedIn,
  async (req, res, next) => {
      const show = req.query.show
      const completed = show=='completed'
      let items=[]
      if (show) { // show is completed or todo, so just show some items
        items = 
          await Transactions.find({userId:req.user._id, completed})
                        .sort({completed:1,priority:1,createdAt:1})
      }else {  // show is null, so show all of the items
        items = 
          await Transactions.find({userId:req.user._id})
                        .sort({completed:1,priority:1,createdAt:1})

      }
            res.render('transactionsList',{items,show,completed});
});



/* add the value in the body to the list associated to the key */
router.post('/transactions',
  isLoggedIn,
  async (req, res, next) => {
      const todo = new Transactions(
        {item:req.body.item,
         createdAt: new Date(),
         completed: false,
         priority: parseInt(req.body.priority),
         userId: req.user._id
        })
      await todo.save();
      res.redirect('/transactions')
});

router.get('/transactions/remove/:itemId',
  isLoggedIn,
  async (req, res, next) => {
      console.log("inside /todo/remove/:itemId")
      await Transactions.deleteOne({_id:req.params.itemId});
      res.redirect('/transactions')
});

router.get('/transactions/complete/:itemId',
  isLoggedIn,
  async (req, res, next) => {
      console.log("inside /transactions/complete/:itemId")
      await Transactions.findOneAndUpdate(
        {_id:req.params.itemId},
        {$set: {completed:true}} );
      res.redirect('/transactions')
});

router.get('/transactions/uncomplete/:itemId',
  isLoggedIn,
  async (req, res, next) => {
      console.log("inside /transactions/complete/:itemId")
      await Transactions.findOneAndUpdate(
        {_id:req.params.itemId},
        {$set: {completed:false}} );
      res.redirect('/transactions')
});

router.get('/transactions/edit/:itemId',
  isLoggedIn,
  async (req, res, next) => {
      console.log("inside /transactions/edit/:itemId")
      const item = 
       await Transactions.findById(req.params.itemId);
      //res.render('edit', { item });
      res.locals.item = item
      res.render('edit')
      //res.json(item)
});

router.post('/transactions/updateTodoItem',
  isLoggedIn,
  async (req, res, next) => {
      const {itemId,item,priority} = req.body;
      console.log("inside /transactions/complete/:itemId");
      await Transactions.findOneAndUpdate(
        {_id:itemId},
        {$set: {item,priority}} );
      res.redirect('/transactions')
});

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
        res.render('summarizeByUser',{results})
});



module.exports = router;
