"use strict";

import express from "express";
import asyncHandler from "express-async-handler";

import { default as fs } from "fs";
import { default as os } from "os";

import { default as bp } from "body-parser";
import { Low } from "lowdb";
import { JSONFile } from 'lowdb-node';

const server = express();
server.use(express.json());

const parser = bp;

const server_port = 60606;

//

let messages_dir = os.homedir() + "/.sws/";
let messages_path = messages_dir + "messages.json";

//

const db = new Low(new JSONFile(messages_path), {});

if (!fs.existsSync(messages_dir)){
  fs.mkdirSync(messages_dir);
}
if (!fs.existsSync(messages_path)) {
  db.data = { messages: [] };
  await db.write();
}else{
  await db.read();
}
//

server.post("/read", asyncHandler(async (req, res) => {
  await db.read();
  res.json(db.data.messages);
}),
)

server.post("/write", asyncHandler(async (req, res) => {
  db.data.messages.push({"data": req.body.message});
  await db.write();
  res.json("written");
}),
)

//

server.listen(server_port, () => {})
