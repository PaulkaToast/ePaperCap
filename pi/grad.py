#!/usr/bin/python
# -*- coding:utf-8 -*-

import epd7in5b
import time
from PIL import Image, ImageDraw, ImageFont
import traceback
import bluetooth
import select
from threading import Thread


# list of filenames in order of slideshow
filenames = [   
        'monad', 
        '2019', 
        'leaps', 
        'lwsn',
        'map']

# driver variables
sleeptime = 3
epd = epd7in5b.EPD()
epd.init()

def is_an_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

class Cap:
    def __init__(self):
        self.slide_show = True
        self.display_index = 0
        self.previous_index = -1
        self.queue_index = 0

    def clear_screen(self):
        try:
            # initial full clear
            print("Clear...")
            epd.Clear(0xFF)
        except:
            print('traceback.format_exc():\n%s',traceback.format_exc())
            exit()

    def display_image(self, filename):
        try:
            HBlackimage = Image.open(filename + '-b.bmp')
            HRedimage = Image.open(filename + '-y.bmp')
            epd.display(epd.getbuffer(HBlackimage), epd.getbuffer(HRedimage))
        except:
            print('traceback.format_exc():\n%s',traceback.format_exc())
            exit()

    def handle_connection(self):
        server_socket=bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        port = 1
        server_socket.bind(("",port))
        server_socket.listen(1)
     
        while True:
            client_socket, address = server_socket.accept()
            print 'Accepted connection from', address
            ready = select.select([client_socket], [], [], 30)

            while ready[0]:
                self.handle_input(server_socket, client_socket)
                ready = select.select([client_socket], [], [], 30)

            client_socket.close()

    def handle_input(self, server_socket, client_socket):       
        data = client_socket.recv(1024)
        data = data.strip()
        print 'Received: %s' % data
        if data == "h" or data == "help":
            print ("Help")
            client_socket.send("<l> - list\n")
            client_socket.send("<s> - display slideshow\n")
            client_socket.send("<int> - display image of index int\n")  

        elif data == "l" or data == "list":
            for i, f in enumerate(filenames):
                msg = str(i) + " - " + f + "\n"
                client_socket.send(msg)

        elif data == "s" or data == "slideshow":
            client_socket.send("slideshow mode\n")
            self.slide_show = True

        elif is_an_int(data) == True:
            index = int(data)
            if index < len(filenames):
                client_socket.send("displaying image %s\n" % index)
                self.queue_index = index
                self.slide_show = False
            else:
                client_socket.send("Invalid index: use <h> or <help> for help\n") 
        else:
            client_socket.send("Invalid input: use <h> or <help> for help\n")

# create an instance of the driver  
d = Cap()

# create thread to handle bluetooth communications
t = Thread(target=d.handle_connection)
t.setDaemon(True)
t.start()

# do a full clear
d.clear_screen()

while True:
    if d.previous_index != d.display_index: 
        d.previous_index = d.display_index
        d.display_image(filenames[d.display_index])
        time.sleep(sleeptime)
    else:
        time.sleep(sleeptime)
        
    if d.slide_show:
        d.display_index = (d.display_index + 1) % len(filenames)
    else:
        d.display_index = d.queue_index
