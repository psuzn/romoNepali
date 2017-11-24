var core = require("./core.js");
var http = require('http');
var qs = require('querystring');

http.createServer(function (req, res) {
    req.on('end', function() {
      var data = qs.parse(body);
      res.writeHead(200);
      var converted=core.translate(data.data,data.smartConvert);
      res.end(converted);

       console.log("raw input:"+data.data);
       console.log("converting with smartConvert="+data.smartConvert);
      console.log("send after converted"+converted+"|");
    });
  

}).listen(1234);