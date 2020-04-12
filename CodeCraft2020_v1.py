import os
import numpy as np

# -------------------输入输出--------------------------


def readData(filename):
    data = []
    f = open(filename)
    for line in f:
        line = list(map(int, line.split(',')))
        data.append(line)
    return data


def writeFile(fileName, res, t1, t2):
    f = open(fileName, 'w')
    f.write(str(len(res))+'\n')
    for r in res:
        for i in range(len(r)-1):
            f.write(t1[r[i]])
        f.write(t2[r[i]])

# ------------------点编号转换为连续id---------------------


def convert(data):
    l = []
    d = {}
    for line in data:
        l.append(line[0])
        l.append(line[1])
    st = list(set(l))
    for i in range(len(st)):
        d[st[i]] = i
    for i in range(len(data)):
        data[i][0] = d[data[i][0]]
        data[i][1] = d[data[i][1]]
    trans1 = [str(v)+',' for v in st]
    trans2 = [str(v)+'\n' for v in st]
    return trans1, trans2, data

# -------------------建立邻接表-----------------------------


def createGraph(data, n):
    g = [[] for i in range(n)]
    g1 = [[] for i in range(n)]
    for line in data:
        g[line[0]].append(line[1])
        g1[line[1]].append(line[0])
    return g, g1

# -------------------深度遍历找环--------------------------


def dfs(g, k, p_o, visit, visit1, res, path):
    for i in range(len(g[k])):
        if g[k][i] == p_o:  # 如果下一个点是查询点，则找到了环
            if len(path) > 2:
                res.append(path.copy())
            continue
        if visit[g[k][i]] == 1 or g[k][i] < p_o or visit1[g[k][i]] != p_o:  # 如果下一个点是已经访问过的点，或者已经查询过的点
            continue
        if len(path) == 7:
            continue
        visit[g[k][i]] = 1  # 将下一个点设置为已访问，将点加入路径中
        path.append(g[k][i])
        dfs(g, g[k][i], p_o, visit, visit1, res, path)  # 访问下一个点
        path.pop()
        visit[g[k][i]] = 0

# ----------------------剪枝操作-----------------------------


def dfs1(g, k, p_o, visit, visit1, length):
    for i in range(len(g[k])):
        if g[k][i] < p_o or visit[g[k][i]] == 1:
            continue
        visit1[g[k][i]] = p_o
        if length == 3:
            continue
        visit[g[k][i]] = 1
        dfs1(g, g[k][i], p_o, visit, visit1, length+1)
        visit[g[k][i]] = 0


if __name__ == "__main__":
    # -------------------输入---------------------------
    data = readData('test_data.txt')
    t1, t2, data = convert(data)

    # --------------------处理----------------------------
    n = len(t1)
    g, g1 = createGraph(data, n)
    visit = [0 for i in range(n)]
    visit1 = [-1 for i in range(n)]
    path = []
    res = []
    for i in range(n):
        path.append(i)
        dfs1(g, i, i, visit, visit1, 1)
        dfs1(g1, i, i, visit, visit1, 1)
        dfs(g, i, i, visit, visit1, res, path)
        path.pop()
        # if i % 100 == 0:
        #     print(i)

    # ---------------------输出-------------------------
    print(len(res))
    res.sort(key=lambda x: len(x))
    writeFile('result.txt', res, t1, t2)
