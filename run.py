# run.py
import os
import socket
from app import create_app

app = create_app()

def get_local_ip():
    """Return the local network IP address or 127.0.0.1 when unavailable."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(("10.255.255.255", 1))
        return sock.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        sock.close()

if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") in ("1", "true", "True")
    port = int(os.environ.get("PORT", 3000))
    host = "0.0.0.0"
    local_ip = get_local_ip()

    print("Starting Herbal Homeo app...")
    print(f"Local URL: http://127.0.0.1:{port}")
    if local_ip != "127.0.0.1":
        print(f"Network URL: http://{local_ip}:{port}")
        print("Other devices on the same Wi-Fi can connect using the Network URL.")
    else:
        print("No Wi-Fi/local network address detected. The app is still available locally.")

    app.run(debug=debug, port=port, host=host)
