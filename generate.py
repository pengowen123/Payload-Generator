from Tkinter import *
from random import randint, uniform

class Class(object):
   def __init__(self, passengers, cargo):
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

# Passenger weights in kg including baggage
weights = [
    0,
    40,
    100
    ]


def generate(mtow,
             fuel,
             min_cargo,
             max_cargo,
             min_pass,
             max_pass,
             class_count):

   cargo = randint(min_cargo, max_cargo)
   weight = fuel + cargo
    
   # Generate random passengers
   # 0 = infant
   # 1 = child
   # 2 = adult
   passenger_count = randint(min_pass, max_pass)
   passengers = []
    
   for x in xrange(passenger_count):
      p = weighted_choice([(0, 1.0), (1, 4.0), (2, 30.0)])
      weight += weights[p]

      if weight > mtow:
         break
        
      passengers.append(p)
      

   # Sort passengers into classes
   classes = [[] for c in xrange(class_count)]

   for p in passengers:
      if class_count < 2:
         max_per_class = len(passengers) / 2
      else:
         max_per_class = len(passengers) / (class_count - 1)
      
      c_rand = randint(0, class_count)
        
      for c in xrange(class_count):
         if len(classes[c]) < max_per_class and c == c_rand:
            classes[c].append(p)

   classes = [Class(c, cargo / class_count) for c in classes]

   return cargo, len(passengers), classes

cargo, passengers, classes = generate(5000,
                                      1000,
                                      300,
                                      600,
                                      100,
                                      200,
                                      3)

class TextField(object):
   def __init__(self, label, x, y):
      self.label = Label(master, text=label)
      self.field = Entry(master, width=7, exportselection=0)
      self.label.place(x=x, y=y)
      self.field.place(x=x+100, y=y)

   def get(self):
      try:
         string = int(self.field.get())
      except:
         return None
         
      return string

   def insert(self, string):
      self.field.delete(0, END)
      self.field.insert(0, string)

def generate_tk():
   window.delete("text")
   window.delete("line")
   
   mtow = fields[0].get()
   fuel = fields[1].get()
   min_cargo = fields[2].get()
   max_cargo = fields[3].get()
   min_pass = fields[4].get()
   max_pass = fields[5].get()
   classes = fields[6].get()

   if None in [mtow, fuel, min_cargo, max_cargo, min_pass, max_pass, classes]:
      draw_text("Invalid input", 40, 210, "red")
      return

   cargo, passengers, classes = generate(mtow,
                                         fuel,
                                         min_cargo,
                                         max_cargo,
                                         min_pass,
                                         max_pass,
                                         classes
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
   draw_text("Pax:   %s" % c.weight, x, y+20, "blue")
   draw_text("Cargo:   %s" % c.cargo, x, y+40, "blue")
   draw_text("Adults:   %s" % c.adult_count, x, y+60, "blue")
   draw_text("Children: %s" % c.child_count, x, y+80, "blue")
   draw_text("Infants:  %s" % c.infant_count, x, y+100, "blue")

master = Tk()
window = Canvas(master, width=550, height=250)
window.pack()

RED = (255, 0, 0)
BLUE = (0, 0, 150)

fields = [
   TextField("MTOW", 0, 20),
   TextField("Fuel", 0, 40),
   TextField("Min. Cargo", 0, 60),
   TextField("Max. Cargo", 0, 80),
   TextField("Min. Passengers", 0, 100),
   TextField("Max. Passengers", 0, 120),
   TextField("Classes", 0, 140)
   ]

button = Button(master, text="Generate", command=generate_tk)
button.place(x=40, y=180)

default = StringVar(master)
default.set("Select Aircraft")
aircraft = OptionMenu(master, default, "Select Aircraft", "foo", "bar", "baz")
aircraft.place(x=196, y=176)

draw_text("Input and output in kg", 4, 0, "black", tag="help")

master.mainloop()
# Add drop down menu to select defaults for different types of planes
