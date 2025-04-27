import os
from flask import Flask, request, render_template, send_file, redirect, url_for, flash
import yt_dlp

app = Flask(__name__)
# SECRET_KEY は Render の環境変数等で設定可能（ここではデフォルト値を設定）
app.secret_key = os.environ.get("SECRET_KEY", "your_secret_key")

# ダウンロードファイルの保存フォルダ（Render環境でも利用可能）
DOWNLOADS_DIR = "downloads"
if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download_video():
    url = request.form.get("url")
    if not url:
        flash("URLを入力してください。")
        return redirect(url_for("index"))
        
    # yt_dlp のオプション設定
    ydl_opts = {
        "outtmpl": os.path.join(DOWNLOADS_DIR, "%(title)s.%(ext)s"),
        "format": "bestvideo+bestaudio/best",
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info_dict)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        flash(f"エラーが発生しました: {e}")
        return redirect(url_for("index"))

if __name__ == "__main__":
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", 5000))
    app.run(host=host, port=port, debug=True)
