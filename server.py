import http.server
import socketserver

# Set the port you want to run the server on
port = 8080

# Create a custom request handler (optional)
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Customize the response here (e.g., serve dynamic content)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"Hello, World!")

# Create the server with the custom request handler
with socketserver.TCPServer(("", port), CustomHandler) as httpd:
    print(f"Serving at port {port}")
    httpd.serve_forever()