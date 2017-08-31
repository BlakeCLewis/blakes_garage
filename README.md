# blakes_garage

A Radiant floor heating project for my garage.
## Parts
  * Raspberry pi Zero W
  * 6 - DS18b20 one-wire temperature sensor water proof - Amazon
  * 2 - ACS758LCB 50A Range Linear Current Sensor module - Amazon
  * 2 - 3V 1 channel relay module - Amazon 
  * 1 - Adafruit Pro Bonnet pcb
  * 1 - mcp3008 8 ch, 10bit ADC w/ SPI interface  - Adafruit 856
  * 1 - 2x8 DIP IC chip socket 
  * 4 - 3x4 right angle male header - Adafruit 816 
  * 1 - OLED display 128x64 - Adafruit 3527

## Temp sensors
  * outside air   (oa)
  * inside air    (ia)
  * hot water     (hw)
  * return 1      (r1)
  * return 2      (r2)
  * mix valve     (mx)

## Current sensors
  * Aquastat 1 (A1)
  * Aquastat 2 (A2)
  
## relay
  * water pump

## 2 stage project 
  * data aquasition and fail safe
     failure mode: gas water water heater standing pilot goes out, system still tries to heat floor. This stage will log 6 temperatures and system state changes.
  * system control
     This stage will remove the auastats and replace them with relays

### water pipe schematic
```
hw________________mx__pump___loop1__aquastat1__valve1_
|                  |       |_loop2__aquastat2__valve2_| 
|_<<oneway-valve<<_|__________________________________|
```

### electric control schematics
 * existing
```
120Vac_________________________________________________
             |                                         |
pi__3Vdc-relay___48V-trans___aquastat1__valve1___P-relay__pump
                           |_aquastat2__valve2___|
```
 * remove aquastats
```
120Vac_________________________________
       |                               |
       |_48V-trans__                   |
                    |                  |
          pi__3v-relay__valve1___P-relay__pump
            |_3v-relay__valve2___|
```

   Valve(1,2) use a material that expands when heated with an electric element, which pushes a valve open. When the valve opens (it is not fast) it make a connection energizing the pump. The Aquastats have a 5&deg;C temp range(min/max). It energizes the valve at min, and closes the valve at max. The dials on the Aqustat do not have numbers and are course adjustments.
    I am going to replace the aqustats with temp sensor and relays, Relays will open the valves and valves will energize the pump. Valves and pump replay are 48VAC, pump is 120VAC, 
