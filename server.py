import http.server
import socketserver
import threading
import sys
import sqlite3
import json
import datetime

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
port = 8080

class PhysicalModel():
    def __init__(self):
        #Data:
        print("Initializing the physical model")
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
        self.conn = sqlite3.connect("history.db")
        print("opened db successfully")

        request = ("CREATE TABLE IF NOT EXISTS history(id INT, weight DECIMAL(10,3), TakeOffDist DECIMAL(10,3),"
                   "weightDestroyed DECIMAL(10,3), time DATETIME);")

        self.conn.execute(request)
        self.conn.commit()

    def set_parameters(self):
        self.Acceleration = self.Thrust/(self.MassEmpty+self.MassLoad)
        self.TakeOffTime = self.TakeOffSpeed/self.Acceleration
        self.Runwaylength = self.TakeOffSpeed*self.TakeOffTime/2
        self.outputmessage = f'''<p style="font-size:2vw"><b>With a load of <u>{self.MassLoad}kg</u></b>: we have <br> 
                                    &emsp;Estimated Takeoff time: {self.TakeOffTime}s <br>
                                    &emsp;Estimated required runway length: {self.Runwaylength}m</p>'''
    def setload(self, load):
        self.MassLoad = load

    def write_input(self, weight, TakeOffDist, weightDestroyed, time):
        # Find new ID:
        query = "SELECT MAX(id) FROM history"
        res = self.conn.execute(query)
        id = res.fetchall()[0][0]+1

        sql = "INSERT INTO history (id, weight, TakeOffDist, weightDestroyed, time) VALUES (?, ?, ?, ?, ?)"
        values = (id, weight, TakeOffDist, weightDestroyed, time)
        self.conn.execute(sql, values)

        self.conn.commit()
        print("Data inserted successfully")

    def receive_message(self, loadWeight, TakeOffDist, weightDestroyed, time):
        print(f"received: {loadWeight}kg, {TakeOffDist}m, {weightDestroyed}kg, time:{time}")
        # You can perform any processing or actions with the received data here
        #add in the sql table the new input
        self.write_input(loadWeight, TakeOffDist, weightDestroyed, time)



# Create a custom request handler (optional)
class CustomHandler(http.server.BaseHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.model = PhysicalModel()
        self.messages_to_display=[]
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b'''<h1 style="font-size:8vw">Server started!</h1>
                             <h2 style="font-size:4vw">This server as been created by Eitan ALLAL </h2>''')
        self.wfile.write(self.model.emptyLoadMessage.encode("utf-8"))
        self.model.setload(10000)
        self.model.set_parameters()
        self.wfile.write(self.model.outputmessage.encode("utf-8"))
        self.model.write_input(0, 500, 0, 2)

        print(self.messages_to_display)

        if len(self.messages_to_display)==0:
            print("Nothing to display here. Printing \"waiting for an input of our client\"")
            self.wfile.write("Waiting an input of our client".encode("utf-8"))
        else:
            self.wfile.write(self.messages_to_display.encode("utf-8"))


    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8')
        print(post_data)
        if self.path == "/eitan":
            # Process the data received from the client
            print("Received POST data:")
            data = json.loads(post_data)  # Assuming you're sending JSON data from the client
            loadWeight = data.get("load_weight")
            TakeOffDist = data.get("takeoff_dist")
            weightDestroyed = data.get("weight_destroyed")
            time = data.get("time")

            time = datetime.datetime.strptime(time, "%Y-%m-%d %H:%M:%S.%f")
            print(time)
            self.model.receive_message(loadWeight, TakeOffDist, weightDestroyed, time)
            print("received packet successfully")
            self.messages_to_display.append(f'''
                        <p style="font-size:2vw"><b>Received new data in the SQL table. </b> <br>
                            &emsp; - Time: {time} <br>
                            &emsp; - Load Weight: {loadWeight} <br>
                            &emsp; - Take-Off Distance: {TakeOffDist} <br>
                            &emsp; - Weight Destroyed: {weightDestroyed} </p>
                        ''')
            print("After sending response to client:", self.messages_to_display)

            # Send a response back to the client
            self.send_response(200, message=None)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            response_message = "Data received successfully!"
            self.wfile.write(response_message.encode("utf-8"))
        else:
            self.send_error(404)



# Create the server with the custom request handler
def run_server(port):
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", port), CustomHandler) as httpd:
        print(f"Serving at port {port}")
        print(f"to access to the server, run http://127.0.0.1:{port}/")
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