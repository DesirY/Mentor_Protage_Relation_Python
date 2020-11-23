'''
该文件计算出各个关系的连通子图的个数，每个连通子图的节点个数和边个数
并导出具有较多边的json格式
'''

import csv
import json
import sys
sys.setrecursionlimit(100000)                  # 提示超过了最大递归深度
# 即使这样还是会报错，在pycharm中修改了 Xms 和 Xmx

visit = {}      # visit 字典标识节点是否被访问过 45：0； 0没有被访问， 1被访问 45是id
adjacencyList = {}  # 邻接链表用来存储每个节点的邻居 每个元素标识为：55：（23， 15， 77）
iterate = 0               # 用来标记当前的递归深度

bridge = []             # 两个集合的桥梁

connectedComponents = []            # 记录连通子图，每个元素代表一个连通子图

def init():
    # 读文件初始化visit和adjacencyList
    with open("./data/mentor_protege_relation_univ_time_NeuroMath.csv", "r") as f:
        f_csv = csv.reader(f)
        next(f)

        for line in f_csv:
            type = int(line[6])
            if type == 1:
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

def DFS(node):
    if iterate == 100:
        return
    iterate += 1
    visit[node] = 1    # 更正
    connectedComponents[-1]["nodes"].append({"id": node})
    for neighbor in adjacencyList[node]:
        connectedComponents[-1]["edges"].append({"source": node, "target": neighbor, "type": 3})
        if visit[neighbor] == 0:
            DFS(neighbor)


def findComponents():
    # 找出所有的连通域 for key in a和 for key in a.keys():完全等价。
    componentNum = 0

    for key in visit:
        if visit[key] == 0:
            # 代表一个新的联通子图
            componentNum += 1
            # 增加一个新的连通子图
            connectedComponents.append({"nodes": [], "edges": []})
            DFS(key)

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
        with open("./top10Components/top" + str(i) + ".json", "w") as f:
            json.dump(connectedComponents[i], f, indent=2)