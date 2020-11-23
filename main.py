import csv
import json

def processCsv():
    '''
    处理csv文件，统计一共有多少条属性为1和2的边，以及这些边涉及到多少个节点
    输出关于节点和边的json文件
    :return:
    '''

    # 输出项
    res = {}
    nodesLst = []
    edgesLst = []
    nodeId = set()          # 在一篇文章中看到使用set会更快 果然快了不止一点半点，这一块简直太重要了，好好复习

    res2 = {}
    nodesLst2 = []
    edgesLst2 = []
    nodeId2 = []

    with open("./data/mentor_protege_relation_univ_time_NeuroMath.csv", 'r') as f:
        f_csv = csv.reader(f)
        next(f_csv)
        count = 0

        for row in f_csv:
            edgeType = int(row[6])

            if edgeType == 1:
                sourceId = int(row[0])
                targetId = int(row[2])
                edge = {"source": sourceId, "target": targetId, "type": edgeType}
                edgesLst.append(edge)

                if sourceId not in nodeId:
                    nodeId.add(sourceId)
                    sourceNode = {"id": sourceId}
                    nodesLst.append(sourceNode)

                if targetId not in nodeId:
                    nodeId.add(targetId)
                    targetNode = {"id": targetId}
                    nodesLst.append(targetNode)

            elif edgeType == 2:
                sourceId = int(row[0])
                targetId = int(row[2])
                edge = {"source": sourceId, "target": targetId, "type": edgeType}
                edgesLst2.append(edge)

                if sourceId not in nodeId2:
                    nodeId2.append(sourceId)
                    sourceNode = {"id": sourceId}
                    nodesLst2.append(sourceNode)

                if targetId not in nodeId2:
                    nodeId2.append(targetId)
                    targetNode = {"id": targetId}
                    nodesLst2.append(targetNode)




            count += 1

            print(count)

        res["nodes"] = nodesLst
        res["edges"] = edgesLst

        res2["nodes"] = nodesLst2
        res2["edges"] = edgesLst2

        print("节点的个数", len(nodesLst))
        print("边的个数", len(edgesLst))
        print("节点的个数2", len(nodesLst2))
        print("边的个数2", len(edgesLst2))

    with open("relation_1.json", "w") as f:
        json.dump(res, f, indent=2)

    with open("relation_2.json", "w") as f:
        json.dump(res2, f, indent=2)

if __name__ == "__main__":
    processCsv()