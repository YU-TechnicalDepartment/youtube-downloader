from flask import Flask, redirect, request, session
import requests
from yt_dlp import YoutubeDL
import os

app = Flask(__name__)
app.secret_key = 'yu10002025'

CLIENT_ID = "663075264415-79kub7cem28i6itfo6sc96kp167hfing.apps.googleusercontent.com"
CLIENT_SECRET = "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"
REDIRECT_URI = "https://youtube-downloader-dfgn.onrender.com"
SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
TOKEN_URL = "https://oauth2.googleapis.com/token"
AUTH_URL = "https://accounts.google.com/o/oauth2/auth"

@app.route("/")
def index():
    return '<a href="/login">GoogleでログインしてYouTube動画をダウンロード</a>'

@app.route("/login")
def login():
    auth_params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPE,
        "access_type": "offline",
        "prompt": "consent"
    }
    return redirect(f"{AUTH_URL}?{requests.compat.urlencode(auth_params)}")

@app.route("/callback")
def callback():
    code = request.args.get("code")
    token_params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code,
        "grant_type": "authorization_code"
    }
    response = requests.post(TOKEN_URL, data=token_params)
    session['token'] = response.json().get("access_token")
    return "ログイン完了！ <a href='/download'>動画をダウンロード</a>"

@app.route("/download")
def download_video():
    if 'token' not in session:
        return redirect("/login")

    video_url = request.args.get("url")
    if not video_url:
        return "動画URLを指定してください。"

    ydl_opts = {
        'format': 'best',
        'outtmpl': './%(title)s.%(ext)s',
        'cookiefile': 'cookies.txt'  # OAuth認証後のクッキーを利用
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            filename = ydl.prepare_filename(info)
            return f"ダウンロード完了: {filename}"
    except Exception as e:
        return f"エラー: {e}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

