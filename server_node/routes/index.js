var express = require('express');
var router = express.Router();

/* GET home page. */
router.get('/', function(req, res, next) {
  var url = "https://picsum.photos/id/"
  var num = Math.floor(Math.random() * 600) + 1
  var num1 = Math.floor(Math.random() * 600) + 1
  var num2 = Math.floor(Math.random() * 600) + 1
  var size = "/500/500"
  var src = url + num + size
  var src1 = url + num1 + size
  var src2 = url + num2 + size
  console.log(url + num + size)
  res.render('index', { title: 'Team Ian - DDOS',
  src: src,
  src1: src1,
  src2: src2});
});

module.exports = router;
