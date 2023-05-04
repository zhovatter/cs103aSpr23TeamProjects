const express = require('express');
const router = express.Router();

router.get('/christina/',
  async (req, res, next) => {
    res.render('christina');
});

router.post('/christina',
  async (req, res, next) => {
      res.redirect('/christina')
});
module.exports = router;