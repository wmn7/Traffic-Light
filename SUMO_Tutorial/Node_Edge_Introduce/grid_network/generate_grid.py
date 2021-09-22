'''
@Author: WANG Maonan
@Date: 2021-09-22 20:35:06
@Description: 生成网格状路网
@LastEditTime: 2021-09-22 20:39:41
'''

# 生成Node文件, 从左下角(0,0)开始生成的
with open('cross.nod.xml', 'w') as file:
    file.write('<nodes> \n')
    for i in range(6):
        for j in range(6):
            file.write('<node id="node%d" x="%d" y="%d" type="priority" /> \n' %(i*6+j, i*100, j*100))
    file.write('</nodes> \n')


# 生成edge文件
with open('cross.edg.xml', 'w') as file:
    file.write('<edges> \n')
    for i in range(6):
        for j in range(6):
            k=0
            if i > 0:
                file.write('<edge id="edge%d_%d" from="node%d" to="node%d" priority="75" numLanes="2" speed="40" /> \n' % (i*6+j,k,i*6+j,(i-1)*6+j))
                k=k+1
            if i < 5:
                file.write('<edge id="edge%d_%d" from="node%d" to="node%d" priority="75" numLanes="2" speed="40" /> \n' % (i*6+j,k,i*6+j,(i+1)*6+j))
                k=k+1
            if j > 0:
                file.write('<edge id="edge%d_%d" from="node%d" to="node%d" priority="75" numLanes="2" speed="40" /> \n' % (i*6+j,k,i*6+j,i*6+j-1))
                k=k+1
            if j < 5:
                file.write('<edge id="edge%d_%d" from="node%d" to="node%d" priority="75" numLanes="2" speed="40" /> \n' % (i*6+j,k,i*6+j,i*6+j+1))
                k=k+1
    file.write('</edges> \n')