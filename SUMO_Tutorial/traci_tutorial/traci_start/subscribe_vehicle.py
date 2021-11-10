'''
@Author: WANG Maonan
@Date: 2021-11-10 11:04:08
@Description: 测试 traci 的一些功能
@LastEditTime: 2021-11-10 16:16:57
'''
import os
import sumolib
from traci import domain

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


# 订阅 junction, 获取 junction 周围的信息
conn.junction.subscribeContext('0', 
                            domain=traci.constants.CMD_GET_VEHICLE_VARIABLE, 
                            dist=100, 
                            varIDs=[traci.constants.VAR_SPEED, traci.constants.VAR_WAITING_TIME])

while traci.simulation.getMinExpectedNumber() > 0:
    # 订阅每一辆车
    for veh_id in conn.simulation.getDepartedIDList(): # 新进入路网的车
        conn.vehicle.subscribe(veh_id, [traci.constants.VAR_POSITION, traci.constants.VAR_SPEED])
    positions_speeds = conn.vehicle.getAllSubscriptionResults()

    # 订阅 junction, 获取 junction 周围的信息
    junction_vehicles = conn.junction.getAllContextSubscriptionResults()
    # conn.junction.getContextSubscriptionResults('0') # 可以指定 junction id

    conn.simulationStep() # 仿真到某一步

conn.close()

