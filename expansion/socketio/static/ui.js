export function addChatMessage(sender, message, isRight, id) {
    let msgElement = document.createElement("div")
    msgElement.className = "chat-message bordered"

    let msgTextElement = document.createElement("p")
    msgTextElement.textContent = message
    msgElement.appendChild(msgTextElement)

    msgElement.appendChild(document.createElement("hr"))
    let msgFollowerGain = document.createElement("p")
    msgFollowerGain.textContent = "Followers gained: n/a"
    msgFollowerGain.id = `msg-follower-gain-${id}`
    msgElement.appendChild(msgFollowerGain)
    msgElement.appendChild(document.createElement("hr"))

    let msgRepliesHeader = document.createElement("p")
    msgRepliesHeader.textContent = "replies:"
    msgElement.appendChild(msgRepliesHeader)

    let msgRepliesContainer = document.createElement("div")
    msgRepliesContainer.id = `replies-${id}`
    msgElement.appendChild(msgRepliesContainer)

    let chatElement = document.getElementById("chat")
    chatElement.prepend(msgElement)
}

export function addReply(message, id) {
    let msgElement = document.createElement("div")
    msgElement.className = "chat-message bordered"

    let msgTextElement = document.createElement("p")
    msgTextElement.textContent = message
    msgElement.appendChild(msgTextElement)

    let repliesContainer = document.getElementById(`replies-${id}`)
    repliesContainer.prepend(msgElement)
}

export function addEndScreen(followers) {
    let msgElement = document.createElement("div")
    msgElement.className = "chat-message bordered"

    let msgTextElement = document.createElement("p")
    msgTextElement.textContent = `Well, your account on critter seems to be blocked. But you have attracted ${followers} followers while you could! Well done!`
    msgElement.appendChild(msgTextElement)

    let chatElement = document.getElementById("chat")
    chatElement.prepend(msgElement)
}
