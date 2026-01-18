################ Credits ######################################################
"""
Created by Satyar Sh
https://github.com/satyarsh

Modified by Catupeloco
https://github.com/catupeloco

tkterminal by Saadmairaj
https://github.com/Saadmairaj/tkterminal
"""
###############################################################################


################# Librarys ####################################################
import tkinter
import os
import sys
from tkinter import messagebox
from tkinter import StringVar
from tkinter import PhotoImage
from tkinter import ttk
from tkinter import Menu
import subprocess
import sqlite3
from tkterminal import Terminal
###############################################################################


################# Settings ####################################################
this_user = os.popen('echo -n "$USER"').read()

tk = tkinter.Tk()
tk.geometry('1493x605')
tk.title("Cliente VPN Openconnect")
tk.iconphoto(True,PhotoImage(file="ethernet-port-icon.png"))
tk.config(bg='#444444')
darkgray = "#444444"
#tk.resizable(False, False)
###############################################################################


################# Style #######################################################
style = ttk.Style()

style.configure('W.TButton', font =('calibri', 10,),
                            foreground="white",background="black")

style.configure('L.TButton', font =('calibri', 9,),
                            foreground="white",background="black")

style.configure('Welcome.TLabel', font =('calibri', 10,),
                            foreground="white",background=darkgray)

style.configure('CmBox.TButton' , font =('calibri', 10,),
                            foreground="black",background="white")
###############################################################################


################# Variable's ##################################################
pad_general = 50
list_of_usernames = list()
list_of_servers = list()
list_of_passwords = list()
server_field_user_input_var = StringVar()
username_field_user_input_var = StringVar()
password_field_user_input_var = StringVar()
###############################################################################


########### Terminal Window ###################################################
terminal = Terminal(pady=1, padx=1,height=15,
                    width=185,background='black',foreground='green',
                    insertbackground='green')

terminal.grid(row=10,column=0,pady=6,columnspan = 10)
terminal.shell = True
###############################################################################


################## Sqlite Connection ##########################################
try:
    sqliteConnection = sqlite3.connect('database.db')
    cursor = sqliteConnection.cursor()

except sqlite3.Error as error:
    terminal.run_command(f"echo 'Error occurred - {error}'")

sqliteConnection.execute('''CREATE TABLE IF NOT EXISTS Info
        (ID        INT              ,
        Username   TEXT             ,
        Server     TEXT             
                                    );''')
###############################################################################


######## Fetching Data From SQL Table #########################################
cursor.execute("""SELECT * FROM Info""")
rows = cursor.fetchall()
for row in rows:
    list_of_usernames.append(row[1])
    list_of_servers.append(row[2])
###############################################################################


################ Functions ####################################################
def Connection_Func(user_input):
    if user_input == 1:
        try:
            # Only all fields are completed, start vpn connection
            if (password_field_user_input_var.get().strip() and 
                server_field_user_input_var.get().strip() and 
                username_field_user_input_var.get().strip()):

                # Disable input when connecting
                Entry1.config(state='disabled')
                Entry2.config(state='disabled')
                Entry3.config(state='disabled')

                # Disable Connect button
                button1.config(state='disabled')

                # Enable Disconnect button
                button2.config(state='normal')

                # Running main bash script with parameters
                command = (
                    f"./oc-gui.sh start {username_field_user_input_var.get().strip()} "
                    f"{password_field_user_input_var.get().strip()} "
                    f"{server_field_user_input_var.get().strip()} > ./oc-gui.log"
                )

                # subprocess.run blocks execution until the script finishes
                process = subprocess.run(command, shell=True)

                # Check if the script executed successfully (return code 0)
                if process.returncode == 0:
                    # Saving data in database.db
                    checkbox_is_clicked()

                    # Log success to terminal
                    terminal.run_command("cat ./oc-gui.log ; echo 'Connection established successfully'")
                else:
                    # Reenable input when disconnecting
                    Entry1.config(state='normal')
                    Entry2.config(state='normal')
                    Entry3.config(state='normal')

                    # Enable Connect button
                    button1.config(state='normal')

                    # Disable Disconnect button
                    button2.config(state='disabled')

                    # If script fails, we do not disable inputs or clear password
                    terminal.run_command(f"echo 'Error: Connection failed with exit code {process.returncode}'")

                # Cleanning password field for rotating passwords and extra security for else
                password_field_user_input_var.set("")
                
            else:
                terminal.run_command("echo 'Error: Debes completar los campos para continuar'")
        
        except Exception:
            terminal.run_command("echo 'Error inesperado al procesar los campos'")

    elif user_input == 3:
        # Reenable input when disconnecting
        Entry1.config(state='normal')
        Entry2.config(state='normal')
        Entry3.config(state='normal')

        # Enable Connect button
        button1.config(state='normal')

        # Disable Disconnect button
        button2.config(state='disabled')

        # Running main Disconnect Button
        password_field_user_input_var.set("")
        terminal.run_command(f"./oc-gui.sh stop; ./oc-gui.sh status")

    elif user_input == 4:
        # Running main Exit Button.
        subprocess.run("./oc-gui.sh stop", shell= True)
        sys.exit()

    elif user_input == 5:
        username_field_user_input_var.set("")
        server_field_user_input_var.set("")
        password_field_user_input_var.set("")
        sqliteConnection.commit()

# Saving server and user in database.db
def checkbox_is_clicked():
    try:
        # Connecting to database.
        sqliteConnection = sqlite3.connect('database.db')
        cursor = sqliteConnection.cursor()

        # Creating tables if they not exists.
        cursor.execute('''CREATE TABLE IF NOT EXISTS Info
             (ID INTEGER PRIMARY KEY AUTOINCREMENT,
              Username TEXT,
              Server TEXT);''')

        # Cleaning old content.
        cursor.execute("DELETE FROM Info")

        # Inserting current content.
        cursor.execute("INSERT INTO Info (Username, Server) VALUES (?, ?)", 
                       (username_field_user_input_var.get(), server_field_user_input_var.get()))

        # Sending data to database.
        sqliteConnection.commit()

    except sqlite3.Error as error:
        # If database is broken.
        terminal.run_command(f"echo 'Error occurred - {error}'")
    
    finally:
        # If database is open, close it.
        if sqliteConnection:
            sqliteConnection.close()

def server_combobox_is_clicked(event):
    username_field_user_input_var.set(list_of_usernames[0])

def username_combobox_is_clicked(event):
    server_field_user_input_var.set(list_of_servers[0])

# Executing "Connect" when pressing enter
def on_enter_key(event):
    # Only if all fields are completed and without empty spaces
    if (server_field_user_input_var.get().strip() and 
        username_field_user_input_var.get().strip() and 
        password_field_user_input_var.get().strip()):

        # Disable input when connecting
        Entry1.config(state='disabled')
        Entry2.config(state='disabled')
        Entry3.config(state='disabled')

        # Disable Connect button
        button1.config(state='disabled')

        # Enable Disconnect button
        button2.config(state='normal')
        
        # Running "Connect"
        Connection_Func(1)
    else:
        # Sending a message if something is empty
        terminal.run_command("echo 'Error: Completa todos los campos antes de presionar Enter'")

###############################################################################


############### Top Left Menu #################################################
# Barra de menú
menubar = Menu(tk)
tk.config(menu=menubar)

file_menu = Menu(
    menubar,
    tearoff = False
)

# Menu archivo
menubar.add_cascade(
    label="Archivo",
    menu=file_menu,
    underline = False
)

file_menu.add_command(
    label='Salir',
    command=tk.destroy
)

exit_menu = Menu(
    menubar,
    tearoff = False
)

# Menu ayuda
menubar.add_cascade(
    label="Ayuda",
    menu=exit_menu
)

exit_menu.add_command(
    label="Acerca",
    command=lambda:messagebox.showinfo('Acerca',
    'Creado por stking68\n  https://github.com/stking68\n\nAdaptado por catupeloco\n  https://github.com/catupeloco',
    icon='info')
)

###############################################################################


label_welcome = ttk.Label(tk , text=f"Bienvenido {this_user}",font=("", 16),style='Welcome.TLabel')
label_welcome.grid(row=0,column=1)

########### Server / Username / Password ######################################
#label_1 = ttk.Label(tk , text="Servidor",font=("", 11),style='L.TButton').grid(row=1,column=0,padx=10,ipady=7)
#Entry1 = ttk.Combobox(tk, values=list_of_servers,font=("",11),textvariable=server_field_user_input_var,style='CmBox.TButton')
#Entry1.bind('<<ComboboxSelected>>', server_combobox_is_clicked)
#Entry1.grid(row=1,column=1,pady=4,ipadx=pad_general)

#label_2 = ttk.Label(tk , text="Usuario",font=("", 11),style='L.TButton').grid(row=2,column=0,padx=10,ipady=7)
#Entry2 = ttk.Combobox(tk, values=list_of_usernames,font=("",11),textvariable=username_field_user_input_var,style='CmBox.TButton')
#Entry2.bind('<<ComboboxSelected>>', username_combobox_is_clicked)
#Entry2.grid(row=2,column=1,pady=4,ipadx=pad_general)

#label_3 = ttk.Label(tk , text="Contraseña",font=("", 11),style='L.TButton').grid(row=3,column=0,padx=10,ipady=7)
#Entry3 = ttk.Entry(tk, show="*",font=("",11),textvariable=password_field_user_input_var,style='CmBox.TButton')
#Entry3.grid(row=3,column=1,pady=4,ipadx=pad_general)

if list_of_servers:
    server_field_user_input_var.set(list_of_servers[0])

if list_of_usernames:
    username_field_user_input_var.set(list_of_usernames[0])

password_field_user_input_var.set("")

label_1 = ttk.Label(tk, text="Servidor", font=("", 11), style='L.TButton').grid(row=1, column=0, padx=10, ipady=7)
Entry1 = ttk.Entry(tk, font=("", 11), textvariable=server_field_user_input_var)
Entry1.grid(row=1, column=1, pady=4, ipadx=pad_general)

label_2 = ttk.Label(tk, text="Usuario", font=("", 11), style='L.TButton').grid(row=2, column=0, padx=10, ipady=7)
Entry2 = ttk.Entry(tk, font=("", 11), textvariable=username_field_user_input_var)
Entry2.grid(row=2, column=1, pady=4, ipadx=pad_general)

label_3 = ttk.Label(tk, text="Contraseña", font=("", 11), style='L.TButton').grid(row=3, column=0, padx=10, ipady=7)
Entry3 = ttk.Entry(tk, show="*", font=("", 11), textvariable=password_field_user_input_var)
Entry3.grid(row=3, column=1, pady=4, ipadx=pad_general)

# Call connect function on enter
Entry3.bind('<Return>', on_enter_key)

###############################################################################


########### Button's ##########################################################
button1 = ttk.Button(tk , text="Conectar",command=lambda:Connection_Func(1),style='W.TButton')
button1.grid(row=4,column=1)

button2 = ttk.Button(tk , text="Desconectar",command=lambda:Connection_Func(3),style='W.TButton', state='disabled')
button2.grid(row=6,column=1)

button_quit = ttk.Button(tk , text="Salir",command=lambda:Connection_Func(4),style='W.TButton')
button_quit.grid(row=9,column=1)

button_purge_database = ttk.Button(tk , text="Limpiar",command=lambda:Connection_Func(5),style='W.TButton')
button_purge_database.grid(row=8,column=1)

#checkbox_saveinfo = ttk.Button(tk, text="Save Account Info",
#                                    command=checkbox_is_clicked,
#                                    style='W.TButton',
#                                    )

#checkbox_saveinfo.grid(row=7,column=1)

###############################################################################


################# Lógica de Auto-foco #########################################
# Verificamos si los campos cargados desde la DB tienen contenido
if server_field_user_input_var.get().strip() and username_field_user_input_var.get().strip():
    # Si ambos están listos, el cursor va a la contraseña
    Entry3.focus_set()
else:
    # Si falta alguno (o ambos), el cursor va al servidor
    Entry1.focus_set()
###############################################################################

tk.mainloop()

tk.mainloop()
cursor.close()
