# GROUP 1

# Benjamin 
# Paige
# Harpreet
# Gwen 

from tkinter import messagebox
from group_1_User import User
import tkinter as tk 
from tkinter import ttk
import group_1_Publisher as pub

MQTT_TOPIC = 'Live Heart Beats'
USER = User("User123", "Usr123")

class HeartBeatPublisherGUI: 
    def __init__(self, root):
        self.root = root
        self.root.title("Heart Beats Publisher")
        self.pub = pub.Publisher(MQTT_TOPIC, USER)

        # Configure rows for spacing
        for i in range(9):
            self.root.rowconfigure(i, weight=1)
        
        ########################
        # Connect - Disconnect #
        ########################
        self.CONNECT = 'Connect'
        self.DISCONNECT = 'Disconnect'
        self.btn_connection_title = tk.StringVar(value=self.CONNECT)

        self.btn_connection = ttk.Button(root, textvariable=self.btn_connection_title, command=self.btn_connection_clicked) 
        
        self.btn_connection.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="E")

        ######################
        # Minimum Range Data #
        ######################
        self.var_min_fluctuation = tk.StringVar(value=0)
        self.min_fluctuation = int(self.var_min_fluctuation.get())

        self.lbl_min_fluctuation = ttk.Label(root, text='Min Range Data')
        self.entry_min_fluctuation = ttk.Entry(root, textvariable=self.var_min_fluctuation)
        
        self.lbl_min_fluctuation.grid(row=1, column=0, padx=10, sticky="E")
        self.entry_min_fluctuation.grid(row=1, column=1, padx=10, sticky="W")

        ######################
        # Maximum Range Data #
        ######################
        self.var_max_fluctuation = tk.StringVar(value=30)
        self.max_fluctuation = int(self.var_max_fluctuation.get())

        self.lbl_max_fluctuation = ttk.Label(root, text='Max Range Data')
        self.entry_max_fluctuation = ttk.Entry(root, textvariable=self.var_max_fluctuation)
        
        self.lbl_max_fluctuation.grid(row=2, column=0, padx=10, sticky="E")
        self.entry_max_fluctuation.grid(row=2, column=1, padx=10, sticky="W")

        #################
        # Activity Data #
        #################
        self.state_var = tk.StringVar(value="resting")

        self.lbl_activity_data = ttk.Label(root, text='Activity Data')
        self.rdb_resting = ttk.Radiobutton(root, text="Resting Heart", variable=self.state_var, value="resting")
        self.rdb_active = ttk.Radiobutton(root, text="Active Heart", variable=self.state_var, value="active")
        
        self.lbl_activity_data.grid(row=3, column=0, padx=10, pady=10, sticky="E")
        self.rdb_resting.grid(row=3, column=1, padx=10, sticky="W")
        self.rdb_active.grid(row=4, column=1, padx=10, sticky="W")

        #################
        # Update Button #
        #################
        self.btn_update = ttk.Button(root, text="Update", command=self.update_heart_sensor) 

        self.btn_update.grid(row=5, column=0, columnspan=2, padx=10, sticky="E")

        ######################################
        # Start Publishing - Stop Publishing #
        ######################################
        self.START_PUBLISHING = 'Start Publishing'
        self.STOP_PUBLISHING = 'Stop Publishing'
        self.btn_publish_title = tk.StringVar(value=self.START_PUBLISHING)

        self.btn_publish = ttk.Button(root, textvariable=self.btn_publish_title, command=self.btn_publish_clicked, state=tk.DISABLED) 
        
        self.btn_publish.grid(row=6, column=0, columnspan=2, padx=10, sticky="E")

        ########
        # USER #
        ########
        self.var_name = tk.StringVar(value=USER.name)
        self.var_username = tk.StringVar(value=USER.username)

        self.lbl_name = ttk.Label(root, text="Name:")
        self.entry_name = ttk.Entry(root, textvariable=self.var_name)
        self.lbl_username = ttk.Label(root, text="Username:")
        self.entry_username = ttk.Entry(root, textvariable=self.var_username)

        self.lbl_name.grid(row=7, column=0, padx=10, pady=[10,0], sticky="E")
        self.entry_name.grid(row=7, column=1, padx=10, pady=[10,0], sticky="W")
        self.lbl_username.grid(row=8, column=0, padx=10, sticky="E")
        self.entry_username.grid(row=8, column=1, padx=10, sticky="W")

        #########
        # Topic #
        #########
        self.var_topic = tk.StringVar(value=MQTT_TOPIC)

        self.lbl_topic = ttk.Label(root, text="Topic:")
        self.entry_topic = ttk.Entry(root, textvariable=self.var_topic)

        self.lbl_topic.grid(row=9, column=0, padx=10, pady=10, sticky="E")
        self.entry_topic.grid(row=9, column=1, padx=10, pady=10, sticky="W")

    # END __init__

    ##################
    # CONNECT BUTTON #
    ##################
    def btn_connection_clicked(self):
        if (self.btn_connection_title.get() == self.CONNECT):
            self.connect()
        else:
            self.disconnect()

    def connect(self):
        # Publisher Logic
        topic = self.var_topic.get()
        user = User(self.var_name.get(), self.var_username.get())
        self.pub.connect(topic, user)

        # Update GUI
        self.btn_connection_title.set(self.DISCONNECT)
        self.btn_publish.config(state=tk.NORMAL)
        self.entry_name.config(state=tk.DISABLED)
        self.entry_username.config(state=tk.DISABLED)
        self.entry_topic.config(state=tk.DISABLED)
        
    def disconnect(self):
        # Publisher Logic
        self.pub.disconnect()

        # Update GUI
        self.btn_connection_title.set(self.CONNECT)
        self.btn_publish_title.set(self.START_PUBLISHING)
        self.btn_publish.config(state=tk.DISABLED)
        self.entry_name.config(state=tk.NORMAL)
        self.entry_username.config(state=tk.NORMAL)
        self.entry_topic.config(state=tk.NORMAL)

    #################
    # UPDATE BUTTON #
    #################
    def update_heart_sensor(self):
        # Retrieve values from entry fields
        self.min_fluctuation = int(self.var_min_fluctuation.get())
        self.max_fluctuation = int(self.var_max_fluctuation.get())

        # Validation
        isValid = False
        if (self.min_fluctuation < self.max_fluctuation):
            isValid = True
        else:
            isValid = False
            messagebox.showerror('Validation Error', 'Error: Cannot Update Data Range! Make sure min range data is smaller than max data.')

        # Update sensor
        if isValid:
            self.pub.update_sensor(self.state_var.get(), self.min_fluctuation, self.max_fluctuation) 

    ##################
    # PUBLISH BUTTON #
    ##################
    def btn_publish_clicked(self):
        if (self.btn_publish_title.get() == self.START_PUBLISHING):
            self.start_publishing()
        else: 
            self.stop_publishing()

    def start_publishing(self):
        # Publisher Logic
        self.pub.start_publish()

        # Update GUI
        self.btn_publish_title.set(self.STOP_PUBLISHING)

    def stop_publishing(self):
        # Publisher Logic
        self.pub.stop_publish()

        # Update GUI
        self.btn_publish_title.set(self.START_PUBLISHING)



# Function to run the GUI 
def start_publisher():
  root = tk.Tk()
  gui = HeartBeatPublisherGUI(root)
  root.mainloop()  

if __name__ == '__main__':
  start_publisher()

