const server = require("express")();
const parser = require("body-parser");
const server_port = 60606;

//

server.use(parser.json());
server.use(parser.urlencoded({ extended: false }));

server.post("/read", (req, rep) => {
    rep.json({reply: req.body})
})

server.post("/write", (req, rep) => {
    rep.json({reply: req.body})
})

//

server.listen(server_port, () => {})
