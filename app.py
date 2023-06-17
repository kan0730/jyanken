from flask import Flask, request, render_template, redirect
import random

app = Flask(__name__)

game_counter = 0
win_counter = 0
loss_counter = 0
#最初の画面
@app.route("/")
def menu():
    return render_template("menu.html")
#ルール説明
@app.route("/rule")
def route():
    return render_template("rule.html")
#ゲーム画面
@app.route("/game", methods=["GET", "POST"])
def game():
    global game_counter, win_counter, loss_counter

    player_choice = None
    enemy_choice = None
    result = None

    if request.method == "POST":
        player_choice = request.form.get("choice")  # プレイヤーの手を取得
        enemy_choice = generate_enemy_choice()  # 敵の手を生成
        result = determine_winner(player_choice, enemy_choice)  # 結果を判定

        # 勝利した場合、勝利回数をカウントアップ
        if result == "勝ち":
            win_counter += 1

        game_counter += 1
        # 3回勝利した場合はリザルト画面に遷移
        if win_counter >= 3:
            reset_counters()
            return redirect("/result")

        # 敗北した場合、敗北回数をカウントアップ
        if result == "負け":
            loss_counter += 1

        game_counter += 1
        # 3回負けた場合はリザルト画面に遷移
        if loss_counter >= 3:
            reset_counters()
            return redirect("/result2")

    return render_template("game.html", player_choice=player_choice, enemy_choice=enemy_choice, result=result)
#勝ち画面
@app.route("/result")
def result():
    return render_template("result.html")
#負け画面
@app.route("/result2")
def result2():
  return render_template("result2.html")

def generate_enemy_choice():
    choices = ["グー", "チョキ", "パー"]
    return random.choice(choices)

def determine_winner(player_choice, enemy_choice):
    if player_choice == enemy_choice:
        return "引き分け"
    elif (
        (player_choice == "グー" and enemy_choice == "チョキ")
        or (player_choice == "チョキ" and enemy_choice == "パー")
        or (player_choice == "パー" and enemy_choice == "グー")
    ):
        return "勝ち"
    else:
        return "負け"

def reset_counters():
    global game_counter, win_counter, loss_counter
    game_counter = 0
    win_counter = 0
    loss_counter = 0

# ゲームが終了した後に呼び出してカウンターをリセットする
reset_counters()

if __name__ == "__main__":
    app.run(debug=True)