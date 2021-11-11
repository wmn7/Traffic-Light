'''
@Author: WANG Maonan
@Date: 2021-11-10 16:44:16
@Description: 修改车辆, 包括位置, 路径, 速度, 长度等
@LastEditTime: 2021-11-11 14:17:01
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


while traci.simulation.getMinExpectedNumber() > 0:
    for vehID in conn.simulation.getDepartedIDList():
        _edges = conn.vehicle.getRoute(vehID) # 现在所在的 edge
        if '3fi' in _edges:
            new_routes = [_edges[0], _edges[1], '2o', '2fi', '2si', '1o']
        else:
            new_routes = [_edges[0], '2o', '2fi', '2si', '1o']
        conn.vehicle.setRoute(vehID, new_routes)

    conn.simulationStep() # 仿真到某一步

conn.close()