const express = require('express');
const router = express.Router();

router.get('/andy/',
  async (req, res, next) => {
    res.render('andy');
});

router.post('/andy',
  async (req, res, next) => {
      res.redirect('/andy')
});
module.exports = router;