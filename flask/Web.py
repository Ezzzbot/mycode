from flask import Flask, render_template, jsonify, request
#from module.calibration_nine import matrix_calculate
from flask_cors import CORS  # 导入 CORS

app = Flask(__name__)
CORS(app)  # 启用 CORS，允许所有来源访问

@app.route('/')
def index():
    return render_template('index.html', output="")
# 加载首页内容
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')
@app.route('/submit', methods=['POST'])
def submit():
    user_input = request.form.get('user_input')  # 使用get方法避免KeyError
    # 在这里处理用户输入
    print(f'用户输入了: {user_input}')  # 打印到控制台
    return '', 204  # 返回一个空的响应

if __name__ == '__main__':
    app.run(debug=True,host='127.0.0.1', port=5000, threaded=True)