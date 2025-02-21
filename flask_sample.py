from flask import Flask, render_template
from markupsafe import escape
from chatgpt_sample import chat_with_chatgpt

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/test/<int:user_id>/")
def hello_user(user_id):
    return f"<p>Hello USER-{escape(user_id)}, World!</p>"


@app.route("/test/<path:subpath>/")
def hello_path(subpath):
    return f"<p>Hello PATH-{escape(subpath)}, World!</p>"


@app.route("/test/<user_message>/")
def hello_home(user_message):
    chatgpt_response = chat_with_chatgpt(
        user_message=user_message,
        system_prompt="你是一位後端管理員，有前端使用者會呼叫你。"
    )
    return chatgpt_response


@app.route("/sample/")
def show_html_sample():
    return render_template(
        'sample.html',
        name="Tony",
        numbers=[11, 22, 33, 44, 55],
        pairs=[('A', 1), ('B', 2), ('C', 3)],
        dict_data={'A': 1, 'B': 2, 'C': 3}
    )


# 如果要使用 python xxx.py 執行
if __name__ == '__main__':
    app.run(debug=True)
