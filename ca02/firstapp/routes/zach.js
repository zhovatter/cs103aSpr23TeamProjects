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

const axios = require('axios')
router.post('/zach/openai',
async (req,res,next) => {
res.locals.prompt = req.body.prompt
    //res.locals.weather = await get_weather(req.body.address)
response =
await axios.post('http://gracehopper.cs-i.brandeis.edu:3500/openai',
{prompt:"Generate a poem about " + req.body.prompt})
res.json(response.data.choices[0].message.content)
})

// const axios = require('axios')
// router.get('/zach/openai',
// async (req,res,next) => {
// response =
// await axios.post('http://gracehopper.cs-i.brandeis.edu:3500/openai',
// {prompt:"how does the flu differ from covid?"})
// res.json(response.data.choices[0].message.content)
// })


module.exports = router;
