import http.server
import socketserver
import webbrowser
import os

PORT = 8000
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

print(f"启动服务器，端口: {PORT}")
print(f"在浏览器中访问: http://localhost:{PORT}/map_navigation.html")
print("按 Ctrl+C 停止服务器")

# 自动打开浏览器
webbrowser.open(f"http://localhost:{PORT}/map_navigation.html")

# 启动服务器
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n服务器已停止")
        httpd.server_close() 