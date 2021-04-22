//HPRose Server
var hprose = require("hprose");

function hello(name) {
    return "Hello " + name + "!";
}

var server = hprose.Server.create("http://127.0.0.1:8080/");

server.addFunction(hello);
server.start();