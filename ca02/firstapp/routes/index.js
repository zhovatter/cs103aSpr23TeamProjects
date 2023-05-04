const express = require('express');
const router = express.Router();

router.get('/index/',
  async (req, res, next) => {
    res.render('index');
});

router.post('/index',
  async (req, res, next) => {
      res.redirect('/index')
});
module.exports = router;