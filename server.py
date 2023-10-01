import http.server
import socketserver
import threading
import sys
import mysql.connector

'''
HTML Cheat:
skip line : <br>
parapgraph: <p> - </p>
tabs: 
    - simple: &nbsp
    - double: &ensp
    - four  : &emsp
bald: <b> - </b>
'''

# Set the port you want to run the server on
port = 8084

class PhysicalModel():
    def __init__(self):
        #Data:
        self.TakeOffSpeed = 140 #m/s
        self.Thrust = 100000 #N
        self.TakeOffTimeMax = 100 #s
        self.MassEmpty = 35000 #kg
        self.MassLoad = 0 #kg
        self.Acceleration = self.Thrust/(self.MassEmpty+self.MassLoad)
        self.TakeOffTime = round(self.TakeOffSpeed/self.Acceleration)
        self.Runwaylength = round(self.TakeOffSpeed*self.TakeOffTime/2)
        self.MassLoadMax = round(self.Thrust*self.TakeOffTimeMax/self.TakeOffSpeed-self.MassEmpty)
        self.emptyLoadMessage = f'''<p style="font-size:2vw"><b>Without load</b>, with the current conditions,
                                    we need a maximum of <u>{self.MassLoadMax} kg</u> of load on board</p>'''

        # Init a SQL database here:
        mydb = mysql.connector.connect(host="localhost")
        mycursor = mydb.cursor()
        mycursor.execute("CREATE DATABASE mydatabase")

    def set_parameters(self):
        self.Acceleration = self.Thrust/(self.MassEmpty+self.MassLoad)
        self.TakeOffTime = self.TakeOffSpeed/self.Acceleration
        self.Runwaylength = self.TakeOffSpeed*self.TakeOffTime/2
        self.outputmessage = f'''<p style="font-size:2vw"><b>With a load of <u>{self.MassLoad}kg</u></b>: we have <br> 
                                    &emsp;Estimated Takeoff time: {self.TakeOffTime}s <br>
                                    &emsp;Estimated required runway length: {self.Runwaylength}m</p>'''
    def setload(self, load):
        self.MassLoad = load

# Create a custom request handler (optional)
class CustomHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        # Customize the response here (e.g., serve dynamic content)
        model = PhysicalModel()
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b'''<h1 style="font-size:8vw">Server started!</h1>
                             <h2 style="font-size:4vw">This server as been created by Eitan ALLAL </h2>''')
        self.wfile.write(model.emptyLoadMessage.encode("utf-8"))
        model.setload(10000)
        model.set_parameters()
        self.wfile.write(model.outputmessage.encode("utf-8"))



# Create the server with the custom request handler
def run_server(port):
    socketserver.ThreadingTCPServer.allow_reuse_address = True
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