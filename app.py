import threading
import webview
from flask import Flask, render_template, jsonify
import subprocess, platform, shutil

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/reboot', methods=['POST'])
def reboot_to_firmware():
    os_name = platform.system()
    try:
        if os_name == 'Windows':
            cmd = ["shutdown", "/r", "/fw", "/t", "0"]
            subprocess.run(cmd, check=True, shell=False)
            return jsonify(ok=True, os=os_name, cmd=" ".join(cmd))
        elif os_name == 'Linux':
            if shutil.which("systemctl"):
                cmd = ["systemctl", "reboot", "--firmware-setup"]
            else:
                cmd = ["reboot", "--firmware-setup"]
            subprocess.run(cmd, check=True, shell=False)
            return jsonify(ok=True, os=os_name, cmd=" ".join(cmd))
        else:
            return jsonify(ok=False, os=os_name, error="Unsupported system"), 400
    except Exception as e:
        return jsonify(ok=False, os=os_name, error=str(e)), 500


def start_flask():
    app.run(host="127.0.0.1", port=5000, debug=False)


if __name__ == "__main__":
    # نشغل Flask بخيط ثاني
    t = threading.Thread(target=start_flask, daemon=True)
    t.start()

    # نفتح نافذة WebView بدل المتصفح
    webview.create_window("BIOS Utility", "http://127.0.0.1:5000")
    webview.start()
