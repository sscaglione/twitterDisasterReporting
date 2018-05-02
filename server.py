from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        if "all" in str(self.path):
            events = self.get_all_events()
        else:
            logging.info('Retrieving all events...\n')
            events = self.get_events()
        self.wfile.write(json.dumps(events).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))

    def get_events(self):
        events_buffer = []
        with open("events.txt") as f:
            with open("events_old.txt", "a+") as out:
                for line in f:
                    out.write(line)
                    line = line.rstrip().split("\t")
                    events_buffer.append([line[0], line[-1]])
        with open("events.txt", "w+") as f:
            f.write("")
        return events_buffer
    def get_all_events(self):
        events_buffer = []
        with open("events_old.txt") as f:
            for line in f:
                line = line.rstrip().split("\t")
                events_buffer.append([line[0], line[-1]])
        return events_buffer


def run(server_class=HTTPServer, handler_class=S, port=8080):
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
