'''
该文件计算出各个关系的连通子图的个数，每个连通子图的节点个数和边个数
并导出具有较多边的json格式
换了非递归的dfs Python也不会内存报错了
计算也非常快
'''

import csv
import json
import sys
sys.setrecursionlimit(100000)                  # 提示超过了最大递归深度
# 即使这样还是会报错，在pycharm中修改了 Xms 和 Xmx

visit = {}      # visit 字典标识节点是否被访问过 45：0； 0没有被访问， 1被访问 45是id
adjacencyList = {}  # 邻接链表用来存储每个节点的邻居 每个元素标识为：55：（23， 15， 77）

connectedComponents = []            # 记录连通子图，每个元素代表一个连通子图


'''
栈函数
'''
class Stack(object):

    def __init__(self):
        self.stack = []

    def push(self, data):
        """
        进栈函数
        """
        self.stack.append(data)

    def pop(self):
        """
        出栈函数，
        """
        return self.stack.pop()

    def gettop(self):
        """
        取栈顶
        """
        return self.stack[-1]

    def isempty(self):
        """
        是否为空
        :return:
        """
        if len(self.stack) == 0:
            return True
        return False

stk = Stack()


def init():
    # 读文件初始化visit和adjacencyList
    with open("./data/mentor_protege_relation_univ_time_NeuroMath.csv", "r") as f:
        f_csv = csv.reader(f)
        next(f)

        for line in f_csv:
            type = int(line[6])
            if type == 2:
                startId = int(line[0])
                endId = int(line[2])

                # 键值是唯一的 不必判断是否在字典中
                visit[startId] = 0
                visit[endId] = 0

                if startId not in adjacencyList:
                    adjacencyList[startId] = set()
                adjacencyList[startId].add(endId)  # set添加元素
                if endId not in adjacencyList:
                    adjacencyList[endId] = set()
                adjacencyList[endId].add(startId)  # set添加元素

        print("初始化完毕")
        print(len(visit))
        print(len(adjacencyList))

def stackDFS(node):
    # 根节点入栈
    stk.push(node)

    # 当栈不为空，元素出栈，出栈元素标记为已访问，出栈元素加入nodes         这里记住python中 not的用法
    while not stk.isempty():
        curNode = stk.gettop()
        stk.pop()

        if visit[curNode] == 0:
            connectedComponents[-1]["nodes"].append({"id": curNode})
            visit[curNode] = 1
            for neighbor in adjacencyList[curNode]:
                if curNode < neighbor:
                    connectedComponents[-1]["edges"].append({"source": curNode, "target": neighbor, "type": 1})
                stk.push(neighbor)

def findComponents():
    # 找出所有的连通域 for key in a和 for key in a.keys():完全等价。
    componentNum = 0

    for key in visit:
        if visit[key] == 0:
            # 代表一个新的联通子图
            componentNum += 1
            # 增加一个新的连通子图
            connectedComponents.append({"nodes": [], "edges": []})
            stackDFS(key)

    print("联通子图的个数为", componentNum)



if __name__ == "__main__":
    init()
    findComponents()

    print("对连通子图按照节点的数量进行排序")
    connectedComponents.sort(key=lambda d:len(d["nodes"]), reverse=True)

    # 输出节点数量前10的联通子图
    for i in range(10):
        print("排名", i)
        print("节点数", len(connectedComponents[i]["nodes"]))
        print("连接边数", len(connectedComponents[i]["edges"]))
        with open("./top10Components/top-2-" + str(i) + ".json", "w") as f:
            json.dump(connectedComponents[i], f, indent=2)