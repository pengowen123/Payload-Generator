from Tkinter import *
from random import randint, uniform

class Class(object):
   def __init__(self, passengers, cargo, weights):
      self.weight = sum([weights[t] for t in passengers])
      self.cargo = cargo
      self.infant_count = passengers.count(0)
      self.child_count = passengers.count(1)
      self.adult_count = passengers.count(2)

# Taken from stackoverflow.com/questions/3679694/
def weighted_choice(choices):
   total = sum(w for c, w in choices)
   r = uniform(0, total)
   upto = 0
   for c, w in choices:
      if upto + w >= r:
         return c
      upto += w
   assert False, "Shouldn't get here"

def generate(mtow,
             fuel,
             min_cargo,
             max_cargo,
             min_pass,
             max_pass,
             classes,
             adults_only,
             units):

   # Passenger weights
   if units == 1:
      weights = [
         0,
         88,
         220
         ]
   else:
      weights = [
          0,
          40,
          100
          ]

   cargo = randint(min_cargo, max_cargo)
   weight = fuel + cargo
    
   # Generate random passengers
   # 0 = infant
   # 1 = child
   # 2 = adult
   passenger_count = randint(min_pass, max_pass)
   passengers = []
    
   for x in xrange(passenger_count):
      if adults_only:
         p = 2
      else:
         p = weighted_choice([(0, 1.0), (1, 4.0), (2, 30.0)])
      
      weight += weights[p]

      if weight > mtow:
         break
        
      passengers.append(p)

   # Sort passengers into classes
   max_per_class = [c for c in classes]
   class_count = len(classes)
   classes = [[] for c in xrange(class_count)]

   for p in passengers:
      class_weights = [float(x) for x in max_per_class]
      c_rand = weighted_choice([(c, class_weights[c]) for c in xrange(class_count)])
        
      for c in xrange(class_count):
         c_ = c
         while len(classes[c_]) > max_per_class[c_]:
            c_ += 1

            if c_ >= class_count:
               c_ = 0
            elif c_ == c:
               break

         c = c_
            
         if len(classes[c]) < max_per_class[c] and c == c_rand:
            classes[c].append(p)

   cargo_split = [0 for x in xrange(class_count)]

   i = 0
   for x in xrange(cargo):
      cargo_split[i] += 1
      i += 1

      if i > class_count - 1:
         i = 0

   classes = [Class(c, cargo_split[i], weights) for i, c in enumerate(classes)]

   return cargo, len(passengers), classes

class Preset(object):
   def __init__(self, options):
      if type(options) != list:
         raise Exception
      elif len(options) != 8:
         raise Exception
      
      self.options = options

class TextField(object):
   def __init__(self, label, x, y, width=7, is_int=True, is_list=False):
      self.label = Label(master, text=label)
      self.field = Entry(master, width=width, exportselection=0)
      self.label.place(x=x, y=y)
      self.field.place(x=x+100, y=y)
      self.is_int = is_int
      self.is_list = is_list

   def get(self):
      try:
         string = self.field.get()
         if len(string) == 0:
            return None
         elif self.is_int:
            return int(string)
         elif self.is_list:
            return [int(i) for i in string.split(",")]
      except:
         return "False"
         
      return string

   def insert(self, string):
      self.field.delete(0, END)
      self.field.insert(0, string)

class ButtonEasy(object):
   def __init__(self, x, y, text, command):
      self.button = Button(master, text=text, command=command)
      self.button.place(x=x, y=y)

def generate_tk():
   global units
   
   window.delete("text")
   window.delete("err_text")
   window.delete("line")
   
   mtow = fields[0].get()
   fuel = fields[1].get()
   min_cargo = fields[2].get()
   max_cargo = fields[3].get()
   min_pass = fields[4].get()
   max_pass = fields[5].get()
   classes = fields[6].get()
   adults_only = adult_box.get()

   if None in [mtow, fuel, min_cargo, max_cargo, min_pass, max_pass]:
      draw_text("Error: Empty fields", 4, 200, "red", tag="err_text")
      return
   elif "False" in [mtow, fuel, min_cargo, max_cargo, min_pass, max_pass]:
      draw_text("Error: Fields must be numbers", 4, 200, "red", tag="err_text")
      return
   elif classes in [None, "False"]:
      draw_text("Error: Classes must be comma separated numbers", 4, 200, "red", tag="err_text")
      return
   elif len(classes) not in [1, 2, 3]:
      print len(classes)
      draw_text("Error: Must be 1-3 classes", 4, 200, "red", tag="err_text")
      return
   elif min_cargo > max_cargo:
      draw_text("Error: Max. cargo can't be less than min.", 4, 200, "red", tag="err_text")
      return
   elif min_pass > max_pass:
      draw_text("Error: Max. passengers can't be less than min.", 4, 200, "red", tag="err_text")
      return
   elif mtow < fuel + max_cargo:
      draw_text("Error: Weight exceeds MTOW", 4, 200, "red", tag="err_text")
      return
   elif True in [x < 0 for x in [mtow, fuel, min_cargo, max_cargo, min_pass, max_pass, classes]]:
      draw_text("Error: Fields must be greater than 0", 4, 200, "red", tag="err_text")
      return

   cargo, passengers, classes = generate(mtow,
                                         fuel,
                                         min_cargo,
                                         max_cargo,
                                         min_pass,
                                         max_pass,
                                         classes,
                                         adults_only,
                                         units.get()
                                         )

   classes = classes[:3]
   x = 200
   draw_text("Passengers: %s" % passengers, x, 160, "blue")
   draw_text("Cargo: %s" % cargo, x+120, 160, "blue")
   
   for i, c in enumerate(classes):
      output_class(c, i+1, x, 20)
      x += 120

def draw_text(string, x, y, color, tag="text"):
   window.create_text((x, y), text=string, fill=color, anchor=NW, tag=tag)

def output_class(c, c_id, x, y):
   draw_text("Class %s" % c_id, x, y, "blue")
   window.create_line((x, y+15, x+70, y+15), fill="darkblue", tag="line")
   draw_text("Pax wt:   %s" % c.weight, x, y+20, "blue")
   draw_text("Cargo:   %s" % c.cargo, x, y+40, "blue")
   draw_text("Adults:   %s" % c.adult_count, x, y+60, "blue")
   draw_text("Children: %s" % c.child_count, x, y+80, "blue")
   draw_text("Infants:  %s" % c.infant_count, x, y+100, "blue")

def load_settings(mtow,
                  min_cargo,
                  max_cargo,
                  min_pass,
                  max_pass,
                  classes,
                  units_):
   try:
      fields[0].insert(mtow.replace(" ", ""))
      fields[1].insert(0)
      fields[2].insert(0)
      fields[3].insert(max_cargo.replace(" ", ""))
      fields[4].insert(0)
      fields[5].insert(max_pass.replace(" ", ""))
      fields[6].insert(classes.replace(" ", "").replace(";", ",")[1:-1])
      units.set(units_)
   except:
      return

def select_preset():
   try:
      preset = presets[default.get()]
      load_settings(preset.options[0],
                    preset.options[2],
                    preset.options[3],
                    preset.options[4],
                    preset.options[5],
                    preset.options[6],
                    preset.options[7])
   except:
      return

def load_file(seek=False):
   global presets, aircraft
   presets = {}
   
   with open("payload_presets.txt", "r") as p_:
      if seek:
         p_.flush()
      
      p = p_.read()

      for line in p.split("\n"):
         if line == "" or line == [" " for x in xrange(len(line))]:
            continue
         
         try:
            sections = line.split(":")
            presets[sections[0].ljust(15)[:15]] = Preset([option if i != 7 else int(option) for i, option in enumerate(sections[1].split(","))])
            aircraft = apply(OptionMenu, (master, default) + tuple(presets.keys()))
            aircraft.place(x=390, y=220)
         except:
            continue

def save_preset():
   window.delete("save_error")
   window.delete("err_text")
   name = fields[7].get()

   if name == None or name == "" or name == "".join(" " for x in xrange(len(name))):
      draw_text("Empty name", 400, 176, "red", tag="save_error")
      return

   if name.ljust(15)[:15] in presets.keys():
      delete_preset(from_name=name)

   options = [fields[i].get() if i not in [1, 2, 4] else "" for i in xrange(7)]
   options.append(units.get())

   if None in [o for i, o in enumerate(options) if i < 6]:
      draw_text("Error: Empty fields", 4, 200, "red", tag="err_text")
      return
   elif "False" in [o for i, o in enumerate(options) if i < 6]:
      print options
      draw_text("Error: Fields must be numbers", 4, 200, "red", tag="err_text")
      return
   elif options[6] in [None, False]:
      draw_text("Error: Classes must be comma separated numbers", 4, 200, "red", tag="err_text")
      return
   elif len(options[6]) not in [1, 2, 3]:
      draw_text("Error: Must be 1-3 classes", 4, 200, "red", tag="err_text")
      return
   elif 0 > options[3]:
      draw_text("Error: Max. cargo can't be less than min.", 4, 200, "red", tag="err_text")
      return
   elif 0 > options[5]:
      draw_text("Error: Max. passengers can't be less than min.", 4, 200, "red", tag="err_text")
      return
   elif options[0] < options[3]:
      draw_text("Error: Weight exceeds MTOW", 4, 200, "red", tag="err_text")
      return
   elif True in [options[i] < 0 for i in xrange(len(options))]:
      draw_text("Error: Fields must be greater than 0", 4, 200, "red", tag="err_text")
      return

   options[6] = str(options[6][:3]).replace(",", ";")[1:-1]
   
   with open("payload_presets.txt", "a") as p:
      p.write("\n" + name + ":" + str(options)[1:-1].replace(" ", "") )
   
   load_file()

   if len(presets) == 0:
      presets["Select Aircraft"] = None
   
   aircraft = apply(OptionMenu, (master, default) + tuple(presets.keys()))
   aircraft.place(x=390, y=220)

   default.set(name.ljust(15)[:15])

def delete_preset(from_name=False):
   global aircraft

   if from_name != False:
      name = from_name
   else:
      name = default.get()
   
   try:
      lines = []
      
      with open("payload_presets.txt", "r+") as p_:
         p = p_.read()
         lines = [l for l in p.split("\n") if l != "" or "".join([" " for x in xrange(len(l))])]

         for i, l in enumerate(lines):
            
            if l.split(":")[0].ljust(15)[:15] == name.ljust(15)[:15]:
               del lines[i]

      with open("payload_presets.txt", "w") as p:
         p.seek(0, 2)
         p.write("\n".join(lines))
   except:
      return

   load_file(seek=True)

   if len(presets) < 1:
      presets["Select Aircraft"] = None

   default.set(presets.keys()[0])
   aircraft = apply(OptionMenu, (master, default) + tuple(presets.keys()))
   aircraft.place(x=390, y=220)

with open("payload_presets.txt", "a") as p:
   pass

icon = """
R0lGODlhEgARAHAAACH5BAEAAPwALAAAAAASABEAhwAAAAAAMwAAZgAAmQAAzAAA/wArAAArMwAr
ZgArmQArzAAr/wBVAABVMwBVZgBVmQBVzABV/wCAAACAMwCAZgCAmQCAzACA/wCqAACqMwCqZgCq
mQCqzACq/wDVAADVMwDVZgDVmQDVzADV/wD/AAD/MwD/ZgD/mQD/zAD//zMAADMAMzMAZjMAmTMA
zDMA/zMrADMrMzMrZjMrmTMrzDMr/zNVADNVMzNVZjNVmTNVzDNV/zOAADOAMzOAZjOAmTOAzDOA
/zOqADOqMzOqZjOqmTOqzDOq/zPVADPVMzPVZjPVmTPVzDPV/zP/ADP/MzP/ZjP/mTP/zDP//2YA
AGYAM2YAZmYAmWYAzGYA/2YrAGYrM2YrZmYrmWYrzGYr/2ZVAGZVM2ZVZmZVmWZVzGZV/2aAAGaA
M2aAZmaAmWaAzGaA/2aqAGaqM2aqZmaqmWaqzGaq/2bVAGbVM2bVZmbVmWbVzGbV/2b/AGb/M2b/
Zmb/mWb/zGb//5kAAJkAM5kAZpkAmZkAzJkA/5krAJkrM5krZpkrmZkrzJkr/5lVAJlVM5lVZplV
mZlVzJlV/5mAAJmAM5mAZpmAmZmAzJmA/5mqAJmqM5mqZpmqmZmqzJmq/5nVAJnVM5nVZpnVmZnV
zJnV/5n/AJn/M5n/Zpn/mZn/zJn//8wAAMwAM8wAZswAmcwAzMwA/8wrAMwrM8wrZswrmcwrzMwr
/8xVAMxVM8xVZsxVmcxVzMxV/8yAAMyAM8yAZsyAmcyAzMyA/8yqAMyqM8yqZsyqmcyqzMyq/8zV
AMzVM8zVZszVmczVzMzV/8z/AMz/M8z/Zsz/mcz/zMz///8AAP8AM/8AZv8Amf8AzP8A//8rAP8r
M/8rZv8rmf8rzP8r//9VAP9VM/9VZv9Vmf9VzP9V//+AAP+AM/+AZv+Amf+AzP+A//+qAP+qM/+q
Zv+qmf+qzP+q///VAP/VM//VZv/Vmf/VzP/V////AP//M///Zv//mf//zP///wAAAAAAAAAAAAAA
AAhCAPcJHEiwoMGDCBMqXMiwoT4AECEKjBixIICBF/dl3PfQIsaJCjdm3HiQ4siJEgmSBPlRZcGO
LWNiNNmwps2bOAMCADs=
"""

master = Tk()
master.title("Payload Generator")
icon = PhotoImage(data=icon)
master.tk.call('wm', 'iconphoto', master._w, icon)

default = StringVar(master)
default.set("Select Aircraft")

presets = {"Select Aircraft": None}
load_file()

window = Canvas(master, width=550, height=250)
window.pack()

fields = [
   TextField("MTOW", 0, 60),
   TextField("Fuel", 0, 80),
   TextField("Min. Cargo", 0, 100),
   TextField("Max. Cargo", 0, 120),
   TextField("Min. Passengers", 0, 140),
   TextField("Max. Passengers", 0, 160),
   TextField("Classes", 0, 180, is_int=False, is_list=True),
   TextField("", 294, 196, width=15, is_int=False)
   ]

buttons = [
   ButtonEasy(40, 220, "Generate", generate_tk),
   ButtonEasy(510, 222, "Load", select_preset),
   ButtonEasy(510, 192, "Save", save_preset),
   ButtonEasy(345, 223, "Delete", delete_preset)
   ]

draw_text("Units", 4, 4, "black", tag="help")
draw_text("Adults only", 4, 24, "black", tag="adult")

if len(presets) == 0:
   presets["Select Aircraft"] = None

aircraft = apply(OptionMenu, (master, default) + tuple(presets.keys()))
aircraft.place(x=390, y=220)

units = IntVar()
units.set(0)

Radiobutton(master, text="kg", variable=units, value=0).place(x=90, y=0)
Radiobutton(master, text="lbs", variable=units, value=1).place(x=125, y=0)

adult_box = IntVar()
adult_button = Checkbutton(master, text="", variable=adult_box)
adult_button.place(x=90, y=20)

master.mainloop()
