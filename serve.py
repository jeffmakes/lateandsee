import http.server
import socketserver
import threading

class ThreadedTCPServer(socketserver.ThreadingMixIn,socketserver.TCPServer): pass

class Serve:
    def __init__(self, port=8000):
        self.port = port

        Handler = http.server.SimpleHTTPRequestHandler

        httpd = ThreadedTCPServer(("", port), Handler)
        print("serving at port", port)

        server_thread = threading.Thread(target=httpd.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()

