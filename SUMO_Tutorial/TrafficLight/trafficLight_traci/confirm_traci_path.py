'''
@Author: WANG Maonan
@Date: 2021-09-26 14:58:04
@Description: 确认 traci 是否在系统环境变量中
@LastEditTime: 2021-09-26 14:58:05
'''
import os
import sys

# 确保 traci 在系统环境变量中
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
    print('SUMO_HOME is In Environment!')
else:
    sys.exit("please declare environment variable 'SUMO_HOME'")