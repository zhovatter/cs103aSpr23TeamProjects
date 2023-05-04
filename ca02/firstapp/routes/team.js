const express = require('express');
const router = express.Router();

router.get('/team/',
  async (req, res, next) => {
    res.render('team');
});

router.post('/team',
  async (req, res, next) => {
      res.redirect('/team')
});
module.exports = router;