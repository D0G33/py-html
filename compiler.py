from collections import defaultdict
from email.policy import default


def rmWQ(string,chara):
    inQuotes = False
    out = ""
    for i in string:
        if i == '"':
            inQuotes = not inQuotes
        if inQuotes or i != chara:
            out += i

    return out

def splitWQ(string,sep):
    inQuotes = False
    out = [""]
    for i in string:
        if i == '"':
            inQuotes = not inQuotes
        #print(inQuotes)
        if inQuotes or i != sep:
            out[-1] += i
        elif i == sep:
            out.append("")
    return out

def eCmd(line):
    parts = splitWQ(line,".")
    out1 = parts[0]
    out2 = splitWQ(parts[1],"=")[0]
    out3 = splitWQ(parts[1],"=")[1].replace('"',"")
    return [out1, out2, out3]

def printDict(dict):
    for i in dict:
        print(i + ": " + dict[i])

class htmlObj:
    def __init__(self,tag="p"):
        self.tag = tag
        self.content = ""
        self.attributes = {}
        self.img = ""
    def __str__(self):
        atr = " "
        for i in self.attributes:
            atr += i + "=" + self.attributes[i]
            atr += " "
        if atr == " ": atr = ""
        if self.img != "":
            return "<" + self.tag + atr + ">" + self.img + self.content + "</" + self.tag + ">"
        return "<" + self.tag + atr + ">" + self.content + "</" + self.tag + ">"
    def __add__(self,other):
        return other + str(self)
    def __radd__(self,other):
        return other + str(self)

class htmlImg:
    def __init__(self,url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS-RcH3_rFP8ZmSEgjhZy5pv4O4bLl-SwZGsA&s"):
        self.tag = "img"
        dStyle = "width:48px;height:48px"
        self.attributes = {"src":url,"style":dStyle}

    def __str__(self):
        atr = " "
        for i in self.attributes:
            atr += i + "=" + self.attributes[i]
            atr += " "
        if atr == " ": atr = ""
        return "<"+self.tag+ atr+">"
    def __add__(self,other):
        return other + str(self)
    def __radd__(self,other):
        return other + str(self)
# Builtins
link = htmlObj()
link.tag = "a"
link.attributes["href"] = "https://www.google.com"
link.content = "Connect To Google!"

class pyml:
    def __init__(self,dir):
        if dir.split(".")[-1] != "pyml":
            exit("Selected File is not a PYML File.")
        f = open(dir,"r")
        self.content = f.read()
        f.close()

        self.htmlHeaders = ["<!DOCTYPE html>","<html>"]
        self.htmlFooters = ["</html>"]

        self.head = {"title":"PYML DEFAULT SCRIPT"}
        self.body = {}

        self.images = {}
        self.references = {"link":link}

    def createFile(self,name="main"):
        f = open(name+".html",'w')
        for i in self.htmlHeaders:
            f.write(i + "\n")

        f.write("<head>\n")
        for i in self.head:
            f.write("\t<"+i+">"+self.head[i]+"</"+i+">\n")
        f.write("</head>\n")

        f.write("<body>\n")
        for i in self.body:
            f.write("\t<" + i + ">" + self.body[i] + "</" + i + ">\n")
        for i in self.comps:
            f.write("\t"+self.comps[i]+"\n")
        f.write("</body>\n")

        for i in self.htmlFooters:
            f.write(i + "\n")

    def populate(self):
        noWhite = rmWQ(self.content.replace("\t",""),'\n')
        keepQuotes = rmWQ(noWhite," ")
        commands = keepQuotes.split(";")
        commands.pop(-1)

        #Create Includes
        for c, i in enumerate(commands):
            if i[0] == ">":
                f = open(i[1:]+".pyin",'r')
                content = f.read()
                f.close()
                noWhite = rmWQ(content.replace("\t", ""), '\n')
                keepQuotes = rmWQ(noWhite, " ")
                externalCommands = keepQuotes.split(";")
                externalCommands.pop(-1)
                commands[c] = externalCommands[0]
                exMf = externalCommands[1:]
                for i in range(len(exMf)):
                    commands.insert(c+1, exMf[len(exMf)-i-1])


        #Remove Comments
        i = 0
        while i < len(commands):
            if commands[i][0] == "#":
                commands.pop(i)
                i -= 1
            i += 1

        self.comps = {}
        for i in commands:
            parts = splitWQ(i,".")

            if parts[0] == "head":
                self.head[parts[1].split("=")[0]] = parts[1].split("=")[1].replace('"',"")

            elif i[0] == "$":
                print(i[1:] + ": Added to Components!")
                self.comps[i[1:]] = htmlObj()

            elif i[0] == "&":
                self.references[i[1:]] = self.comps[i[1:]]
                self.comps.pop(i[1:])
                print(i[1:] + " Moved to Refs")

            elif i[0] == "+":
                self.images[i[1:]] = htmlImg()
                print(i[1:] + " Image Created")

            elif "<<" in i:
                names = i.split("<<")
                self.comps[names[0]] = self.references[names[1]]
                print(names[0] + " set to reference " + names[1])

            else:
                if parts[1] == "a" or parts == "attributes":
                    print(parts)
                    if parts[2] != "del":
                        partSplit = parts[2].split("=")
                        self.comps[parts[0]].attributes[partSplit[0]] = partSplit[1].replace('"',"")
                else:
                    cmd = eCmd(i)

                #Editting Image
                if cmd[0] in self.images:
                    print(cmd)
                    if cmd[1] == "url":
                        self.images[cmd[0]].attributes["src"] = cmd[2]
                    if cmd[1] == "style":
                        self.images[cmd[0]].attributes["style"] = cmd[2]

                else:
                    if cmd[1] == "content":
                        self.comps[cmd[0]].content = cmd[2]
                    if cmd[1] == "tag":
                        self.comps[cmd[0]].tag = cmd[2]
                    if cmd[1] == "img" or cmd[1] == "image" or cmd[1] == 'i':

                        self.comps[cmd[0]].img = self.images[cmd[2]]


        print("\n\nComponents:")
        for i in self.comps:
            print(i + ": " + self.comps[i])


testDoc = pyml("main.pyml")
testDoc.populate()
testDoc.createFile("main")