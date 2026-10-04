import http.server
import socketserver
import os

PORT = 5173
os.chdir(r"C:\Users\Public\data_analyst_portfolio\presentation_layer")
Handler = http.server.SimpleHTTPRequestHandler

class MyServer(socketserver.TCPServer):
    allow_reuse_address = True

try:
    with MyServer(("", PORT), Handler) as httpd:
        print(f"Premium BI Presentation running successfully!")
        print(f"Open this exact link in your browser to view: http://localhost:{PORT}")
        httpd.serve_forever()
except Exception as e:
    print(f"Error starting server: {e}")
