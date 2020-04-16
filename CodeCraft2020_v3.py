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
    cnt = 0
    for r in res:
        cnt += len(r)
    f.write(str(cnt)+'\n')
    for rr in res:
        for r in rr:
            for i in range(len(r)-1):
                f.write(t1[r[i]])
            f.write(t2[r[len(r)-1]])

# ------------------点编号转换为连续id---------------------


def convert(data):
    l = []
    d = {}
    for line in data:
        l.append(line[0])
        l.append(line[1])
    st = list(set(l))
    st.sort()
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
    for i in range(n):
        g[i].sort()
        g1[i].sort()
    return g, g1

# -------------------深度遍历找环--------------------------


def dfs(g, k, p_o, visit, visit1, res, path):
    for i in range(len(g[k])):
        v = g[k][i]
        if v < p_o:
            continue
        if visit1[v] == -2 and visit[v] == 0:
            path.append(v)
            length = len(path)
            if length > 2:
                res[length-3].append(path.copy())
                # print(path)
            path.pop()
            # continue
        if visit[v] == 1 or (visit1[v] != p_o and visit1[v] != -2):
            continue
        if len(path) == 6 or v == p_o:
            continue
        visit[v] = 1  # 将下一个点设置为已访问，将点加入路径中
        path.append(v)
        dfs(g, v, p_o, visit, visit1, res, path)  # 访问下一个点
        path.pop()
        visit[v] = 0

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
    data = readData('/data/test_data.txt')
    t1, t2, data = convert(data)

    # --------------------处理----------------------------
    n = len(t1)
    g, g1 = createGraph(data, n)
    visit = [0 for i in range(n)]
    visit1 = [-1 for i in range(n)]  # 为-1则是被剪掉的点
    path = []
    res = [[] for i in range(5)]
    for i in range(n):
        path.append(i)
        dfs1(g, i, i, visit, visit1, 1)
        dfs1(g1, i, i, visit, visit1, 1)
        for j in range(len(g1[i])):
            visit1[g1[i][j]] = -2  # 将倒数第二个点标记为-2
        dfs(g, i, i, visit, visit1, res, path)
        path.pop()
        for j in range(len(g1[i])):
            visit1[g1[i][j]] = i
        # if i % 100 == 0:
        #     print(i)

    # ---------------------输出-------------------------
    print(len(res))
    # res.sort(key=lambda x: len(x))
    writeFile('/projects/student/result.txt', res, t1, t2)
