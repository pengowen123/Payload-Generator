#Payload-Generator

![alt tag](https://raw.github.com/pengowen123/Payload-Generator/master/screenshot.png)

Generates passengers and cargo along with their distributions.

#Usage

Enter maximum takeoff weight into the MTOW field. Enter the weight of the fuel into the Fuel field. Cargo will be generated in a range from the Min. cargo and Max. cargo fields. Passenger count will be generated in a range from the Min. passengers and Max. passengers fields. There may be fewer passengers generated to keep the weight under the MTOW. Enter the max passengers of each class in the Classes field, comma separated. If all classes have reached maximum capacity, no more passengers are generated. After all fields are entered, click the Generate button and the results will appear in blue on the right. To change the input and output units, select one of the buttons at the top. If you want only adults to be generated, tick the checkbox at the top.

To save all the current settings (except for fuel, and minimum cargo and passengers, which are saved as 0), type a name into the field next to the Save button and click the button. To load these settings, select a saved aircraft from the dropdown menu. To delete an aircraft, select it from the dropdown menu and click the Delete button.

#Installation

Go to the [releases](https://github.com/pengowen123/Payload-Generator/releases) and get the latest version. If you have Python 2.7 or later (but not 3), you can simply move the generate.pyw file to somewhere convenient and double click it to run the program. Otherwise, move the Payload-Generator folder in the exe folder to somewhere convenient, and run the generate.exe file inside.

#Bugs

If you encounter a bug, file an issue listing operating system, Python version, Payload-Generator version, and steps to reproduce.
