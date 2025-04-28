from flask import Flask, request, send_file, render_template_string
import os
from yt_dlp import YoutubeDL

app = Flask(__name__)

# シンプルなHTMLフォーム（必要に応じてテンプレートシステムに拡張可能）
HTML = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>YouTube Downloader</title>
  </head>
  <body>
    <h1>YouTube Downloader</h1>
    <form method="POST">
      <input name="url" type="text" placeholder="YouTubeのURLを入力" style="width: 300px;">
      <button type="submit">ダウンロード</button>
    </form>
  </body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        video_url = request.form.get("url")
        if not video_url:
            return "URLを入力してください", 400

        # 出力ファイル名のテンプレート
        output_template = "downloaded_video.%(ext)s"
        ydl_opts = {
            "format": "best",
            "outtmpl": output_template,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info)
        except Exception as e:
            return f"ダウンロード中にエラーが発生しました: {e}", 500

        # ダウンロード完了後、ファイルを返す
        return send_file(filename, as_attachment=True)
    return render_template_string(HTML)

if __name__ == "__main__":
    # Renderでは環境変数PORTが設定されるので、そちらを優先します
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
