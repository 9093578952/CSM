# Eda Yan <yidayan@usc.edu> -USC SPORT LAB
# modified by Hao Ge
# considering what Saeed suggested last week, 
# i think the best way to achieve "all in one" style control and auto run, 
# while still keep the locality and modularity of the code
# is to write a very top level wrapper file. that controls and calls all the sub-module

import os
import importlib
import sys

# according to Saeed's envision, it should

# job 0
# check the OOP_circuit_simulator config.py file, see if the LUT
# user asking exist, if not, call characterisaion tool to create it.
sys.path.insert(1,'./simulation')
#import config
config_file = importlib.import_module("config")

VERILOG_FILE = config_file.verilog_netlist_dir
SPICE_FILE = VERILOG_FILE.split("/")[-1]
SPICE_FILE = SPICE_FILE.replace('.v', '.sp')

owd = os.getcwd() # record original working directory
os.chdir("./simulation")
# get all gate types in .v netlist
gate_list = []
gate_type_list = []
f = open(VERILOG_FILE, 'r')
Lines = f.readlines()
f.close()
for line in Lines:
    if "//" in line:
        gate_list.append(line)
gate_list = gate_list[5:]
for line in gate_list:
    items = line.split()
    gate_name = items[1]
    gate_type_list.append(gate_name)
#print(gate_type_list)

# check if the gate LUT exists in LUT_bin
LUT_name_front = config_file.LUT_bin_dir + config_file.TECH
LUT_name_back = "VL" + str(config_file.VL) + "_VH" + str(config_file.VH) + "_VSTEP" + \
                str(config_file.VSTEP) + "_P" + str(config_file.PROCESS_VARIATION) + "_V" \
                + str(config_file.VDD) + "_T" + str(config_file.TEMPERATURE) + ".lut"
miss_gate = []

for gate in gate_type_list:
    lut_dir = LUT_name_front + "_" + gate + "_" + LUT_name_back
    print lut_dir
    if os.path.exists(lut_dir) == False:
        print(gate, ": this gate's LUT doesn't exist, will characterize for it")
        miss_gate.append(gate)
os.chdir(owd)

# do characterisation for missing gate
# this cannot work, characteration module not imported, use command line style. --haoge
if len(miss_gate) > 0:
    for gate in miss_gate:
        os.chdir("../characterisation")
        characterisation.main(gate, config_file.VSTEP, "../modelfiles/PTM_MG/lstp/7nm_LSTP.pm", \
                              fig_file.VDD, config_file.TEMPERATURE)
    os.chdir(owd)


# job 1
# read original verilog netlist and record all final outputs, so that final output loads 
# can be added to them. This job should modify the final_output_load of config file
print("reading verilog netlist, and get the final outputs information")
#os.chdir("../HSPICE_simulation")
sys.path.insert(1,'./HSPICE_simulation')
from translator_from_verilog_to_spice_netlist import *
circuit_output = translator_from_verilog_to_spice_netlist(\
    "./simulation/"+VERILOG_FILE, "./HSPICE_simulation/" + SPICE_FILE)


# job 2 
# call OOP_circuit_simulator in simulation folder
os.chdir("./simulation")
os.system("python OOP_circuit_simulator.py config.py")
os.chdir(owd)

# job 3
# translate CSM_config file to spice .sp file
# call hspice and run equivalent.
os.sys("cp ./simulation/config.py ./HSPICE_simulation/config.py")
os.chdir("./HSPICE_simulation")
os.system("python hspice_simulator.py")
os.chdir(owd)

# job 4
# call Auto_Plotter to plot csm simulation result
# todo: how to plot hspice output?
#os.chdir("../CSM-master/Auto_Plotter")
#os.system("python plot.py")
