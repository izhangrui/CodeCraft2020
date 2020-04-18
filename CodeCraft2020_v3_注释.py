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
    st = list(set(l))  # 其实这儿求交集更好，懒得改了
    st.sort()  # 排个序，输出就不用排序了
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
    g1 = [[] for i in range(n)]  # 反向图
    for line in data:
        g[line[0]].append(line[1])
        g1[line[1]].append(line[0])
    for i in range(n):
        g[i].sort()  # 排序，为了输出有序
        g1[i].sort()
    return g, g1

# -------------------深度遍历找环--------------------------

# 6+1思路：利用反向图标记可能成为环的倒数第一个点，再进行深度为6的搜索，搜索到被标记的点则成环。


def dfs(g, k, p_o, visit, visit1, res, path):
    for i in range(len(g[k])):
        v = g[k][i]
        if v < p_o:  # 小于查询点p_o的点都不用访问
            continue

        if visit1[v] == -2 and visit[v] == 0:  # 当碰到倒数第一个点且这个点未被访问过，则找到一条路径
            path.append(v)  # 把倒数第一个点加入路径中
            length = len(path)
            if length > 2:
                res[length-3].append(path.copy())
            path.pop()

        if visit[v] == 1 or (visit1[v] != p_o and visit1[v] != -2):
            continue
        if len(path) == 6 or v == p_o:  # 当搜索长度到6 或者 访问到查询点p_o就不继续访问了
            continue
        visit[v] = 1  # 访问v
        path.append(v)
        dfs(g, v, p_o, visit, visit1, res, path)
        path.pop()
        visit[v] = 0  # 退出v点，取消访问标记

# ----------------------剪枝操作-----------------------------

# 3邻域剪枝思路：如果将图看作是无向图，一个点数为7的环中，距离起点最远的点距离不超过3


def dfs1(g, k, p_o, visit, visit1, length):
    for i in range(len(g[k])):
        if g[k][i] < p_o or visit[g[k][i]] == 1:  # 1.小于查询点p_o的点都不用访问了;  2.当前查询中已经访问过的点不用再访问;
            continue
        # p_o为当前查找环的点，把距离p_o小于等于3的点标记为p_o(也可以标记为1，不过结束查询p_o点之后要，重新标记为-1)
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
    visit1 = [-1 for i in range(n)]  # 确定3邻域
    path = []
    res = [[] for i in range(5)]  # 长度分别为3，4，5，6，7的路径
    for i in range(n):
        # --------------3邻域剪枝----------------------------------
        # 分别遍历g,g1确定查询点i的3邻域
        # 把距离小于3的点的visit1标记为i，这样就确定了3邻域(不标记为1或者0是因为每次循环不用重新初始化visit1，为了省时间)
        dfs1(g, i, i, visit, visit1, 1)
        dfs1(g1, i, i, visit, visit1, 1)

        # --------------深度遍历找环--------------------------------
        for j in range(len(g1[i])):
            # 将倒数第一个点（6+1）visit1标记为-2，其实可以新建一个visit2来标记的，要容易理解些。
            visit1[g1[i][j]] = -2

        path.append(i)
        dfs(g, i, i, visit, visit1, res, path)  # 找查询点i的所有环
        path.pop()

        for j in range(len(g1[i])):
            visit1[g1[i][j]] = i  # 清除visit1 "-2" 的标记

    # ---------------------输出-------------------------
    writeFile('/projects/student/result.txt', res, t1, t2)
