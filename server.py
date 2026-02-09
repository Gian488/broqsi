import socket
import threading
import pyautogui
import io
from PIL import Image

HOST = ''  # Listen on all interfaces
PORT = 5001


def handle_client(conn):
    try:
        while True:
            # Take screenshot
            screenshot = pyautogui.screenshot()
            buf = io.BytesIO()
            screenshot.save(buf, format='JPEG')
            img_bytes = buf.getvalue()
            # Send image size first
            conn.sendall(len(img_bytes).to_bytes(8, 'big'))
            # Send image bytes
            conn.sendall(img_bytes)
            # Receive control command
            cmd = conn.recv(1024).decode()
            if cmd:
                parts = cmd.split()
                if parts[0] == 'move':
                    x, y = int(parts[1]), int(parts[2])
                    pyautogui.moveTo(x, y)
                elif parts[0] == 'click':
                    pyautogui.click()
                elif parts[0] == 'type':
                    text = ' '.join(parts[1:])
                    pyautogui.typewrite(text)
    except Exception as e:
        print('Connection closed:', e)
    finally:
        conn.close()

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)
    print(f'Server listening on port {PORT}...')
    while True:
        conn, addr = s.accept()
        print('Connected by', addr)
        threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

if __name__ == '__main__':
    start_server()
