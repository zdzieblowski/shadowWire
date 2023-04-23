const server = require("express")()
const server_port = 60606;

//

server.post("/read", (req, rep) => {
    rep.json({reply: req})
})

server.post("/write", (req, rep) => {
    rep.json({reply: req})
})

//

server.listen(server_port, () => {})