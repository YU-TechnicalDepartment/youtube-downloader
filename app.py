from flask import Flask, request, send_file
import os
from yt_dlp import YoutubeDL
import tempfile

app = Flask(__name__)

# 一時的な保存先ディレクトリ（システムのテンポラリ領域を利用）
DOWNLOAD_DIR = tempfile.gettempdir()

# ダウンロードオプションの設定（ファイル名には動画タイトルが使われます）
ydl_opts = {
    'format': 'best',
    'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s')
}

def download_video(url):
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return filename
    except Exception as e:
        print("動画ダウンロード中にエラーが発生しました:", e)
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form.get("video_url")
        if video_url:
            filename = download_video(video_url)
            if filename and os.path.exists(filename):
                # ダウンロードしたファイルをユーザーに返す
                return send_file(filename, as_attachment=True)
            else:
                return "動画のダウンロードに失敗しました。", 400
    return '''
        <html>
            <head>
                <meta charset="UTF-8">
                <title>YouTube Downloader</title>
            </head>
            <body>
                <h1>YouTube Downloader</h1>
                <form method="post">
                    <label for="video_url">ダウンロードするYouTube動画のURLを入力してください：</label><br>
                    <input type="text" id="video_url" name="video_url" size="50"><br><br>
                    <input type="submit" value="ダウンロード">
                </form>
            </body>
        </html>
    '''

if __name__ == "__main__":
    # Render では PORT 環境変数がセットされるので、その値を使います
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
