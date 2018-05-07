"""
Server for front end to connect to, interfaces with EventDetect

Note: Currently EventDetect and the server are interfacing by file I/O. It is a goal to rewrite this code to use sockets.
Due to having 2 scripts using the same file, files are opened with os.O_NONBLOCK. This may not work on non-Linux systems.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import os

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        #Log request, handle request
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        if "all" in str(self.path):
            #GET /all retrieves all archieved events
            events = self.get_all_events()
        else:
            #GET / retrieves events still in queue
            logging.info('Retrieving all events...\n')
            events = self.get_events()
        self.wfile.write(json.dumps(events).encode('utf-8'))

    def do_POST(self):
        #Log post requests
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

    def get_events(self):
        #Read events from queue, write events to archive file, return events to be sent to front end
        events_buffer = []
        with open("events.txt", "r", os.O_NONBLOCK) as f:
            with open("events_old.txt", "a+") as out:
                for line in f:
                    out.write(line)
                    line = line.rstrip().split("\t")
                    events_buffer.append(line)
        with open("events.txt", "w+", os.O_NONBLOCK) as f:
            f.write("")
        return events_buffer
    def get_all_events(self):
        #Read events from archive file, return events to be sent to front end
        events_buffer = []
        with open("events_old.txt") as f:
            for line in f:
                line = line.rstrip().split("\t")
                events_buffer.append(line)
        return events_buffer


def run(server_class=HTTPServer, handler_class=S, port=8080):
    #Clear archive file on server startup
    with open("events_old.txt", "w+") as f:
        f.write("")

    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')

if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
