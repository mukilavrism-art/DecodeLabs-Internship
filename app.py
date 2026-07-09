from flask import Flask, request, render_template_string
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel("models/gemini-2.5-flash")
chat = model.start_chat(history=[])

chat_history = []

app = Flask(__name__)

HTML = """

<!DOCTYPE html>

<html>
<head>
    <title>AI Chatbot</title>

<style>
    *{
        margin:0;
        padding:0;
        box-sizing:border-box;
        font-family:Arial, sans-serif;
    }
    <script>
window.onload = function() {
    const chatBox = document.querySelector(".chat-box");
    chatBox.scrollTop = chatBox.scrollHeight;
}
</script>

    body{
        background:#ece5dd;
    }

    .container{
        width:90%;
        max-width:900px;
        margin:20px auto;
        background:white;
        border-radius:15px;
        overflow:hidden;
        box-shadow:0 0 15px rgba(0,0,0,0.2);
    }

    .header{
        background:#075e54;
        color:white;
        padding:15px;
        font-size:22px;
        font-weight:bold;
    }

    .chat-box{
        height:500px;
        overflow-y:auto;
        padding:20px;
        background:#efeae2;
    }

    .message{
        margin-bottom:15px;
        max-width:75%;
        padding:12px;
        border-radius:10px;
        line-height:1.5;
        white-space:pre-wrap;
    }

    .user{
        background:#dcf8c6;
        margin-left:auto;
        text-align:left;
    }

   .bot{
    background:white;
    border:1px solid #ddd;
    word-wrap:break-word;
    overflow-wrap:break-word;
    white-space:pre-wrap;
    text-align:left;
}

    .input-area{
        display:flex;
        padding:15px;
        background:white;
        border-top:1px solid #ddd;
    }

    .input-area input{
        flex:1;
        padding:12px;
        border:1px solid #ccc;
        border-radius:25px;
        outline:none;
    }

    .input-area button{
        margin-left:10px;
        padding:12px 20px;
        border:none;
        background:#075e54;
        color:white;
        border-radius:25px;
        cursor:pointer;
    }

    .input-area button:hover{
        background:#0b806f;
    }
</style>


</head>
<body>

<div class="container">


<div class="header">
    Gemini AI Chatbot
</div>

<div class="chat-box">

    {% for chat in chats %}

        <div class="message user">
            {{ chat.user }}
        </div>

        <div class="message bot">
            {{ chat.bot }}
        </div>

    {% endfor %}

</div>

<form method="POST" class="input-area">
    <input type="text"
           name="message"
           placeholder="Type a message..."
           required>

    <button type="submit">Send</button>
</form>


</div>

</body>
</html>
"""
@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        user_message = request.form["message"]

        try:
            response = chat.send_message(user_message)
            bot_reply = response.text.replace("*", "")

            chat_history.append({
                "user": user_message,
                "bot": bot_reply
            })

        except Exception as e:

            chat_history.append({
                "user": user_message,
                "bot": f"Error: {str(e)}"
            })

    return render_template_string(
        HTML,
        chats=chat_history
    )


if __name__ == "__main__":
    app.run(debug=True)


    



   