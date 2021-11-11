'''
@Author: WANG Maonan
@Date: 2021-11-10 16:44:16
@Description: 向路网中增加车辆
@LastEditTime: 2021-11-11 14:56:43
'''
import os
import sumolib

def getAbsPath(file_relpath):
    """将相对路径转换为绝对路径
    """
    file_abspath = os.path.abspath(__file__) # 获得当前文件的绝对路径
    folder_abspath = os.path.dirname(file_abspath) # 获得所在文件夹
    return os.path.join(folder_abspath, file_relpath)

is_libsumo = False

if is_libsumo:
    import libsumo as traci
else:
    import traci

sumoBinary = sumolib.checkBinary('sumo-gui')

if is_libsumo:
    traci.start([sumoBinary, "-c", getAbsPath("./SUMO_Detector_ENV/env/hello.sumocfg")])
    conn = traci
else:
    traci.start([sumoBinary, "-c", getAbsPath("./SUMO_Detector_ENV/env/hello.sumocfg")], label='0')
    conn = traci.getConnection('0')

# #############
# 指定起点和终点
# #############
conn.route.add('new_trip', ['2fi', '2o']) # [startEdge, endEdge]
for i in range(10):
    conn.vehicle.add('new_{}'.format(i), 'new_trip', depart=10*i, departLane='free') # depart 是时间

# #############
# 指定详细的路径
# #############
conn.route.add('new_trip_2', ['4fi', '4si', '1o', '1fi']) # 详细的路径
for i in range(10, 20):
    conn.vehicle.add('new_{}'.format(i), 'new_trip_2', depart=10*i, departLane='free') # depart 是时间


while traci.simulation.getMinExpectedNumber() > 0:
    for vehID in conn.simulation.getDepartedIDList():
        routes = conn.vehicle.getRoute(vehID)
        if '3si' in routes:
            conn.vehicle.remove(vehID) # 删除经过 3si 的车辆
    conn.simulationStep() # 仿真到某一步

conn.close()