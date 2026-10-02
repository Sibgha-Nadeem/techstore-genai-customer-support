import { useState } from "react";
import "./App.css";

function App() {

  const [message, setMessage] = useState("");

  const [messages, setMessages] = useState([
    {
  sender: "assistant",
  text: "Hi! 👋 I'm TechStore's AI customer support assistant. I can help with questions about our products, shipping, returns, payments, and warranties. I can only provide information available in my knowledge base, so I may not be able to answer questions outside these areas."
}
  ]);

  async function sendMessage() {

    if (message.trim() === "") {
      return;
    }

    // Save the customer's message
    const userMessage = {
      sender: "user",
      text: message
    };

    setMessages((previousMessages) => [
      ...previousMessages,
      userMessage
    ]);

    // Save the message before clearing the input
    const question = message;

    setMessage("");

    try {

      // Send the question to FastAPI
      const response = await fetch(
        "http://127.0.0.1:8000/ask",
        {
          method: "POST",

          headers: {
            "Content-Type": "application/json"
          },

          body: JSON.stringify({
            question: question
          })
        }
      );

      const data = await response.json();

      // Add the AI response to the chat
      const assistantMessage = {
        sender: "assistant",
        text: data.answer
      };

      setMessages((previousMessages) => [
        ...previousMessages,
        assistantMessage
      ]);

    } catch (error) {

      console.error(error);

      setMessages((previousMessages) => [
        ...previousMessages,
        {
          sender: "assistant",
          text: "Sorry, I couldn't connect to the support server."
        }
      ]);
    }
  }

  return (
    <div className="app">

      <div className="chat-container">

        {/* Header */}

        <div className="chat-header">

          <div>
            <h1>TechStore</h1>
            <p>Support Chat Bot</p>
          </div>

          <div className="status">
            <span className="status-dot"></span>
            Online
          </div>

        </div>


        {/* Messages */}

        <div className="chat-messages">

          {messages.map((item, index) => (

            <div
              key={index}
              className={
                item.sender === "user"
                  ? "message user-message"
                  : "message assistant-message"
              }
            >
              {item.text}
            </div>

          ))}

        </div>


        {/* Input */}

        <div className="chat-input">

          <input
            type="text"
            placeholder="Type your question..."
            value={message}

            onChange={(event) => {
              setMessage(event.target.value);
            }}

            onKeyDown={(event) => {

              if (event.key === "Enter") {
                sendMessage();
              }

            }}
          />

          <button onClick={sendMessage}>
            Send
          </button>

        </div>

      </div>

    </div>
  );
}

export default App;