from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import yt_dlp
import os

app = Flask(__name__)

# ダウンロードファイルの保存先ディレクトリ
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    # ユーザーが動画の URL を入力するフォームをレンダリング
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form.get('url')
    if not video_url:
        return redirect(url_for('index'))
    
    # yt‑dlp のオプション設定（最高品質の動画を対象・プレイリストは除外）
    ydl_opts = {
        'format': 'best',
        'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(id)s.%(ext)s'),
        'noplaylist': True
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
        file_path = ydl.prepare_filename(info)
    except Exception as e:
        return f"ダウンロード中にエラーが発生しました: {str(e)}"
    
    # ダウンロード完了ファイルを添付ファイルで返す
    return send_from_directory(DOWNLOAD_FOLDER, os.path.basename(file_path), as_attachment=True)

if __name__ == '__main__':
    # Render環境ではPORTが環境変数として渡されるのでそれを利用
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
