import http.server
import socketserver
import threading
import sys

# Set the port you want to run the server on
port = 8080

class PhysicalModel():
    def __init__(self):
        #Data:
        self.TakeOffSpeed = 140 #m/s
        self.Thrust = 100000 #N
        self.TakeOffTimeMax = 100 #s
        self.MassEmpty = 35000 #kg
        #Computation for empty load
        self.Acceleration = self.Thrust/self.MassEmpty
        self.TakeOffTime = self.TakeOffSpeed/self.Acceleration
        self.Runwaylength = self.TakeOffSpeed*self.TakeOffTime/2
        self.MassLoadMax = self.Thrust*self.TakeOffTimeMax/self.TakeOffSpeed-self.MassEmpty

        self.emptyLoadMessage = f"Without load, with the current conditions, we need a maximum of {self.MassLoadMax} kg on board"
# Create a custom request handler (optional)
class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Customize the response here (e.g., serve dynamic content)
        model = PhysicalModel()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write("Hello, World!\nHi".encode("utf-8"))
        self.wfile.write(model.emptyLoadMessage.encode("utf-8"))

# Create the server with the custom request handler
def run_server(port):
    with socketserver.TCPServer(("", port), CustomHandler) as httpd:
        print(f"Serving at port {port}")
        print(f"to access to the server, run http://localhost:{port}/")
        httpd.serve_forever()

# Create and start the server thread
server_thread = threading.Thread(target=run_server, args=(port,))
server_thread.daemon = True
server_thread.start()

try:
    # Monitor keyboard input for the "Esc" key press
    while True:
        key = input("Type 'Quit' to stop the server: ")
        if key.lower() == 'quit':
            print("Stopping the server...")
            break
except KeyboardInterrupt:
    pass

# Gracefully exit the server thread
sys.exit()