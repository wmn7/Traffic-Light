###
 # @Author: WANG Maonan
 # @Date: 2021-11-12 14:30:42
 # @Description: 测试直接使用 SUMO 的速度
 # @LastEditTime: 2021-11-15 22:11:51
### 
sum=0 # 总的运算时长

for i in {1..20};do

    START_TIME=`date +%s` # 开始时间

    sumo -c ./SUMO_Detector_ENV/env/hello.sumocfg -r ./SUMO_Detector_ENV/routes/1000.rou.xml --time-to-teleport 1000 --no-warnings --no-step-log

    END_TIME=`date +%s` # 结束时间

    EXECUTING_TIME=`expr $END_TIME - $START_TIME` # 运行时间
    let "sum+=EXECUTING_TIME" # 进行数值运算
    echo 'Time,' $EXECUTING_TIME
done

echo 'Total Time,' $sum