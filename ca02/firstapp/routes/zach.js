const express = require('express');
const router = express.Router();

router.get('/zach/',
  async (req, res, next) => {
    res.render('zach');
});

router.post('/zach',
  async (req, res, next) => {
      res.redirect('/zach')
});
module.exports = router;
