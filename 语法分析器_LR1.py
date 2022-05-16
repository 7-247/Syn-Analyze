import os

start_symbol = ""  # 初始符号
symbol = set()  # 所有符号集合
terminal_symbol = set()  # 终结符集合
non_terminal_symbol = set()  # 非终结符集合

产生式 = []  # {'left': "S'", 'right': ['S']}
项目 = []  # {'left': "S'", 'right': ['S'], 'point': 0}
新项目 = []  # {'left': "S'", 'right': ['S'], 'point': 0, "origin": 0, "accept": "#"}
首项 = {}  # 每个非终结符B的形如B→·C的产生式的序号 首项['S']={2, 5}

closure = []  # 每个项目的闭包 closure[0]={0, 2, 5, 7, 10}
closureSet = []  # 项目集族 closureSet[0]={0, 2, 5, 7, 10}

goto = [] # go[状态i][符号j] 该数组依次存储了不同内容，分别为： 
# = Closure{项目x, 项目y}
# = {项目x, 项目y, 项目z}
# = 状态k
# 进入Action/Goto环节后，go函数会被转换为goto函数
# goto[状态i][符号j]=0:accept / +x:移进字符和状态x（sx）/ -x:用产生式x归约（rx）/ 无定义:err


first = {} # first['F']={'(', 'a', 'b', '^'}
first_empty = []  # first集中含有空的非终结符集合 {"E'", "T'", "F'"}

gotoFile = open(r'output\\goto.txt', 'w', encoding="utf-8")
firstFile = open(r'output\\first.txt', 'w', encoding="utf-8")
productionFile = open(r'output\\production.txt', 'w', encoding="utf-8")
closureFile = open(r'output\\closure.txt', 'w', encoding="utf-8")
lrFile = open(r'output\\lr.txt', 'w', encoding="utf-8")
analyzeFile = open(r'output\\analyze.txt', 'w', encoding="utf-8")
xmjzFile = open(r'output\\xmjz.txt', 'w', encoding="utf-8")


# 传入项目集(列表，内含项目编号)，推得其closure；判断是否已存在
# 若不存在，命名新项目集族，并求Goto。
def find_Goto(i):
    global symbol, closure
    #print(i)
    for j in closureSet[i]:
        #print("  ", j)
        item = 新项目[j]
        try:
            nowCharacter = item["right"][item["point"]]
            if nowCharacter in goto[i]:
                goto[i][nowCharacter].append(j + len(terminal_symbol))
            else:
                goto[i][nowCharacter] = [j + len(terminal_symbol)]
        except:
            pass
    for j in symbol:
        if j in goto[i]:  # goto(i, j)
            newSet = set()
            for itemOrd in goto[i][j]:
                newSet |= closure[itemOrd]
            print("Goto(I%d,%s) = Closure(" % (i, j), goto[i][j], ') =', newSet, "={", end=" ", file=gotoFile)
            for k in newSet:
                print(新项目[k]["left"], "->", ''.join(新项目[k]["right"]), ",", 新项目[k]["accept"], end=" ", sep="", file=gotoFile)
            print("}", end=" ", file=gotoFile)
            #print("len(ClosureSet)=", len(closureSet))
            if newSet in closureSet:
                goto[i][j] = closureSet.index(newSet)
            else:
                closureSet.append(newSet)
                goto.append({})
                goto[i][j] = len(closureSet) - 1
            print('= I', goto[i][j], sep="", file=gotoFile)
    print(i, closureSet[i], file=xmjzFile)


# 求项目i的Closure
def find_closure(i, ini):
    #print("find_closure", i)
    global closure
    #if len(closure[i]) > 0:
    #    return closure[i]

    item = 新项目[i]
    try:
        nowCharacter = item["right"][item["point"]]
        beta = ""
        alpha = item["accept"]
        fir = set()
        try:
            beta = item["right"][(item["point"] + 1):]
            beta += [alpha]
            for sym in beta:
                fir |= first[sym]
                if sym not in first_empty:
                    break
        except:
            fir = set(alpha)
        if nowCharacter in 首项:
            for j in 首项[nowCharacter]:
                if j not in closure[ini] and 新项目[j]["accept"] in fir:
                    #print(j)
                    closure[i].add(j)
                    closure[ini].add(j)
                    closure[i] |= find_closure(j, ini)
    except:
        closure[i].add(i)
        return {i}
    return closure[i]


with open("input\产生式.txt", encoding="utf-8") as f:
    for line in f:
        line = line.strip().replace('\n', ' ')
        #print(line)
        if line == "":
            continue
        line = line.split(':')
        terminal_symbol.add(line[0])
        symbol.add(line[0])
        if line[1] == '$':
            产生式.append({"left": line[0], "right": []})
        else:
            产生式.append({"left": line[0], "right": line[1].split(' ')})
            symbol |= (set(line[1].split(' ')))

start_symbol = 产生式[0]["left"]
symbol |= terminal_symbol
symbol -= {''}
terminal_symbol -= {''}
non_terminal_symbol = terminal_symbol
terminal_symbol = symbol - non_terminal_symbol
terminal_symbol |= {'#'}

#print(产生式)

#求First集
for item in non_terminal_symbol:
    first[item] = set()
for item in terminal_symbol:
    first[item] = {item}

bfs = []
for item in 产生式:
    try:
        sym = item["right"][0]
        if sym in terminal_symbol:
            first[item["left"]].add(sym)
    except:
        first_empty.append(item["left"])
        bfs.append(item["left"])

import copy

proCopy = copy.deepcopy(产生式)
while len(bfs) > 0:
    sym = bfs.pop(-1)
    for i, item in zip(range(len(proCopy)), proCopy):
        if item["left"] == sym:
            proCopy[i]["right"] = []
        elif sym in item["right"]:
            proCopy[i]["right"].remove(sym)
            if len(proCopy[i]["right"]) == 0:
                if item["left"] not in first_empty:
                    first_empty.append(item["left"])
                    bfs.append(sym)

print(first_empty, file=firstFile)

f = 1
while f:
    f = 0
    for item in 产生式:
        for sym in item["right"]:
            if not first[item["left"]].issuperset(first[sym]):
                f = 1
                first[item["left"]] |= first[sym]
            if sym not in first_empty:
                break
    #print(first, "\n")

for item in non_terminal_symbol:
    print("%s\n%s" % (item, " ".join(list(first[item]))), " $" if item in first_empty else "", "\n", file=firstFile)

# 获取所有项目
for order, i in zip(range(len(产生式)), 产生式):
    for j in range(len(i["right"]) + 1):
        项目.append({"left": i["left"], "right": i["right"], "point": j, "origin": order, "isTer": (j == len(i["right"]))})

for i, item in zip(range(len(项目)), 项目):
    for sym in terminal_symbol:
        closure.append(set())
        新项目.append(copy.deepcopy(item))
        新项目[-1]["accept"] = sym

for i, item in zip(range(len(新项目)), 新项目):
    if item["point"] == 0:
        if item["left"] in 首项:
            首项[item["left"]].add(i)
        else:
            首项[item["left"]] = {i}

print("项目：\n", 项目, "\n", file=productionFile)
print("新项目：\n", 新项目, "\n", file=productionFile)
print("原点在开头的产生式编号：\n", 首项, "\n", file=productionFile)

#print(新项目)

#求每个项目的闭包
print("单个项目的闭包：", file=closureFile)
for i, item in zip(range(len(新项目)), 新项目):
    print("%-4d " % i, item, file=closureFile)
    closure[i].add(i)
    closure[i] = find_closure(i, i)
    if item["origin"] == 0 and item["accept"] == '#' and item["point"] == 0:
        closureSet.append(closure[i])
    print("  ", closure[i], file=closureFile)

#print(closureSet[0])
goto.append({})

print("Goto：", file=gotoFile)
i = 0
while (i < len(closureSet)):
    find_Goto(i)
    i += 1
    print(file=gotoFile)

print("LR(1)分析器：", file=lrFile)
ts = sorted(list(terminal_symbol - {start_symbol}))
nts = sorted(list(non_terminal_symbol - {start_symbol}))
print("   ", '  '.join(map(lambda x: (x + "  ")[:3], ts)), "", '  '.join(map(lambda x: (x + "  ")[:3], nts)), file=lrFile)
for i in range(len(closureSet)):
    print("%-3d" % i, end=" ", file=lrFile)
    for item in closureSet[i]:
        k = item
        item = 新项目[item]
        if item["isTer"] == True:
            if item["accept"] in goto[i]:
                print("error!", "%d号项目集族的\t%s\t符号冲突，冲突的产生式为\t%d\t" % (i, item["accept"], k), 新项目[k])
                '''
                print("项目集族为：")
                for t in closureSet[i]:
                    print(t, 新项目[t])
                    '''
            else:
                goto[i][item["accept"]] = -item["origin"]
    for j in ts:
        try:
            if goto[i][j] > 0:
                print("s%-3d" % goto[i][j], end=" ", file=lrFile)
            if goto[i][j] < 0:
                print("r%-3d" % -goto[i][j], end=" ", file=lrFile)
            if goto[i][j] == 0:
                print("acc ", end=" ", file=lrFile)
        except:
            print("    ", end=" ", file=lrFile)
    for j in nts:
        try:
            print("%-4d" % goto[i][j], end=" ", file=lrFile)
        except:
            print("    ", end=" ", file=lrFile)
    print(file=lrFile)

names = ""
with open('intermediate\\names.txt', encoding="utf-8") as f:
    names = f.read()
names = names.strip().replace(' ', "").split('\n')
names = names[::-1]
names = list(filter(lambda x: x != "", names))
# print(names)
inp = "" # 分析栈
with open("intermediate\\processed_sourceCode.txt", encoding="utf-8") as f:
    inp = f.read()
inp = inp.strip().split('\n')
inp = list(filter(lambda x: x != "", inp))
inp += ['#']
print(inp, "的分析栈：", file=analyzeFile)
statusStack = [0] # 状态栈
charStack = ['#'] # 输入栈
pointer = 0
tree = []
for i in range(len(closureSet)):
    tree.append({})

root = -1
cntNode = -1
nodeStack = [] # 语法树结点 nodeStack[cntNode]["name"]="123" nodeStack[cntNode]["children"]=[1, 2, 3]
print("%-10s %-10s %-10s" % (' '.join(map(lambda x: str(x), statusStack)), ' '.join(charStack), ' '.join(inp[pointer:])), file=analyzeFile)
while True:
    c = inp[pointer]
    try:
        num = goto[statusStack[-1]][c]
        if num == 0:
            print("Accepted", file=analyzeFile)
            tree[statusStack[-1]]["name"] = charStack[-1]
            root = statusStack[-1]
            break
        elif num > 0:
            statusStack.append(num)
            #print(num, c)
            tree.append({})
            cntNode += 1
            tree[cntNode]["name"] = c
            nodeStack.append(cntNode)
            charStack.append(c)
            pointer += 1

            if c in ["identifier", "number"]:
                tree[cntNode]["children"] = [cntNode + 1]
                tree.append({})
                cntNode += 1
                tree[cntNode]["name"] = names.pop()

        elif num < 0:
            item = 产生式[-num]  # 用 item 规约
            if item["right"] == []:  # 空
                charStack += [item["left"]]
                statusStack.append(goto[statusStack[-1]][item["left"]])

                tree.append({})
                cntNode += 1
                tree[cntNode]["children"] = [cntNode + 1]
                tree[cntNode]["name"] = item["left"]
                nodeStack.append(cntNode)

                tree.append({})
                cntNode += 1
                tree[cntNode]["children"] = []
                tree[cntNode]["name"] = ''

            else:
                k = len(item["right"])
                statusStack = statusStack[:-k]
                charStack = charStack[:-k] + [item["left"]]
                statusStack.append(goto[statusStack[-1]][item["left"]])
                #print(statusStack[-1])
                tree.append({})
                cntNode += 1
                tree[cntNode]["children"] = []

                for i in range(k):
                    nowNode = nodeStack.pop()
                    tree[cntNode]["children"].append(nowNode)
                tree[cntNode]["children"] = tree[cntNode]["children"][::-1]
                tree[cntNode]["name"] = item["left"]
                nodeStack.append(cntNode)

    except:
        print("error", file=analyzeFile)
        break
    print("%-10s \t\t %-10s \t\t %-10s" % (' '.join(map(lambda x: str(x), statusStack)), ' '.join(charStack), ' '.join(inp[pointer:])), file=analyzeFile)


def outp(now):
    #print(now)
    if not tree[now]:
        return {}
    di = {}
    di["name"] = tree[now]["name"].replace("_", "_  \n") + ' '

    di["children"] = []
    if ("children" not in tree[now]) or (not tree[now]["children"]):
        return di
    for child in tree[now]["children"]:
        di["children"].append(outp(child))

    #print(now, di)
    return di


# print(root)
outpTree = outp(cntNode)
#print(outpTree)

from pyecharts import options as opts
from pyecharts.charts import Tree

treeData = [outpTree]
c = (
    Tree().add(
        "",
        treeData,
        orient="TB",
        initial_tree_depth=-1,
        #collapse_interval=10,
        symbol_size=3,
        is_roam=True,
        edge_shape="polyline",
        #is_expand_and_collapse=False,
        label_opts=opts.LabelOpts(
            position="top",
            horizontal_align="right",
            vertical_align="middle",
            #rotate='15',
            font_size=15)).set_global_opts(title_opts=opts.TitleOpts(title="语法树")).render("output\语法树.html"))
