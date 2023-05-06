const express = require('express');
const router = express.Router();

router.get('/christina/',
  async (req, res, next) => {
    res.render('christina');
});

const axios = require('axios')
router.post('/christina/openai',
async (req,res,next) => {
res.locals.promot = req.body.prompt
response =
await axios.post('http://gracehopper.cs-i.brandeis.edu:3500/openai',
{prompt:"Generate a joke about" + req.body.prompt})
res.json(response.data.choices[0].message.content)
})

router.post('/christina',
  async (req, res, next) => {
      res.redirect('/christina')
});
module.exports = router;