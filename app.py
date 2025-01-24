from flask import Flask, render_template, request, jsonify
import os
import yt_dlp

app = Flask(__name__)

# Path to the downloads folder
DOWNLOAD_DIR = os.path.join(os.path.expanduser("~"), "Downloads", "yt-downloader")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    video_url = request.form.get('url')
    download_type = request.form.get('type', 'video')  # 'video' or 'audio'

    if not video_url:
        return jsonify({"error": "URL is required"}), 400

    try:
        ydl_opts = {
            'outtmpl': f'{DOWNLOAD_DIR}/%(title)s.%(ext)s',
            'format': 'bestaudio/best' if download_type == 'audio' else 'bestvideo+bestaudio/best',
            'noplaylist': True,
            'noresume': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=True)
            response = {
                "message": "Download successful",
                "title": info.get('title'),
                "duration": info.get('duration'),
                "webpage_url": info.get('webpage_url'),
                "type": "Audio" if download_type == 'audio' else "Video"
            }
            return jsonify(response)

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
