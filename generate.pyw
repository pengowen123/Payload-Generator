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
             class_count,
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
   classes = [[] for c in xrange(class_count)]

   for p in passengers:
      if class_count < 2:
         max_per_class = len(passengers)
      else:
         max_per_class = len(passengers) / (class_count - 1)

      class_weights = [1.0, 5.0, 6.0]
      c_rand = weighted_choice([(c, class_weights[c]) for c in xrange(class_count)])
        
      for c in xrange(class_count):
         if c == 0 and len(classes[c]) > 20:
            if class_count >= 3:
               c = 2
            elif class_count >= 2:
               c = 1
            
         if len(classes[c]) < max_per_class and c == c_rand:
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
   def __init__(self, label, x, y, width=7, is_int=True):
      self.label = Label(master, text=label)
      self.field = Entry(master, width=width, exportselection=0)
      self.label.place(x=x, y=y)
      self.field.place(x=x+100, y=y)
      self.is_int = is_int

   def get(self):
      try:
         string = self.field.get()
         if self.is_int:
            return int(string)
      except:
         return None
         
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
   window.delete("line")
   
   mtow = fields[0].get()
   fuel = fields[1].get()
   min_cargo = fields[2].get()
   max_cargo = fields[3].get()
   min_pass = fields[4].get()
   max_pass = fields[5].get()
   classes = fields[6].get()
   adults_only = adult_box.get()

   if None in [mtow, fuel, min_cargo, max_cargo, min_pass, max_pass, classes] or classes not in [1, 2, 3] or min_cargo > max_cargo or min_pass > max_pass or mtow < fuel + max_cargo:
      draw_text("Invalid options", 31, 200, "red")
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
      fields[6].insert(classes.replace(" ", ""))
      units.set(units_)
   except:
      return

def select_preset():
   try:
      preset = presets.get(default.get())
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
            return

def save_preset():
   window.delete("save_error")
   name = fields[7].get()

   if name.ljust(15)[:15] in presets.keys():
      return

   if name == None or name == "" or name == "".join(" " for x in xrange(len(name))):
      draw_text("Invalid name", 400, 176, "red", tag="save_error")
      return

   options = [fields[i].get() if i not in [1, 2, 4] else "" for i in xrange(7)]
   options.append(units.get())

   if None in options or options[6] not in [1, 2, 3] or 0 > options[3] or 0 > options[5] or options[0] < options[3]:
      window.delete("save_error")
      draw_text("Invalid options", 400, 176, "red", tag="save_error")
      return

   with open("payload_presets.txt", "a") as p:
      p.write("\n" + name + ":" + str(options)[1:-1].replace(" ", "") )
   
   load_file()

   if len(presets) == 0:
      presets["Select Aircraft"] = None
   
   aircraft = apply(OptionMenu, (master, default) + tuple(presets.keys()))
   aircraft.place(x=390, y=220)

def delete_preset():
   global aircraft
   
   try:
      lines = []
      
      with open("payload_presets.txt", "r+") as p_:
         p = p_.read()
         lines = [l for l in p.split("\n") if l != "" or "".join([" " for x in xrange(len(l))])]

         for i, l in enumerate(lines):
            
            if l.split(":")[0].ljust(15)[:15] == default.get().ljust(15)[:15]:
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

master = Tk()
master.title("Payload Generator")

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
   TextField("Classes", 0, 180),
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
