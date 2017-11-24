var core = require("./core.js");
var http = require('http');
var qs = require('querystring');

http.createServer(function (req, res) {

  if (req.method === 'POST') {
    var body = '';
    req.on('data', function(chunk) {
      body += chunk;
    });
    req.on('end', function() {
      var data = qs.parse(body);
      res.writeHead(200);
      var converted=core.translate(data.data,data.smartConvert);
      res.end(converted);

       console.log("raw input:"+data.data);
       console.log("converting with smartConvert="+data.smartConvert);
      console.log("send after converted"+converted+"|");
    });
  } else {
    res.writeHead(404);
    res.end();
  }

}).listen(1234);