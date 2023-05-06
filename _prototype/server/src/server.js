"use strict";

const filesystem = require("fs");

const server = require("express")();
const parser = require("body-parser");
const server_port = 60606;

//

server.use(parser.json());
server.use(parser.urlencoded({ extended: false }));

server.post("/read", (req, rep) => {
  console.log("request: download at height: " + req.body.height);

  let data = JSON.parse(filesystem.readFileSync("fakedata.json"));
  let selected_data = {};
  let iter = 0;
  for(let item in data.messages){
    let obj_item = data.messages[item];
    if(obj_item.height >= parseInt(req.body.height)){
      selected_data[iter] = obj_item;
      iter++;
    }
  }
  rep.json(selected_data);
})

server.post("/write", (req, rep) => {
  let data = JSON.parse(filesystem.readFileSync("fakedata.json"));
  data.messages.push({"height":data.messages.length, "data":req.body.message});

  let modified_data = JSON.stringify(data);
  filesystem.writeFileSync("fakedata.json", modified_data);

  rep.json({reply: req.body.message})
})

//

server.listen(server_port, () => {})
