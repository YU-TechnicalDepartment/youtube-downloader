from flask import Flask, request, send_file, render_template, redirect, url_for, flash
import os
from yt_dlp import YoutubeDL

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  # フラッシュメッセージ等に必要な場合

# 一時的な保存先。サーバー環境やホスティング先によって適切なパスに調整してください。
DOWNLOAD_FOLDER = '/tmp'

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form.get("url")
        if not video_url:
            flash("URLを入力してください。")
            return redirect(url_for("index"))

        # 動画の出力テンプレート：一時ディレクトリ内に保存
        ydl_opts = {
            'format': 'best',
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s')
        }
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info)
        except Exception as e:
            flash(f"ダウンロード中にエラーが発生しました: {e}")
            return redirect(url_for("index"))
        
        # ファイルが無事ダウンロードされた場合、直接ユーザーに送信
        if os.path.exists(filename):
            return send_file(filename, as_attachment=True)
        else:
            flash("ダウンロードしたファイルが見つかりませんでした。")
            return redirect(url_for("index"))
    
    # GETの場合はHTMLフォームを表示
    return render_template("index.html")

if __name__ == "__main__":
    # Renderなどのクラウド環境ではPORTが環境変数から渡されるのでその場合は下記のように設定
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
