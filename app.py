from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import yt_dlp
import os

app = Flask(__name__)

# ダウンロードファイル保存用のディレクトリを作成
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    # ユーザーが動画 URL を入力するためのフォームを表示
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form.get('url')
    if not video_url:
        return redirect(url_for('index'))
    
    # yt‑dlp のオプション設定（フォーマットは最高品質、プレイリストは除外）
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(id)s.%(ext)s'),
        'noplaylist': True
    }
    
    # ここでは動画の存在チェックなどは行わず、直接ダウンロード処理に進む
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
    file_path = ydl.prepare_filename(info)
    
    # ダウンロード完了後、対象ファイルを送信（添付ファイルとしてダウンロード）
    return send_from_directory(DOWNLOAD_FOLDER, os.path.basename(file_path), as_attachment=True)

if __name__ == '__main__':
    # Render 環境では PORT 環境変数を利用（ローカル実行時は 5000 番ポート）
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
