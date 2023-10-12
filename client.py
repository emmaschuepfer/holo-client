import asyncio
import PySimpleGUI as sg
import socket
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

ip_holo_1 = '192.168.0.100' #HOLOLENS 1 TPLink
ip_holo_2 = '192.168.178.38' #HOLOLENS 1 Hermannsklause

ips = {
    "HOLO_OPT_1": ip_holo_1, 
    "HOLO_OPT_2": ip_holo_2 
}

ip = ""

connection_attempts = 0
connected = False

start_time = time.time()
delta = 0

async def tcp_echo_client(loop):
    print("Trying to connect to: "+ ip +":" + "65432")
    reader, writer = await asyncio.open_connection(ip, 65432)

    print('Connected to Hololens, starting application')
    global connected 
    global start_time
    global connection_attempts
    connected = True
    start_time = time.time()
    #writer.write(message.encode())

    while True: 
        await asyncio.sleep(1)
        data = await reader.read(100)

        print('Received: %r' % data.decode())

        if "Ending" in data.decode():
            print('Closing the socket')
            writer.close()
            connected = False
            connection_attempts = 0
            return 'DONE!'
            # loop.stop()
            

def start_server_async(ip):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    # loop = asyncio.get_event_loop()
    loop.run_until_complete(tcp_echo_client(loop))
    loop.close()
    return 'DONE!'
    
sg.theme('LightGrey6')

layout_l = [
   [
      sg.Col([
         [sg.Text('ℹ', font='_ 20', expand_x=True, text_color="black")]
      ]),
      sg.Col([
         [sg.Text('Pc and hololens must be connected \nto the same network (TPLink)', font='_ 14', expand_x=False ,text_color="black")],
      ])  
    ], 
    [
      sg.Col([
         [sg.Text('ℹ', font='_ 20', expand_x=True, text_color="black" )]
      ]),
      sg.Col([
         [sg.Text('Device numbers can be found \non the backside of the devices', font='_ 14', expand_x=False ,text_color="black")],
      ])  
    ], 
    [
      sg.Col([
         [sg.Text('ℹ', font='_ 20', expand_x=True, text_color="black" )]
      ]),
      sg.Col([
         [sg.Text('Application must run on hololens \nbefore connecting to it', font='_ 14', expand_x=False ,text_color="black")],
      ])  
    ],
    [
      sg.Col([
         [sg.Text('ℹ', font='_ 20', expand_x=True, text_color="black" )]
      ]),
      sg.Col([
         [sg.Text('To find device ip address use hololens \nvoice command "what is my ip address?"', font='_ 14', expand_x=False ,text_color="black")],
      ])  
    ],
     [
      sg.Col([
         [sg.Text('ℹ', font='_ 20', expand_x=True, text_color="black" )]
      ]),
      sg.Col([
         [sg.Text('Check console output for more info', font='_ 14', expand_x=False ,text_color="black")],
      ])  
    ],
]
   
layout_r = [
   [sg.Text('Which Hololens device do you want to connect to?', font='_ 16', pad=((0, 0), (0, 20)), expand_x=True)],
#    [sg.Combo(names, font=('_', 14),  expand_x=True, enable_events=True,  readonly=False, key='-COMBO-')],
   [sg.Radio('Device 1', 1, font='_ 14', key='HOLO_OPT_1', enable_events="True", size=(10, 20)), sg.Text(ip_holo_1, font='_ 14', text_color="grey")],
   [sg.Radio('Device 2', 1, font='_ 14', key='HOLO_OPT_2', enable_events="True", size=(10, 20)), sg.Text(ip_holo_2, font='_ 14', text_color="grey")],  
   [sg.Radio('Other:', 1, font='_ 14', key='HOLO_OPT_3', enable_events="True", size=(10, 20)), sg.Input(disabled=True, key='HOLO_OPT_3_INPUT', font='_ 14', size=(16, 20), disabled_readonly_background_color="white", background_color="#f2f2f2", text_color="grey")],
   [sg.Button('Connect', key="CONNECT",button_color=("#43A047", "#f2f2f2"),font=('_', 14), pad=((0, 0), (20, 20)))], 
   [sg.Text('Console Output:', font='_ 14', size=(50,0)), sg.Text(font='_ 14', expand_x=True, key="PASSED_TIME", justification="r",text_color="grey", size=(10,0))],
   [sg.Output(size=(60,10), key="OUTPUT", font='_ 14', text_color="black", background_color="#f2f2f2", sbar_background_color="#E1E1E1", sbar_arrow_color="grey", sbar_trough_color="#f2f2f2")],
   [sg.Button('Clear Console', key="CLEAR", button_color=("grey", "#f2f2f2"), font=('_', 14), pad=((0, 20), (20, 20))), sg.Button('Exit Program', button_color=("red", "#f2f2f2"), key="EXIT", font=('_', 14), pad=((0, 0), (20, 20)))], 
]

layout = [
    [sg.Col(layout_l, pad=(40)), sg.VSeperator(color="grey"), sg.Col(layout_r, pad=(30))]
    ]


window = sg.Window('ReSy: Hololens Server Connection', layout, grab_anywhere=True, finalize=True)

while True:
    event, values = window.read(timeout=100)
    if connected == True:
        delta = round((time.time()-start_time)*1000)
        window['PASSED_TIME'].update(f'{delta//1000//60:02d}:{delta//1000%60:02d}', text_color="#a6b1bd" )

        if delta//1000 >= (200) and delta//1000 <= (215):
            window['PASSED_TIME'].update(f'{delta//1000//60:02d}:{delta//1000%60:02d}', text_color="#ff9100" )


    # print(event, values)
    if event in (sg.WIN_CLOSED, 'EXIT'):
        break
    if event == '-COMBO-':
        ch = sg.popup_yes_no("Do you want to restart?", title="YesNo")
    if event == 'HOLO_OPT_3':
        if values["HOLO_OPT_3"] == True:
            window['HOLO_OPT_3_INPUT'].Update(disabled=False)
    if event == 'HOLO_OPT_1' or event == 'HOLO_OPT_2':
        window['HOLO_OPT_3_INPUT'].Update(disabled=True)
    if event == 'CONNECT' and connection_attempts == 0:
        connection_attempts += 1
        if values["HOLO_OPT_1"] == True:
            ip = ips['HOLO_OPT_1']
            print("You chose hololens device 1 with ip: " + ip)

            window.perform_long_operation(lambda : start_server_async(ip), '-END KEY-')
        elif values["HOLO_OPT_2"] == True:
            ip = ips['HOLO_OPT_2']
            print("You chose hololens device 2 with ip: " + ip)

            window.perform_long_operation(lambda : start_server_async(ip), '-END KEY-')

        elif values["HOLO_OPT_3"] == True and values["HOLO_OPT_3_INPUT"] != "":
            ip = values["HOLO_OPT_3_INPUT"]
            try:
                socket.inet_aton(ip)
                print("You chose custom device with ip: " + ip)

                window.perform_long_operation(lambda : start_server_async(ip), '-END KEY-')
            except:
                print("Please enter valid IP Address")

                connection_attempts = 0

        elif values["HOLO_OPT_3"] == True and values["HOLO_OPT_3_INPUT"] == "":
            print("Please enter valid IP Address")
            connection_attempts = 0

        else: 
            print("Choose which device to connect to")
            connection_attempts = 0
    
    elif event == 'CONNECT' and connection_attempts > 0:

        if connected == True:
            print("You already are connected to a device")
        
        if connected == False:
            print("Seems like you already tried to connect to a device")

    if event == "CLEAR":
        window.FindElement('OUTPUT').Update('')
    elif event == '-END KEY-':
            return_value = values[event]
            
window.close()


# loop = asyncio.get_event_loop()

# loop.run_until_complete(tcp_echo_client(loop))
# loop.close()
