import string
import random
from flask import Flask, render_template, redirect, request

app = Flask(__name__)

# 存储房间信息到字典
room_info = {}


@app.route("/")
def start():
    code = generate_code()
    return redirect(f"/{code}")

@app.route("/<string:code>")
def play(code):
    if not is_valid_code(code):
        code = generate_code()
        return redirect(f"/{code}")
    if code not in room_info:
        room_info[code] = {'game_board': [[None]*9 for _ in range(9)]}
    print(room_info)
    
    # 在这里完成游戏逻辑
    
    return render_template("s.html", code=code)

@app.route("/update/<string:code>", methods=["POST"])
def update(code):
    if code in room_info:
        game_board = room_info[code]['game_board']
        
        # 从请求获取更新的棋盘信息
        req_data = request.get_json()
        row = req_data['row']
        col = req_data['col']
        player = req_data['player']
        
        # 更新棋盘
        game_board[row][col] = player
        print(game_board)
        
        # 返回成功的响应
        return {"message": "Update successful."}
    
    # 返回错误的响应
    return {"message": "Error: Invalid room code."}, 400

def generate_code():
    code = ''.join(random.choices(string.ascii_uppercase, k=6))
    return code

def is_valid_code(code):
    # 检查code是否为6位大写字母
    if len(code) != 6 or not code.isalpha() or not code.isupper():
        return False
    return True

if __name__ == "__main__":
    app.run()
