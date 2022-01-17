def initialize(grids=5,lanes=3,length=200):
    os.system("netgenerate --grid --grid.number=5 -L="+str(lanes)+" --grid.length="+str(length)+" --output-file=grid.net.xml")

def single(path,vehicles):
    os.system(path + "randomTrips.py -n grid.net.xml -o flows.xml --begin 0 --end 1 --period 1 --flows "+str(vehicles))
    os.system("jtrrouter --flow-files=flows.xml --net-file=grid.net.xml --output-file=grid.rou.xml --begin 0 --end 10000 --accept-all-destinations")
    os.system(path + "generateContinuousRerouters.py -n grid.net.xml --end 10000 -o rerouter.add.xml")
    tree = ET.parse("grid.sumocfg")
    root = tree.getroot()
    for child in root:
        if (child.tag == 'output'):
            for child2 in child:
                child2.attrib['value'] = 'grid.output'+str(vehicles)+'.xml'
    with open('grid.sumocfg', 'wb') as f:
        tree.write(f)
    os.system("sumo -c grid.sumocfg --device.fcd.period 100")

    if __name__ == '__main__':
        print("Done")
        import os
        import numpy as np
        import analysis
        from matplotlib import pyplot as plt

        import xml.etree.ElementTree as ET
        path = "C:\Hackers Realm\iit bombay techfest\sumo1\sumo"
        initialize()
        vehicles_arr=np.r_[np.linspace(10,100,10).astype(int),np.linspace(100,2000,20).astype(int)]
        for i in range(0,len(vehicles_arr)):
            single(path,vehicles_arr[i])