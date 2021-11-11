'''
@Author: WANG Maonan
@Date: 2021-11-11 15:21:45
@Description: 订阅探测器
@LastEditTime: 2021-11-11 20:07:06
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

if is_libsumo:
    sumoBinary = sumolib.checkBinary('sumo', bindir='/mnt/d/traffic_info/traffic_info_env/bin')
    traci.start([sumoBinary, "-c", getAbsPath("./SUMO_Detector_ENV/env/hello.sumocfg")])
    conn = traci
else:
    sumoBinary = sumolib.checkBinary('sumo-gui', bindir='/mnt/d/traffic_info/traffic_info_env/bin')
    traci.start([sumoBinary, "-c", getAbsPath("./SUMO_Detector_ENV/env/hello.sumocfg")], label='0')
    conn = traci.getConnection('0')


# 订阅 E1 探测器, last simulation step 车辆数量
for e1_id in conn.inductionloop.getIDList():
    conn.inductionloop.subscribe(e1_id, [traci.constants.LAST_STEP_VEHICLE_NUMBER])

# 订阅 E2 探测器, 车速, 占有率, 排队长度(车辆数和长度)
for e2_id in conn.lanearea.getIDList():
    conn.lanearea.subscribe(e2_id, [traci.constants.LAST_STEP_MEAN_SPEED, # 17
                                    traci.constants.LAST_STEP_OCCUPANCY, # 19
                                    traci.constants.JAM_LENGTH_VEHICLE, # 24 
                                    traci.constants.JAM_LENGTH_METERS]) # 25

# 订阅 E3 探测器, 延误时间, 平均通行时间, 平均停车次数, 通过的车辆 (通过 e3 区域)
for e3_id in conn.multientryexit.getIDList():
    conn.multientryexit.subscribe(e3_id, [traci.constants.VAR_TIMELOSS, # 140
                                          traci.constants.VAR_LAST_INTERVAL_TRAVELTIME, # 88
                                          traci.constants.VAR_LAST_INTERVAL_MEAN_HALTING_NUMBER, # 32
                                          traci.constants.VAR_LAST_INTERVAL_VEHICLE_NUMBER]) # 33

while traci.simulation.getMinExpectedNumber() > 0:
    e1_results = conn.inductionloop.getAllSubscriptionResults()
    e2_results = conn.lanearea.getAllSubscriptionResults()
    e3_results = conn.multientryexit.getAllSubscriptionResults() # E3 必须要经过两个探测器

    conn.simulationStep()

conn.close()