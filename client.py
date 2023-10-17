import requests
import datetime
import re

port = 8080

def check_formatting_float(value):
    try:
        float_value = float(value)
        if float_value < 0:
            print("enter a positive value")
            return True
        elif float_value > 1e6:
            print("This value seems to big. Enter a value less than 1,000,000")
            return True
        else:
            print("Test OK!")
            return False
    except:
        print("please enter a valid float")
        return True

def check_formatting_date(date):
    regex = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}(.\d+)?"
    if re.match(regex, date):
        return False
    else:
        return True


server_url = f"http://127.0.0.1:{port}/eitan"

while True:
    # Get user input from the terminal
    main_menu = input("Press 0 if you want to send data to the server: ")
    print(main_menu.lower())
    if main_menu.lower() == '0':
        loop = True
        while loop:
            load_weight = input("Enter the weight in kg of the load: ")
            loop = check_formatting_float(load_weight)
        loop = True
        while loop:
            TakeOffDist = input("Enter the take off distance in meters: ")
            loop = check_formatting_float(TakeOffDist)
        loop = True
        while loop:
            weightDestroyed = input("Enter the weight in kg of the load destroyed: ")
            loop = check_formatting_float(weightDestroyed)
        loop = True
        while loop:
            time = input("Enter the time under the format YYYY-MM-DD HH:MM:SS.nnnnn. To take the current time, leave empty")
            if time.lower()=="":
                time = str(datetime.datetime.now())
                print("Current time:", time)
                loop = False
            else:
                loop = check_formatting_date(time)
                print()



        data_to_send = {
        "load_weight": load_weight,
        "takeoff_dist": TakeOffDist,
        "weight_destroyed": weightDestroyed,
        "time": time
        }

        try:
            # Send a POST request to the server with the data
            response = requests.post(server_url, json=data_to_send)

            # Check if the request was successful
            if response.status_code == 200:
                print("Data sent successfully to the server.")

            else:
                print(f"Failed to send data. Server returned status code: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    if main_menu.lower() == 'exit':
        break



print("Client is exiting.")