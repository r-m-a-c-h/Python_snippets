import time
import socket
import threading
import tkinter as tk
from tkinter import *

selected_option = None  # Shared variable

# Create Object
root = Tk() 
root.title("FX MT4 Trainer")

wait_clr = "darkgrey"
action_clr = "lightblue"

root.configure(bg=action_clr)

# Initialize tkinter window            
root.geometry('250x300')

def set_option(option):
    global selected_option
    selected_option = option
    print(f"Option selected: {option}")

buttons = {
   "BUY": {
        "bg": "green",
        "x": 40,
        "y": 10,
        "h": 3,
        "w": 8
   },
   "SELL": {
        "bg": "red",
        "x": 140,
        "y": 10,
        "h": 3,
        "w": 8
   },
   "CLOSE_ALL": {
        "bg": "yellow",
        "x": 35,
        "y": 80,
        "h": 3,
        "w": 24
   },
   "HOLD": {
       "bg": "lightgrey",
        "x": 35,
        "y": 150,
        "h": 3,
        "w": 24
   }
}

def create_button(key):
    btn = Button(root, 
                text=key, 
                #bg=buttons[key]["bg"],
                bg=wait_clr,
                height=buttons[key]["h"], width=buttons[key]["w"], 
                state=tk.DISABLED,
                # Call change_color when the button is clicked
                command=lambda: set_option(key))
    btn.place(x=buttons[key]["x"], y=buttons[key]["y"])
    return btn

buy = create_button("BUY")
sell = create_button("SELL")
close_all = create_button("CLOSE_ALL")
hold = create_button("HOLD")

spinboxes = {
    "RISK": {
        "values": ("0.5", "0.75", "1", "1.25", "1.5", "1.75", "2", "2.25", "2.5"),
        "width": 4,
        "x": 135,
        "y": 215,
        "default": "2.5"
    },
    "TP_RATIO": {
        "width": 4,
        "x": 135,
        "y": 235,
        "default": "3"
    },
    "SL_RATIO": {
        "width": 4,
        "x": 135,
        "y": 255,
        "default": "1"
    },
    "BAR_INDEX": {
        "values": ("1", "2", "3", "4", "5", "6", "7", "8", "9", "10"),
        "width": 4,
        "x": 135,
        "y": 275,
        "default": "1"
    }
}

def create_spinxbox(key):
    spinbox_var = tk.StringVar(value="0.000") # Initial value with 3 decimals
    if(key == "TP_RATIO"):
        spinbox = Spinbox(root,  from_=0.50, to=10.00, increment=0.10, textvariable=spinbox_var, width=spinboxes[key]["width"])
    elif(key == "SL_RATIO"):
        spinbox = Spinbox(root,  from_=0.1, to=10.00, increment=0.1, textvariable=spinbox_var, width=spinboxes[key]["width"])
    else:    
        spinbox = Spinbox(root, values=spinboxes[key]["values"], textvariable=spinbox_var, width=spinboxes[key]["width"])
    spinbox.place(x=spinboxes[key]["x"], y=spinboxes[key]["y"])
    spinbox.delete(0, "end")
    spinbox.insert(0, spinboxes[key]["default"])
    return spinbox

spinbox_risk = create_spinxbox("RISK")
spinbox_takeprofit = create_spinxbox("TP_RATIO")
spinbox_stoploss = create_spinxbox("SL_RATIO")
spinbox_bar_index = create_spinxbox("BAR_INDEX")

labels = {
    "RISK": {
        "label": "RISK %:",
        "x": 50,
        "y": 215
    },
    "TP_RATIO": {
        "label": "TAKEPROFIT:",
        "x": 50,
        "y": 235
    },
    "SL_RATIO": {
        "label": "STOPLOSS:",
        "x": 50,
        "y": 255
    },
    "BAR_INDEX": {
        "label": "BAR INDEX:",
        "x": 50,
        "y": 275
    }
}

def create_label(key):
    label = tk.Label(root, text=labels[key]["label"], bg=action_clr)
    label.place(x=labels[key]["x"], y=labels[key]["y"])
    return label

label_risk = create_label("RISK")
label_takeprofit = create_label("TP_RATIO")
label_stoploss = create_label("SL_RATIO")
label_bar_index = create_label("BAR_INDEX")

def wait_colors():
    #root.configure(bg=wait_clr)
    buy.configure(bg=wait_clr, state=tk.DISABLED)
    sell.configure(bg=wait_clr, state=tk.DISABLED)
    close_all.configure(bg=wait_clr, state=tk.DISABLED)
    hold.configure(bg=wait_clr, state=tk.DISABLED)
    #label_risk.configure(bg=wait_clr)
    #label_takeprofit.configure(bg=wait_clr)
    #label_stoploss.configure(bg=wait_clr)
    #label_bar_index.configure(bg=wait_clr)

def action_colors():
    root.configure(bg=action_clr)
    buy.configure(bg=buttons["BUY"]["bg"], state=tk.NORMAL)
    sell.configure(bg=buttons["SELL"]["bg"], state=tk.NORMAL)
    close_all.configure(bg=buttons["CLOSE_ALL"]["bg"], state=tk.NORMAL)
    hold.configure(bg=buttons["HOLD"]["bg"], state=tk.NORMAL)
    label_risk.configure(bg=action_clr)
    label_takeprofit.configure(bg=action_clr)
    label_stoploss.configure(bg=action_clr)
    label_bar_index.configure(bg=action_clr)

def handle_client(conn, addr):
    global selected_option
    selected_option = None
    action_colors()

    data = conn.recv(1024)
    
    #print('Connected by', addr)
    #print(f"Received: {data.decode()}")  # Example: decode received data
    #print(float(spinbox_risk.get()))

    # Process the received data and create a response
    while True:
        if selected_option:  # Check if an option has been selected
            response_message = f"{selected_option};{float(spinbox_risk.get())};{float(spinbox_takeprofit.get())};{float(spinbox_stoploss.get())};{float(spinbox_bar_index.get())}"
            print(response_message)
            conn.send(response_message.encode())
            selected_option = None #reset the variable
            break
        time.sleep(0.1)  # Avoid busy-waiting, check every 0.1 seconds
    conn.close()
    wait_colors()


def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 5002))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.daemon = True #thread will close when the main program exits
        client_thread.start()

server_thread = threading.Thread(target=start_server)
server_thread.daemon = True
server_thread.start()

root.mainloop()