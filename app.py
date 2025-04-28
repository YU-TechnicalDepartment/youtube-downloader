from flask import Flask, request, render_template, send_from_directory, redirect, url_for
import yt_dlp
import os

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form.get('url')
    if not video_url:
        return redirect(url_for('index'))
    
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
        error_message = str(e)
        # 「Video unavailable」というメッセージが含まれる場合は、ユーザー向けのエラーメッセージを返す
        if "Video unavailable" in error_message:
            return "指定された動画は利用できません。違う動画のURLを試してください。"
        else:
            return f"ダウンロード中にエラーが発生しました: {error_message}"
    
    return send_from_directory(DOWNLOAD_FOLDER, os.path.basename(file_path), as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
