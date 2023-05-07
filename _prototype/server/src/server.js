"use strict";

const fs = require("fs");
const os = require("os");

const server = require("express")();
const parser = require("body-parser");
const server_port = 60606;

//

server.use(parser.json());
server.use(parser.urlencoded({ extended: false }));

server.post("/read", (req, rep) => {
  //console.log("request: download at height: " + req.body.height);

  let messages_path = os.homedir() + "/.sws/messages.json";

  if (fs.existsSync(messages_path)) {
    let data = JSON.parse(fs.readFileSync(messages_path));
    let selected_data = [];
    let iter = 0;
    for (let item in data.messages) {
      let obj_item = data.messages[item];
      if (obj_item.height >= parseInt(req.body.height)) {
        selected_data[iter] = obj_item;
        iter++;
      }
    }
    rep.json(selected_data);
  } else {
    rep.json({"error": "no messages available"});
  }
})

server.post("/write", (req, rep) => {

  let messages_dir = os.homedir() + "/.sws/";
  let messages_path = messages_dir + "messages.json";

  if (fs.existsSync(messages_path)) {
    let data = JSON.parse(fs.readFileSync(messages_path));
    data.messages.push({"height":data.messages.length, "data":req.body.message});

    let modified_data = JSON.stringify(data);
    fs.writeFileSync(messages_path, modified_data);

  } else {
    if (!fs.existsSync(messages_dir)) {
      fs.mkdirSync(messages_dir);
    }
    let modified_data = JSON.stringify({"messages": [{"height": 0, "data":req.body.message}]});
    fs.writeFileSync(messages_path, modified_data);
  }

  rep.json({reply: req.body.message})

})

//

server.listen(server_port, () => {})
