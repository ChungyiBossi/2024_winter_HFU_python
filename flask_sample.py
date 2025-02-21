from flask import Flask
from chatgpt_sample import chat_with_chatgpt

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/home/<user_message>")
def hello_home(user_message):
    chatgpt_response = chat_with_chatgpt(
        user_message=user_message,
        system_prompt="你是一位後端管理員，有前端使用者會呼叫你。"
    )
    return chatgpt_response


# 如果要使用 python xxx.py 執行
if __name__ == '__main__':
    app.run(debug=True)
