'''
@Author: WANG Maonan
@Date: 2021-09-26 15:53:41
@Description: 利用 traci 获取和控制信号灯
@LastEditTime: 2021-09-26 16:25:10
'''
import traci
from sim import Sim

sumo_sim = Sim(sumo_config='./env/hello.sumocfg')
sumo_sim.launchEnv() # 开启仿真


# 获取信号灯信息
logic_list = traci.trafficlight.getCompleteRedYellowGreenDefinition('0')[0] # 只有一个 program
print(logic_list)
# 修改信号灯信息, 将绿灯时长都加 10 秒
for phase in logic_list.phases:
    if 'G' in phase.state:
        phase.duration += 10
traci.trafficlight.setCompleteRedYellowGreenDefinition(tlsID='0', tls=logic_list)
# 重新打印修改后的红绿灯信息
logic_list = traci.trafficlight.getCompleteRedYellowGreenDefinition('0')[0]
print(logic_list)


sumo_sim.close()