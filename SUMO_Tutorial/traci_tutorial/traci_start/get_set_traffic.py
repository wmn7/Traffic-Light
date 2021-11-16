'''
@Author: WANG Maonan
@Date: 2021-11-16 16:38:37
@Description: 利用 traci 得到信号灯, 或是修改信号灯数据
@LastEditTime: 2021-11-16 21:15:31
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


def get_trafficLight_info(tls_id='0', program_id=0):
    """得到信号灯的数据
    """
    remaining_duration = conn.trafficlight.getNextSwitch(tls_id) - conn.simulation.getTime() # 距离下一个相位的时间
    print('Remain Duration, {}'.format(remaining_duration))
    logic = conn.trafficlight.getCompleteRedYellowGreenDefinition(tls_id)[program_id] # 得到信号灯
    for phase in logic.phases:
        print(phase.state, phase.duration)
        # print(phase.minDur)
        # print(phase.maxDur)


def set_trafficLight_info(tls_id='0', program_id=0):
    """设置信号灯的数据
    """
    logic = conn.trafficlight.getCompleteRedYellowGreenDefinition(tls_id)[program_id] # 得到信号灯
    for phase in logic.phases: # 修改信号灯的值
        phase.duration = 3
        phase.minDur = 3
        phase.maxDur = 3
    conn.trafficlight.setCompleteRedYellowGreenDefinition(tls_id, logic) # 设置信号灯


while conn.simulation.getMinExpectedNumber() > 0:
    get_trafficLight_info() # 获得信号灯信息
    set_trafficLight_info() # 设置信号灯
    conn.simulationStep()


conn.close()