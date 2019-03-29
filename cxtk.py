from tkinter import Tk, Canvas

class CanvasContainer():
    def __init__(self, total_W, total_H):
        self.master = Tk()
        self.canvas = Canvas(self.master, width=total_W, height=total_H)
        self.canvas.pack()
        self.elements = dict()
    def updateCanvas(self, is_alive):
        if is_alive:
            self.canvas.update()
            self.master.update_idletasks()
        else:
            self.canvas.destroy()
            self.master.destroy()
    def getElements(self):
        ret = list()
        for key in self.elements:
            ret.append([str(key),self.elements[key]])
        return ret
    def remove(self, key):
        if key in self.elements.keys():
            for val in self.elements[key]:
                self.canvas.delete(val)
            self.elements.pop(key)
            return True
        else:
            return False
    def removeMany(self, keylist):
        ks = [""]
        if "*" in keylist:
            ks = list(self.elements.keys())
        else:
            ks = keylist.copy()
        count = 0
        for key in ks:
            count += 1 if self.remove(key) else 0
        return count
    def create_border(self, prepad):
        pad = prepad-3
        width = int(self.canvas.config()["width"][4])
        height = int(self.canvas.config()["height"][4])
        self.canvas.create_line(pad,pad, width-pad,pad, width-pad,height-pad, pad,height-pad, pad,pad )
    def create_line(self, plist, name):
        if str(name) not in self.elements.keys():
            newval = list()
            newval.append(self.canvas.create_line(*plist))
            self.elements[str(name)] = newval
        else:
            self.elements[str(name)].append(self.canvas.create_line(*plist))
    def create_oval(self, plist, name="dots"):
        if str(name) not in self.elements.keys():
            newval = list()
            newval.append(self.canvas.create_oval(*plist))
            self.elements[str(name)] = newval
        else:
            self.elements[str(name)].append(self.canvas.create_oval(*plist))
