import time
from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = 'localhost'
PORT_NUMBER = 9000


class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        paths = {
            '/lbon': {'status': 200},
            '/lboff': {'status':200 },
            '/baz': {'status': 404},
            '/qux': {'status': 500}
        }

        if self.path in paths:
            print("path is ",self.path)
            self.respond(paths[self.path])
        else:
            print("path is ",self.path)
            self.respond({'status': 500})
    
    def killOldProcess(self):
        import subprocess,signal
        p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        out, err = p.communicate()
        for line in out.splitlines():
            if 'lightboxcontroller' in line:
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)

    def handlePath(self,path):
        if path == '/lbon':
           import lightboxcontroller as lb
           lb.setup()
           lb.demoProtocol(True)
           return 'handled lbon'
        if path == '/lboff':
           # seriously bad hack
           self.killOldProcess()
           import lightboxcontroller as lb
           lb.setup()
           lb.reset()
           return 'handled lboff'
        
    def handle_http(self, status_code, path):
        mess=self.handlePath(path)
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        content = '''
        <html><head><title>Result.</title></head>
        <body><p>{}p>
        <p>You accessed path: {}</p>
        </body></html>
        '''.format(mess,path)
        return bytes(content, 'UTF-8')

    def respond(self, opts):
        response = self.handle_http(opts['status'], self.path)
        self.wfile.write(response)

if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))
