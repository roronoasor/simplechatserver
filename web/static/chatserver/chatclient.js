function formatAMPM(date) {
  var date = new Date(date);
  var year = date.getFullYear();
  var month = date.getMonth();
  var day = date.getDate();
  var hours = date.getHours();
  var minutes = date.getMinutes();
  var ampm = hours >= 12 ? 'pm' : 'am';
  hours = hours % 12;
  hours = hours ? hours : 12; // the hour '0' should be '12'
  minutes = minutes < 10 ? '0'+minutes : minutes;
  var strTime = year + "/" + month + "/" + day + "  " + hours + ':' + minutes + ' ' + ampm;
  return strTime;
}

function addtolist(msg, timestamp, username, who) {

    if (username == who){
    chatDivClassName = "chat";
    }else{
    chatDivClassName = "chat chat-left";
    }

    var chatBox = document.getElementById("chats");

    var newChatDiv = document.createElement("div");
    newChatDiv.className = chatDivClassName;

    var avatarDiv = document.createElement("div");
    avatarDiv.className = "chat-avatar";
    var avatarAnchor = document.createElement("a");
    avatarAnchor.className = "avatar avatar-online";
    avatarAnchor.setAttribute("data-original-title", username);
    avatarAnchor.setAttribute("title", username);
    var avatarImg = document.createElement("img");
    avatarImg.src = "/static/chatserver/avatar-basic.svg";
    avatarAnchor.appendChild(avatarImg);
    avatarDiv.appendChild(avatarAnchor);

    var chatBodyDiv = document.createElement("div");
    chatBodyDiv.className = "chat-body";

    var chatContentDiv = document.createElement("div");
    chatContentDiv.className = "chat-content";

    var chatPTag = document.createElement("p");
    var chatMessage = document.createTextNode(msg);

    var chatTimeTag = document.createElement("time");
    chatTimeTag.className = "chat-time";
    chatTimeTag.setAttribute("datetime", timestamp)
    chatTimeTag.innerText = formatAMPM(timestamp);

    chatPTag.appendChild(chatMessage);
    chatContentDiv.appendChild(chatPTag);
    chatContentDiv.appendChild(chatTimeTag);

    chatBodyDiv.appendChild(chatContentDiv);

    newChatDiv.appendChild(avatarDiv);
    newChatDiv.appendChild(chatBodyDiv);

    chatBox.appendChild(newChatDiv);

}



const roomName = JSON.parse(document.getElementById('room-name').textContent);
const userName = JSON.parse(document.getElementById('loggedinusername').textContent);

const chatSocket = new WebSocket(
            'ws://'
            + window.location.host
            + '/ws/chat/'
            + roomName
            + '/'
        );

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
//            console.log(data);
    addtolist(data.message, data.timestamp, data.username, userName);
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
            console.error(e);
};


document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function(e) {
    console.log(e.keyCode);
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    var date = new Date();
    var isoDateString =  date.toISOString();
    chatSocket.send(JSON.stringify({
        'message': message,
        'username': userName,
        'isodatetime': isoDateString
    }));
    messageInputDom.value = '';
};