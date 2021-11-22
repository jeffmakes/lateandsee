import http.server
import socketserver
import threading

class ThreadedTCPServer(socketserver.ThreadingMixIn,socketserver.TCPServer): pass

class Serve:
    def __init__(self, port=8000):
        self.port = port

        Handler = http.server.SimpleHTTPRequestHandler

        self.httpd = ThreadedTCPServer(("", port), Handler)
        print("Serving at port", port)

        self.server_thread = threading.Thread(target=self.httpd.serve_forever)
        # Exit the server thread when the main thread terminates
        self.server_thread.daemon = True
        self.server_thread.start()

    def stop(self):
        self.httpd.shutdown()


