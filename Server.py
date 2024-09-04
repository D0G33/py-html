import base64
from http.server import *
import atexit
import urllib.request
import os
import socket
import zipfile as zf
import shutil

hostIp = socket.gethostbyname(socket.gethostname())

servers = []

pyPath = os.getcwd()

# Content Type Dictonary
fileExDict = {"zip":"application/zip",
              "ogg":"application/ogg",
              "xml":"application/xml",
              "pdf":"application/pdf",
              "json":"application/json",
              "mp3":"audio/mpeg",
              "wav":"audio/x-wav",
              "gif":"image/gif",
              "jpg":"image/jpeg",
              "png":"image/png",
              "tiff":"image/tiff",
              "ico":"vnd.microsoft.icon",
              "txt":"text/plaintext",
              "html":"text/html",
              "mp4":"video/mp4",
              "bat":"text/plaintext"}

#hostname
hostname = hostIp

#sets file seperators
if os.name == "nt":
    fileSeperator = "\\"
else:
    fileSeperator = "/"

print(hostIp)

class exit:
    def __init__(self,server):
        self.server = server

    def exitFunc(self):
        try:
            self.server.server_exit()
        except:
            print('"At Exit" Detected Server is Already Closed')

def runWebServer(fileDirs,port=27554):
    class createClass(BaseHTTPRequestHandler):
        def do_GET(self):
            # defaults

            contents = "empty"
            contentType = "text/html"
            # reset Servers
            for i in servers:
                i.close_server()
            #command handler
            cmd = self.path
            cmd = cmd.replace("/","",1)

            print(cmd)
            if cmd == "": cmd = "main"
            f = open(fileDirs[cmd],"rb")
            contents = f.read()
            f.close()
            contentType = fileExDict[fileDirs[cmd].split('.')[-1]]

            self.send_response(200)
            self.send_header("Content-type", contentType)
            self.end_headers()
            self.wfile.write(contents)

    server_address = ('', port)
    server = HTTPServer(server_address,createClass)
    ex = exit(server)
    atexit.register(ex.exitFunc)
    try:
        server.serve_forever()
    except:
        print("Server Now Closing")

if __name__ == "__main__":

    #createDirFromZip(pyPath + fileSeperator+"FileServerFiles"+fileSeperator+"output-2.zip","FileServerFiles")
    fileDirs = {"main":"main.html",
            "favicon.ico":"favicon.ico",
            "anger":"catmemes\\angerCat.jpg",
            "happy":"catmemes\\happy-catto-cats.gif"}
    runWebServer(fileDirs)
