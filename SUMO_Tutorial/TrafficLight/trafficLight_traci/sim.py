'''
@Author: WANG Maonan
@Date: 2021-09-26 15:07:44
@Description: 使用 TraCI 开启并运行仿真
@LastEditTime: 2021-09-26 15:56:54
'''
import sys
import traci

class Sim(object):
    def __init__(self, sumo_config, GUI=False):
        self.sumo_config = sumo_config # sumo config 文件
        self.launch_env_flag = False
        self.GUI = GUI
        
    def launchEnv(self):
        """开始模拟(通过traci来获得其中数据)
        """
        if self.GUI:
            sumo_gui = 'sumo-gui'
        else:
            sumo_gui = 'sumo'

        traci.start([
            sumo_gui,
            "-c", self.sumo_config,
            "--no-warnings",
            "--seed", "2"])        
        self.launch_env_flag = True

    def close(self):
        """关闭实验环境
        """
        traci.close()
        self.launch_env_flag = False
        sys.stdout.flush()

    def reset(self):
        """关闭当前环境, 并开启一个新的环境
        """
        self.close()
        self.launchEnv()

    def step(self):
        """一直进行仿真，直到结束
        """
        steps = 0
        assert self.launch_env_flag
        while traci.simulation.getMinExpectedNumber() > 0: # 当路网里面还有车
            traci.simulationStep()
            steps = steps + 1

    def runSim(self):
        """开始模拟
        """
        self.launchEnv()  # 初始化环境
        self.step()  # 进行模拟
        self.close()  # 关闭环境

if __name__ == '__main__':
    sumo_sim = Sim(sumo_config='./env/hello.sumocfg')
    sumo_sim.runSim() # 运行仿真