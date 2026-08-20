const messageInput =
    document.getElementById(
        "message-input"
    );

const sendButton =
    document.getElementById(
        "send-btn"
    );

const newChatButton =
    document.getElementById(
        "new-chat-btn"
    );

const messagesContainer =
    document.getElementById(
        "messages"
    );

const welcomeScreen =
    document.getElementById(
        "welcome-screen"
    );

const conversationTitle =
    document.getElementById(
        "conversation-title"
    );


/* ================================= */
/* NEW CHAT */
/* ================================= */

newChatButton.addEventListener(
    "click",
    () => {

        clearChat();

        conversationTitle.textContent =
            "New conversation";

        messageInput.focus();

    }
);


/* ================================= */
/* SEND MESSAGE */
/* ================================= */

sendButton.addEventListener(
    "click",
    sendMessage
);


messageInput.addEventListener(
    "keydown",
    function(event) {

        if (
            event.key === "Enter" &&
            !event.shiftKey
        ) {

            event.preventDefault();

            sendMessage();

        }

    }
);


async function sendMessage() {

    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    addMessage("user", message);

    messageInput.value = "";

    showTyping();

    sendButton.disabled = true;

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/api/v1/chat",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    message: message
                })
            }
        );

        if (!response.ok) {
            throw new Error(
                `HTTP error: ${response.status}`
            );
        }

        const data = await response.json();

        hideTyping();

        addMessage(
            "assistant",
            data.response
        );

    } catch (error) {

        hideTyping();

        console.error("Chat error:", error);

        addMessage(
            "assistant",
            "Sorry, I couldn't connect to Clinexa AI. Please try again."
        );

    } finally {

        sendButton.disabled = false;

        messageInput.focus();
    }
}

/* ================================= */
/* ADD MESSAGE */
/* ================================= */

function addMessage(
    role,
    content
) {

    welcomeScreen.style.display =
        "none";


    const row =
        document.createElement(
            "div"
        );


    row.className =
        `message-row ${role}`;


    const avatar =
        document.createElement(
            "div"
        );


    avatar.className =
        "message-avatar";


    avatar.textContent =
        role === "user"
            ? "P"
            : "✚";


    const contentWrapper =
        document.createElement(
            "div"
        );


    contentWrapper.className =
        "message-content";


    const bubble =
        document.createElement(
            "div"
        );


    bubble.className =
        "message-bubble";


    bubble.textContent =
        content;


    const time =
        document.createElement(
            "div"
        );


    time.className =
        "message-time";


    time.textContent =
        getCurrentTime();


    contentWrapper.appendChild(
        bubble
    );

    contentWrapper.appendChild(
        time
    );


    row.appendChild(
        avatar
    );

    row.appendChild(
        contentWrapper
    );


    messagesContainer.appendChild(
        row
    );


    scrollToBottom();

}


/* ================================= */
/* TYPING INDICATOR */
/* ================================= */

function showTyping() {

    hideTyping();


    const row =
        document.createElement(
            "div"
        );


    row.id =
        "typing-indicator";


    row.className =
        "message-row assistant";


    row.innerHTML = `

        <div class="message-avatar">
            ✚
        </div>

        <div class="message-content">

            <div class="message-bubble">

                <div class="typing">

                    <span></span>
                    <span></span>
                    <span></span>

                </div>

            </div>

        </div>

    `;


    messagesContainer.appendChild(
        row
    );


    scrollToBottom();

}


function hideTyping() {

    const typing =
        document.getElementById(
            "typing-indicator"
        );


    if (typing) {

        typing.remove();

    }

}


/* ================================= */
/* CLEAR CHAT */
/* ================================= */

function clearChat() {

    messagesContainer.innerHTML =
        "";

    welcomeScreen.style.display =
        "flex";

}


/* ================================= */
/* SCROLL */
/* ================================= */

function scrollToBottom() {

    const chatArea =
        document.getElementById(
            "chat-area"
        );


    chatArea.scrollTop =
        chatArea.scrollHeight;

}


/* ================================= */
/* TIME */
/* ================================= */

function getCurrentTime() {

    return new Date()
        .toLocaleTimeString(
            [],
            {
                hour: "2-digit",
                minute: "2-digit"
            }
        );

}


/* ================================= */
/* SUGGESTION CARDS */
/* ================================= */

document
    .querySelectorAll(
        ".suggestion-card"
    )
    .forEach(
        card => {

            card.addEventListener(
                "click",
                () => {

                    messageInput.value =
                        card.dataset.message;

                    sendMessage();

                }
            );

        }
    );


/* ================================= */
/* SEARCH */
/* ================================= */

const searchInput =
    document.getElementById(
        "conversation-search"
    );


searchInput.addEventListener(
    "input",
    () => {

        const search =
            searchInput.value
                .toLowerCase();


        document
            .querySelectorAll(
                ".conversation-item"
            )
            .forEach(
                item => {

                    item.style.display =
                        item.textContent
                            .toLowerCase()
                            .includes(search)
                            ? "block"
                            : "none";

                }
            );

    }
);