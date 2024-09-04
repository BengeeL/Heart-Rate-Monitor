# GROUP 1

# Benjamin 
# Paige
# Harpreet
# Gwen 

import json
import tkinter as tk 
from tkinter import ttk
from tkinter import scrolledtext
from group_1_Subscriber import Subscriber
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

MQTT_TOPIC = 'Live Heart Beats'
AGE = 21
MIN_SAFE_RATE = 40
MAX_BASE_SAFE_RATE = 220

class HeartBeatSubscriberGUI: 
    def __init__(self, root):
        self.root = root
        self.root.title("Heart Beats Subscriber")
        self.sub = Subscriber(MQTT_TOPIC)
        self.sub.client.on_message = self.message_handler

        self.previous_packet = 0

        # Configure rows for spacing
        for i in range(8):
            self.root.rowconfigure(i, weight=1)
            
        ########################
        # Connect - Disconnect #
        ########################
        self.CONNECT = 'Connect'
        self.DISCONNECT = 'Disconnect'
        self.btn_connection_title = tk.StringVar(value=self.CONNECT)
        
        self.btn_connection = ttk.Button(root, textvariable=self.btn_connection_title, command=self.btn_connection_clicked) 
        
        self.btn_connection.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="E")
        
        ############
        # User Age #
        ############
        self.var_age = tk.StringVar(value=AGE)

        self.lbl_age = ttk.Label(root, text='Age')
        self.entry_age = ttk.Entry(root, textvariable=self.var_age, width=33)
        self.lbl_safe_beat = ttk.Label(root, text='Safe BPM')
        self.btn_update_age = ttk.Button(root, text="Update Age", command=self.btn_update_age_clicked) 

        self.lbl_age.grid(row=1, column=0, padx=10, sticky="E")
        self.entry_age.grid(row=1, column=1, padx=10, sticky="W")
        self.lbl_safe_beat.grid(row=2, column=1, padx=10)
        self.btn_update_age.grid(row=3, column=1, padx=10, sticky="E")

        self.update_safe_bpm_label(self.var_age.get())

        ######################
        # Incoming Data Area #
        ######################
        self.input = ""

        self.lbl_heart_rate = ttk.Label(root, text='Data Log')
        self.text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=13, width=40, state=tk.DISABLED) 
  
        self.lbl_heart_rate.grid(row=4, column=0, padx=10, pady=10, sticky="NE")
        self.text_area.grid(row=4, column=1, padx=10, pady=10, sticky="NW")       

        #########
        # Topic #
        #########
        self.var_topic = tk.StringVar(value=MQTT_TOPIC)

        self.lbl_topic = ttk.Label(root, text="Topic:")
        self.entry_topic = ttk.Entry(root, textvariable=self.var_topic, width=33)

        self.lbl_topic.grid(row=5, column=0, padx=10, pady=10, sticky="E")
        self.entry_topic.grid(row=5, column=1, padx=10, pady=10, sticky="W")

        ####################
        # Heart Rate Graph #
        ####################
        self.heart_rates = []
        for i in range(60):
            self.heart_rates.append(60)
        
        self.chart_canvas = tk.Canvas(root, width=400, height=300, bg="light grey")
        self.chart_canvas.grid(row=0, rowspan=7, column=2, padx=10, pady=10, sticky="NW")

    ##################
    # CONNECT BUTTON #
    ##################
    def btn_connection_clicked(self):
        if (self.btn_connection_title.get() == self.CONNECT):
            self.connect()
        else:
            self.disconnect()

    def connect(self):
        # Subscriber Logic
        topic = self.var_topic.get()
        self.sub.connect(topic)

        # GUI updates
        self.btn_connection_title.set(self.DISCONNECT)
        self.entry_topic.config(state=tk.DISABLED)

    def disconnect(self):
        # Subscriber Logic
        self.sub.disconnect()

        # GUI updates
        self.btn_connection_title.set(self.CONNECT)
        self.entry_topic.config(state=tk.NORMAL)

    #####################
    # UPDATE AGE BUTTON #
    #####################
    def btn_update_age_clicked(self):
        age = self.var_age.get()
        self.update_safe_bpm_label(age)

    def update_safe_bpm_label(self, age):
        self.max_safe_rate = MAX_BASE_SAFE_RATE - int(age)
        self.lbl_safe_beat.config(text=f"Min safe BPM: {MIN_SAFE_RATE} - Max safe BPM {self.max_safe_rate}")

    ##########################
    # INCOMING DATA HANDLING #
    ##########################
    def message_handler(self, client, userdata, message):
        data_display = ""

        try:
            # Convert Data
            data = json.loads(message.payload.decode("utf-8"))

            packet_id = data.get('packet_id')
            timestamp = data.get('timestamp')
            heart_rate = data.get('heart_rate')

            user_data = data.get('user')
            username = user_data.get('username')
            
            # Add Packet Log
            if (self.previous_packet + 1 != int(packet_id)):
                data_display = f"\nPacket {int(packet_id) - self.previous_packet} missed.\n"
                
            data_display += f"\nPacket: {packet_id}\nTimestamp: {timestamp}\nUser: {username}\nBPM: {heart_rate}"

            if (int(heart_rate) < MIN_SAFE_RATE): 
                data_display += f"\n*** WARNING: LOW BPM RECORDED: {heart_rate} ***"

            if (int(heart_rate) > self.max_safe_rate): 
                data_display += f"\n*** WARNING: HIGH BPM RECORDED: {heart_rate} ***"

            # Add heart beat data to Graph data source. 
            self.heart_rates.append(heart_rate)
            if len(self.heart_rates) > 60:
                self.heart_rates.pop(0)  

            self.chart_canvas.after(0, self.draw_chart_in_thread)

            self.previous_packet = packet_id

        except json.JSONDecodeError:
            data_display = f"\n\nERROR: Invalid JSON data received.\n\n"
        
        # Update Log
        self.text_area.config(state=tk.NORMAL) 
        self.text_area.insert(tk.END, f"\n{data_display}")
        self.text_area.see(tk.END)  
        self.text_area.config(state=tk.DISABLED) 

    #########
    # GRAPH #
    #########
    def draw_chart_in_thread(self):
        # Extract data points for the last minute (first 60 readings)
        heart_rates = self.heart_rates[0:60]

        # Create a figure and axis
        fig, ax = plt.subplots()

        # Plot the heart rates as a dotted line
        ax.plot(heart_rates, linestyle='--', marker='o', label='Heart BPM')

        # Set Table Data
        ax.set_xlabel('Readings for the last Minute')
        ax.set_ylabel('Heart BPM')
        ax.set_title('Heart BPM for the last minute')
        ax.set_ylim([MIN_SAFE_RATE, self.max_safe_rate])
        ax.legend()
        ax.grid(True)

        # Update the Graph
        self.update_chart(fig)

        # Close the figure
        plt.close(fig)

    def update_chart(self, fig):
        # Clear the existing canvas
        self.chart_canvas.delete("all")

        # If a FigureCanvasTkAgg instance already exists, use it. Otherwise, create a new one.
        if hasattr(self, 'canvas_agg'):
            self.canvas_agg.figure = fig
        else:
            self.canvas_agg = FigureCanvasTkAgg(fig, master=self.chart_canvas)

        # Draw on the canvas
        self.canvas_agg.draw()

        # Get the widget and pack it
        self.canvas_agg.get_tk_widget().pack()


# Function to run the GUI 
def start_subscriber():
  root = tk.Tk()
  gui = HeartBeatSubscriberGUI(root)
  root.mainloop()  

if __name__ == '__main__':
  start_subscriber()