#!/usr/bin/python

import os
import json

tmp_filename_rackpos_diag='/tmp/json-to-rack-pos-diag'
tmp_filename='/tmp/json-to-rackdiag'
json_filepath='/var/tmp/json-to-rackdiag/json-to-rackdiag.json'

#####

def create_str_each_u_from_each_u(rack):
 str_each_u=''
 for each_u in rack['each_u']:
  tmp_each_u=each_u.copy()
  if (not 'serial' in tmp_each_u):
   tmp_each_u['serial']=None
  elif (not 'hostname' in tmp_each_u):
   tmp_each_u['hostname']=None
  str_each_u += '{position}:{hostname}\\n{serial}\n'.format(**tmp_each_u)
 return str_each_u
 

def main():
 
 ##
 # read json
 ##
 with open(json_filepath) as f:
  js=json.load(f)

 ##
 # create rack-pos-diagram
 ##
 racks=[]
 (max_rack_x, max_rack_y)=(0, 0)
 for rack in js['racks']:
  if (rack['rack_x'] > max_rack_x):
   max_rack_x = rack['rack_x']
  if (rack['rack_y'] > max_rack_y):
   max_rack_y = rack['rack_y']
 #print (max_rack_x, max_rack_y)

 for i in range(max_rack_y):
  racks.append([str() for i in range(max_rack_x)])

 #print (racks)

 for rack in js['racks']:
  rack_x=rack['rack_x']-1
  rack_y=rack['rack_y']-1
 # print (rack_x, rack_y)
  racks[rack_y][rack_x]=rack['rackname']

 #print (racks)
 str_for_racks=''
 for y in range(len(racks)):
  line_of_rack=racks[y]
  str_for_racks+='{'
  for x in range(len(line_of_rack)):
   #print (str_for_racks)
   #print (y, x, racks[y][x])
   str_for_racks += racks[y][x]
   str_for_racks+='|'
  str_for_racks=str_for_racks[:-1]
  str_for_racks+='}|'
 str_for_racks=str_for_racks[:-1]

 str_for_rack_position_diagram="""
digraph structs {{
    node [shape=record]; 
    room [ 
     label="{0}" 
    ];     
}}
""".format(str_for_racks)
 # print (str_for_rack_position_diagram)

 with open(tmp_filename_rackpos_diag, 'w') as f:
  f.write(str_for_rack_position_diagram)
 os.system('dot -Tsvg -o {0}.svg {0}'.format(tmp_filename_rackpos_diag))


 ##
 # create rack-diagram
 ##
 str_each_rack=''
 for rack in js['racks']:
  # rackname, str_each_u
  str_each_u=create_str_each_u_from_each_u(rack)
  str_each_rack += """
 rack {{
 12U;
 description={0};
 {1}
 }}
 """.format(rack['rackname'], str_each_u)
 
 #print (str_each_rack)
 
 rackdiag="""
 rackdiag {{
 ascending;
 {0}
 }}
 """.format(str_each_rack)
 
 #print (rackdiag)
 
 with open(tmp_filename, 'w') as f:
  f.write(rackdiag)
 os.system('rackdiag -Tsvg {0}'.format(tmp_filename))
 

if __name__ == '__main__':
 main()
