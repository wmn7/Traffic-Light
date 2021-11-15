'''
@Author: WANG Maonan
@Date: 2021-11-11 21:47:27
@Description: 比较 libsumo 与 traci
@LastEditTime: 2021-11-15 22:14:34
'''
import os
import time
import sumolib

def getAbsPath(file_relpath):
    """将相对路径转换为绝对路径
    """
    file_abspath = os.path.abspath(__file__) # 获得当前文件的绝对路径
    folder_abspath = os.path.dirname(file_abspath) # 获得所在文件夹
    return os.path.join(folder_abspath, file_relpath)

is_libsumo = True
vehicle_num = 10000 # route 的选择

if is_libsumo:
    import libsumo as traci
else:
    import traci

sumoBinary = sumolib.checkBinary('sumo', bindir='/mnt/d/traffic_info/traffic_info_env/bin')

times_list = [] # 记录 20 次运行的时间

for i in range(20):
    start_time = time.time() # 开始时间
    if is_libsumo:
        traci.start([sumoBinary, 
                        "-c", getAbsPath("./SUMO_Detector_ENV/env/hello.sumocfg"), 
                        "-r", getAbsPath("./SUMO_Detector_ENV/routes/{}.rou.xml".format(vehicle_num)),
                        "--time-to-teleport",  "1000",
                        "--no-warnings",
                        "--no-step-log"]
                    )
        conn = traci
    else:
        traci.start([sumoBinary, 
                        "-c", getAbsPath("./SUMO_Detector_ENV/env/hello.sumocfg"), 
                        "-r", getAbsPath("./SUMO_Detector_ENV/routes/{}.rou.xml".format(vehicle_num)),
                        "--time-to-teleport",  "1000",
                        "--no-warnings",
                        "--no-step-log"],
                    label='0'
                    )
        conn = traci.getConnection('0')

    simulation_steps = 0
    while conn.simulation.getMinExpectedNumber() > 0:
        conn.simulationStep()
        simulation_steps += 1 # 计算仿真步数

    executing_time = time.time() - start_time # 程序运行时间
    times_list.append(executing_time)
    print('Time, {}; Simulation Steps, {}'.format(executing_time, simulation_steps))

    if is_libsumo:
        conn.close()
    else:
        traci.close()

import numpy as np
print(np.sum(times_list), np.mean(times_list))
