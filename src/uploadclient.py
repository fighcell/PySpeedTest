# -*- coding: utf-8 -*-
"""
Created on Thu Jan 25 20:07:11 2018

@author: Misha
"""

import socket
import sys

from settings import REC_FILE, UPLOAD_URLS, UPLOAD_PORT

# solution for issue #16
if sys.version_info[0] == 2:
    def encoder(string):
        return string.encode('ascii')
else:
    def encoder(string):
        return bytes(string, 'ascii')


class Uploader(object):

    def __init__(self, handler=None):
        self.handler = handler
        self.lines = None
        self.socket = None
        self.has_connection = False

    def establish_connection(self):
        print('Beginning connection searching on port ' + str(UPLOAD_PORT))

        for url in UPLOAD_URLS:
            try:
                self.set_label(1, url + ":" + str(UPLOAD_PORT))
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(30)  # it's slow...
                self.socket.connect((url, int(UPLOAD_PORT)))
                self.has_connection = True
                print("Connected to " + url + ":" + str(UPLOAD_PORT))
                break

            except (socket.gaierror, socket.timeout) as exc:
                # Welp, that one didn't work... keep going!
                print("Couldn't connect to {}".format(url))
                messagebox.showerror(exc.args[0])

        return self.has_connection

    def send_data(self):
        if not self.has_connection:
            raise ValueError("Can't upload data with no connection!")

        print("Reading file for data to upload")
        with open(REC_FILE, 'r') as infile:
            self.lines = infile.readlines()


        for line in self.lines:
            self.set_label(2, line)
            encoded = encoder(line)
            self.socket.sendall(encoded)

        self.set_label(2, 'Clearing file')
        with open(REC_FILE, 'w') as handle:
            handle.write('')

    def upload(self):
        self.establish_connection()

        if not self.has_connection:
            print("===> Unable to connect!")

        self.send_data()
        print("===> Sent data successfully!")
