# Matplotlib4iPerf

Matplotlib4iPerf is an interpreter which receive a file generated from iPerf and using python library (Matplotlib) to make graphical presentation.  

## iPerf

Run iPerf server  
$ iperf -s -D  

run iPerf client  
$ iperf -c $serverip --logfile Matpliotlib4iPerf/input/filename -t 200  

## Usage 

Put all iPerf generated files into input directory.  
Than run iPerfGraph.py.  

To remove all the file in the output and the input directories - simply run inputRecycle.py and outputRecycle.py.  

## Result

2 graphs:  
- 1 for Bytes transferred
- 1 for bandwidth

## Iptables

It can also be used to convert iptables' logs to graph.  
Example file: iptables.log