import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from werkzeug.exceptions import abort

class PhysicalModel():
    
    '''
    Input:
        - Load Weight
         
    Output:
        - TakeOff Distance Necessary
        - TakeOff Time
        - Excess Load Weight 
    '''
    def __init__(self):
        #Data:
        print("Initializing the physical model")
        self.TakeOffSpeed = 140 #m/s
        self.Thrust = 100000 #N
        self.TakeOffTimeMax = 100 #s
        self.WeightEmpty = 35000 #kg
        self.WeightLoadFull = 0 #kg
        self.WeightLoadToDestroy = 0 #kg
        self.WeightLoad = 0 #kg
        self.Acceleration = self.Thrust/(self.WeightEmpty+self.WeightLoad)
        self.TakeOffTime = round(self.TakeOffSpeed/self.Acceleration)
        self.TakeOffDistance = round(self.TakeOffSpeed*self.TakeOffTime/2)
        self.WeightLoadMax = round(self.Thrust*self.TakeOffTimeMax/self.TakeOffSpeed-self.WeightEmpty)
        
    def update_parameters(self):
        self.WeightLoad = self.WeightLoadFull - self.WeightLoadToDestroy
        self.Acceleration = self.Thrust/(self.WeightEmpty+self.WeightLoad)
        self.TakeOffTime = round(self.TakeOffSpeed/self.Acceleration, 1)
        self.TakeOffDistance = round(self.TakeOffSpeed*self.TakeOffTime/2)
        
    def setLoadFull(self, load):
        self.WeightLoadFull = load
        self.update_parameters()
        print(f"updated parameters: \ncurrent total load:{self.WeightLoad} \nRequired TakeOff Time:{self.TakeOffTime} \nRequired TakeOff Distance:{self.TakeOffDistance} \nDestroying: {self.WeightLoadToDestroy} ")
    
    def setWeightLoadToDestroy(self, WeightLoadToDestroy):
        self.WeightLoadToDestroy = WeightLoadToDestroy
        self.update_parameters()
        print(f"updated parameters: \ncurrent total load:{self.WeightLoad} \nRequired TakeOff Time:{self.TakeOffTime} \nRequired TakeOff Distance:{self.TakeOffDistance} \nDestroying: {self.WeightLoadToDestroy} ")
        
    def getWeightLoadToDestroy(self):
        return self.WeightLoadToDestroy
        
    def getTakeOffTime(self):
        return self.TakeOffTime
    
    def getTakeOffDistance(self):
        return self.TakeOffDistance
    
    # def getWeightLoadMax(self):
    #     return self.WeightLoadMax
    
    def getWeightLoad(self):
        return self.WeightLoad
    
    def getLoadToDestroy(self):
        return self.WeightLoadMax-self.WeightLoad

    def setLoadToMaxLoad(self):
        self.WeightLoad = self.WeightLoadMax
        self.update_parameters()
        print(f"Load = maximum. updated parameters: \ncurrent load:{self.WeightLoad} \nRequired TakeOff Time:{self.TakeOffTime} \nRequired TakeOff Distance:{self.TakeOffDistance}\n ")
        

model = PhysicalModel()


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_line(line_id):
    conn = get_db_connection()
    line = conn.execute('SELECT * FROM history WHERE id = ?',
                        (line_id,)).fetchone()
    conn.close()
    if line is None:
        abort(404)
    return line

@app.route('/')
def index():
    conn = get_db_connection()
    history = conn.execute('SELECT * FROM history').fetchall()
    conn.close()
    return render_template('index.html', history=history)

@app.route('/<int:line_id>')
def line(line_id):
    line = get_line(line_id)
    return render_template('line.html', line=line)

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        ##TODO: check the formatting here !
        LoadWeight = request.form['LoadWeight']
        WeightDestroyed = request.form['WeightDestroyed']
        TakeOffDistance = request.form['TakeOffDistance']

        if not LoadWeight:
            flash('LoadWeight is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO history (LoadWeight, WeightDestroyed, TakeOffDistance) VALUES (?, ?, ?)',
                         (LoadWeight, WeightDestroyed, TakeOffDistance))
            
            conn.commit()
            conn.close()
            model.setLoad(float(LoadWeight))
            
            return redirect(url_for('index'))

    return render_template('create.html')

@app.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    line = get_line(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM history WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(line['LoadWeight']))
    return redirect(url_for('index'))

@app.route('/calculator', methods=('GET', 'POST'))
def calculator():
    if request.method == 'POST':
        LoadWeight = request.form["LoadWeight"]
        WeightToDestroy = request.form["WeightToDestroy"]
        print(f"Received a post: weight={LoadWeight}, toDestroy={WeightToDestroy}")
        if len(LoadWeight)>=1:
            model.setLoadFull(float(LoadWeight))
            model.setWeightLoadToDestroy(float(WeightToDestroy))
    return render_template('calculator.html', takeofftime=model.getTakeOffTime(), takeoffdistance=model.getTakeOffDistance(), loadtodestroy=model.getLoadToDestroy())

@app.route('/send_to_db', methods=['POST'])
def send_to_db():
    conn = get_db_connection()
    LoadWeight = model.getWeightLoad()
    WeightDestroyed = model.getLoadToDestroy()
    TakeOffDistance = model.getTakeOffDistance()
    
    conn.execute('INSERT INTO history (LoadWeight, WeightDestroyed, TakeOffDistance) VALUES (?, ?, ?)',
                    (LoadWeight, WeightDestroyed, TakeOffDistance))
    
    conn.commit()
    conn.close()
    model.setLoad(float(LoadWeight))
            
    print("Send to the db !")
    return redirect(url_for('index'))

