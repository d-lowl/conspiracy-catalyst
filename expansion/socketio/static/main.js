import { io } from "https://cdn.socket.io/4.6.1/socket.io.esm.min.js";
import {addChatMessage, addEndScreen, addReply} from "./ui.js";

const socket = io({
  autoConnect: false
});

let finished = false;
let noFollowers = 3;
let messageId = 0;
let turnsLeft = 10;

function updateFollowerCount() {
  document.getElementById("follower-counter").innerText = `followers: ${noFollowers}`
}

function updateTurnCounter() {
  document.getElementById("turns-counter").innerText = `days left: ${turnsLeft}`
}

function setWait(wait) {
  let spinner = document.getElementById("loading-spinner")
  let chat_input = document.getElementById("chat-input")
  let chat_submit = document.getElementById("chat-submit")
  spinner.hidden = !wait
  chat_input.disabled = wait || finished
  chat_submit.disabled = wait || finished
}

function initChat() {
  let chat_submit = document.getElementById("chat-submit")
  chat_submit.addEventListener("click", sayHandler)
  let chat_input = document.getElementById("chat-input")
  chat_input.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
      event.preventDefault();
      sayHandler()
    }
  })
  updateFollowerCount()
  updateTurnCounter()
}

socket.on("connect", () => {
  console.log("connect", socket.connected); // true
  initChat()
  setWait(false)
});

socket.on("turn", (dataString) => {
  let data = JSON.parse(dataString)
  document.getElementById(`msg-follower-gain-${data.message_id}`).innerText = `Followers gained: ${data.total_follower_gain}`
  noFollowers = data.followers
  updateFollowerCount()
  for (let response of data.responses) {
    addReply(response.reply, data.message_id)
  }
  if (turnsLeft === 0) {
    addEndScreen(noFollowers)
    setWait(true)
  } else {
    setWait(false)
  }
})

socket.on("error", (errorMsg) => {
  console.log(errorMsg)
})

function sayHandler() {
  let input = document.getElementById("chat-input")
  let msg = input.value
  input.value = ""
  addChatMessage("you", msg, false, messageId)
  say(msg, messageId)
  turnsLeft--;
  updateTurnCounter()
}

function say(msg, messageId) {
  setWait(true)
  socket.emit("say", JSON.stringify({
    message_id: messageId,
    message: msg
  }))
}

console.log(socket)

setWait(true)
socket.connect()
