if __name__ == '__main__':
    from LRDFA import LRDFANode
else:
    from SynAnalyze.LRDFA import LRDFANode
import pandas as pd
import numpy as np
import os
from pyecharts import options as opts
from pyecharts.charts import Tree


class SynAnalyze(object):
    def __init__(self):
        self.firstSet = dict()  # 终结符和非终结符的first集
        self.productions = list()  # 产生式列表
        self.terminators = list()  # 终结符集合
        self.nonTerminators = list()  # 非终结符集合
        self.productionsDict = dict()  # 将产生式集合按照左侧的非终结符归类
        self.LRTable = dict()  # LR(1)分析表

    def readSynGrammar(self, filename):
        for line in open(filename, 'r'):
            line = line.strip()
            cur_left = line.split(':')[0]
            cur_right = line.split(':')[1]
            right_list = list()
            # 产生式右侧不止一个元素
            if cur_right.find(' ') != -1:
                right_list = cur_right.split(' ')
            # 产生式右侧就一个元素
            else:
                right_list.append(cur_right)
            production = {cur_left: right_list}
            self.productions.append(production)

    def getTerminatorsAndNon(self):
        all_elem = list()
        for production in self.productions:
            for left in production.keys():
                if left not in self.productionsDict:
                    self.productionsDict[left] = list()
                self.productionsDict[left].append((
                    tuple(production[left]),
                    self.productions.index(production)))  # 待思考，或许只要存index
                if left not in all_elem:
                    all_elem.append(left)
                if left not in self.nonTerminators:
                    self.nonTerminators.append(left)
                for right in production[left]:
                    if right not in all_elem:
                        all_elem.append(right)

        # 终结符集合 = 所有元素 - 非终结符集合
        # self.terminators = all_elem - self.nonterminators
        for i in all_elem:
            if i not in self.nonTerminators:
                self.terminators.append(i)

    def getFirstSetForOne(self, cur_status, is_visit):
        # 如果当前符号的first集已经算过，则直接返回
        if cur_status in self.firstSet.keys():
            return self.firstSet[cur_status]
        cur_first_set = list()
        # 如果当前符号是终结符，则返回该终结符
        if cur_status in self.terminators:
            if cur_status not in cur_first_set:
                cur_first_set.append(cur_status)
            return cur_first_set
        # 如果当前符号是非终结符，则继续计算
        if cur_status not in is_visit:
            is_visit.append(cur_status)
        # 对左边为该非终结符的所有产生式进行计算
        for right_list in self.productionsDict[cur_status]:
            flag = True
            for right in right_list[0]:
                if right == '$':
                    cur_first_set.append('$')
                    break
                if right in is_visit:  # 如果该元素在递归过程中已经访问过，则不再计算
                    continue
                cur_set = self.getFirstSetForOne(right, is_visit)  # 递归求解
                if '$' in cur_set:
                    for i in cur_set:
                        if i not in cur_first_set:
                            cur_first_set.append(i)
                    cur_first_set.remove('$')
                else:
                    for i in cur_set:
                        if i not in cur_first_set:
                            cur_first_set.append(i)
                    flag = False
                    break
                if '$' not in cur_set:  # 如果当前符号不能推出空，则不在向后计算
                    break
            if flag:
                cur_first_set.append('$')

        return cur_first_set

    def getFirstSets(self):
        for terminator in self.terminators:
            self.firstSet[terminator] = self.getFirstSetForOne(
                terminator, list())
        for nonterminator in self.nonTerminators:
            self.firstSet[nonterminator] = self.getFirstSetForOne(
                nonterminator, list())

    # cur_item: (产生式编号，产生式左侧，产生式右侧符号列表，圆点位置，向前搜索符集合)
    def getClosure(self, cur_item, item_set):
        # item_set = list()
        item_set.append(cur_item)
        right_list = cur_item[2]
        point_index = cur_item[3]
        tail_set = cur_item[4]
        # 圆点后为非终结符才继续增大项目集
        if point_index < len(right_list) and (right_list[point_index] in self.nonTerminators):
            # 计算以该非终结符为左侧的产生式的向前搜索符集合
            new_tail_set = list()
            flag = True
            for i in range(point_index + 1, len(right_list)):
                cur_first_set = self.firstSet[right_list[i]]
                if '$' in cur_first_set:
                    for j in cur_first_set:
                        if j != '$':
                            new_tail_set.append(j)
                else:
                    flag = False
                    for j in cur_first_set:
                        if j not in new_tail_set:
                            new_tail_set.append(j)
                    break
            if flag:
                for j in tail_set:
                    if j not in new_tail_set:
                        new_tail_set.append(j)
            # 对以圆点后非终结符为左侧的产生式进行遍历
            for pro_list in self.productionsDict[right_list[point_index]]:
                new_item = (pro_list[1], right_list[point_index],
                            pro_list[0], 0, tuple(new_tail_set))
                if new_item not in item_set:  # 递归计算
                    for i in self.getClosure(new_item, item_set):
                        if i not in item_set:
                            item_set.append(i)
            # 合并项目集中产生式相同的项目
            new_item_set = dict()
            for item in item_set:
                pro_key = (item[0], item[1], item[2], item[3])
                if tuple(pro_key) not in new_item_set.keys():
                    new_item_set[tuple(pro_key)] = list()
                for i in item[4]:
                    if i not in new_item_set[tuple(pro_key)]:
                        new_item_set[tuple(pro_key)].append(i)
            item_set = list()
            for key in new_item_set.keys():
                final_item = (key[0], key[1], key[2], key[3],
                              tuple(new_item_set[key]))
                if tuple(final_item) not in item_set:
                    item_set.append(tuple(final_item))
        return item_set

    def createLRTable(self, LRTable_path):
        all_status = dict()
        all_item_set = dict()

        def getLRDFANode(id):
            if id in all_status:
                return all_status[id]
            else:
                node = LRDFANode(id)
            return node
        # 建立开始项目集 I0
        start_id = 0
        start_node = getLRDFANode(start_id)
        start_item_set = self.getClosure(
            (0, 'sstart', ('start',), 0, ('#',)), list())
        start_node.addItemSetBySet(start_item_set)
        all_item_set[tuple(start_item_set)] = start_id
        all_status[start_id] = start_node
        # BFS
        queue = list()
        queue.append(start_node)
        moving_id = 0  # 动态生成项目集编号
        while queue:
            now_node = queue.pop(0)
            now_item_set = now_node.itemSet
            now_node_id = now_node.id
            is_visit = list()
            is_visit.clear()
            for item in now_item_set:
                if item in is_visit:
                    continue
                is_visit.append(item)
                pro_id = item[0]
                left = item[1]
                right_list = item[2]
                point_index = item[3]
                tail_set = item[4]
                if point_index >= len(right_list) or '$' in right_list:  # 归约
                    if now_node_id not in self.LRTable.keys():  # 为当前项目集在LR分析表中创立表项
                        self.LRTable[now_node_id] = dict()
                    for tail in tail_set:
                        if tail in self.LRTable[now_node_id].keys():
                            print('当前文法不属于LR(1)文法！！！')
                            return
                        if pro_id:
                            self.LRTable[now_node_id][tail] = (
                                'r', pro_id)  # 用第 pro_id 个产生式进行归约
                        else:
                            self.LRTable[now_node_id][tail] = ('acc',)
                else:
                    next_item = (pro_id, left, right_list,
                                 point_index + 1, tail_set)
                    next_item_set = self.getClosure(next_item, list())
                    next_c = right_list[point_index]
                    for ex_item in now_item_set:  # 对后一个字符相同的其他产生式也要求闭包，并取并
                        if ex_item in is_visit:
                            continue
                        ex_right_list = ex_item[2]
                        ex_point_index = ex_item[3]
                        if ex_point_index < len(ex_right_list) and ex_right_list[ex_point_index] == next_c:
                            if ex_item not in is_visit:
                                is_visit.append(ex_item)
                            ex_next_item = (
                                ex_item[0], ex_item[1], ex_item[2], ex_point_index + 1, ex_item[4])
                            for i in self.getClosure(ex_next_item, list()):
                                if i not in next_item_set:
                                    next_item_set.append(i)
                    # 合并项目集中产生式相同的项目
                    new_item_set = dict()
                    for iitem in next_item_set:
                        pro_key = (iitem[0], iitem[1], iitem[2], iitem[3])
                        if tuple(pro_key) not in new_item_set.keys():
                            new_item_set[tuple(pro_key)] = list()
                        for i in iitem[4]:
                            if i not in new_item_set[tuple(pro_key)]:
                                new_item_set[tuple(pro_key)].append(i)
                    next_item_set = list()
                    for key in new_item_set.keys():
                        final_item = (key[0], key[1], key[2],
                                      key[3], tuple(new_item_set[key]))
                        if tuple(final_item) not in next_item_set:
                            next_item_set.append(tuple(final_item))
                    if tuple(next_item_set) in all_item_set.keys():  # 该项目集已经处理过
                        next_node_id = all_item_set[tuple(next_item_set)]
                    else:  # 新建一个项目集
                        moving_id += 1
                        next_node_id = moving_id
                        all_item_set[tuple(next_item_set)] = next_node_id
                        next_node = getLRDFANode(next_node_id)
                        next_node.addItemSetBySet(next_item_set)
                        all_status[next_node_id] = next_node
                        queue.append(next_node)
                    if now_node_id not in self.LRTable.keys():  # 为当前项目集在LR分析表中创立表项
                        self.LRTable[now_node_id] = dict()
                    if right_list[point_index] in self.LRTable[now_node_id].keys():
                        print('当前文法不属于LR(1)文法！！！')
                        return
                    if right_list[point_index] in self.terminators:
                        self.LRTable[now_node_id][right_list[point_index]] = (
                            'S', next_node_id)
                    else:
                        self.LRTable[now_node_id][right_list[point_index]] = (
                            'G', next_node_id)
        actColumns = self.terminators
        actColumns.append("#")
        action = pd.DataFrame(index=list(
            self.LRTable.keys()), columns=actColumns)
        goto = pd.DataFrame(index=list(self.LRTable.keys()),
                            columns=self.nonTerminators)
        for i in self.LRTable.keys():
            for j in self.LRTable[i].keys():
                if self.LRTable[i][j][0] == 'G':
                    goto[j][i] = self.LRTable[i][j]
                else:
                    action[j][i] = self.LRTable[i][j]
        action[np.nan] = np.nan
        table = action.join(goto)
        table = table.drop(['$'], axis=1)
        table.to_csv(LRTable_path)
        #print("LR table:")
        # print(table)

    def runOnLRTable(self, tokens):
        status_stack = [0]  # 状态栈
        symbol_stack = [('#', -1, 1)]  # 符号栈
        tree_layer = list()
        tree_layer_num = list()
        tree_line = list()
        tokens.reverse()
        isSuccess = False
        step = 0
        while True:
            step += 1
            top_status = status_stack[-1]
            now_line_num, now_token = tokens[-1]
            # print('token: ' + now_token)
            # print('symbol stack:')
            # print(symbol_stack)
            # print('status stack:')
            # print(status_stack)
            # print()
            # os.system("pause")
            if now_token in self.LRTable[top_status].keys():  # 进行状态转移
                action = self.LRTable[top_status][now_token]
                if action[0] == 'acc':
                    isSuccess = True
                    break
                elif action[0] == 'S':
                    if len(tree_layer_num) == 0:
                        tree_layer_num.append(0)
                    else:
                        tree_layer_num[0] += 1
                    status_stack.append(action[1])
                    symbol_stack.append((now_token, 0, tree_layer_num[0]))
                    tree_layer.append((now_token, 0, tree_layer_num[0]))
                    tokens = tokens[:-1]
                elif action[0] == 'r':
                    production = self.productions[action[1]]
                    left = list(production.keys())[0]
                    next_line = 0
                    if production[left] != ['$']:  # 不需修改两个栈
                        right_length = len(production[left])
                        status_stack = status_stack[:-right_length]
                        #symbol_stack = symbol_stack[:-right_length]
                        for i in range(len(symbol_stack) - 1, len(symbol_stack) - right_length - 1, -1):
                            next_line = max(next_line, symbol_stack[i][1])
                            tree_line.append(
                                [symbol_stack[i][1], symbol_stack[i][2], 0, 0])
                            symbol_stack.pop(i)
                        next_line += 1
                    else:
                        next_line = 1
                        right_length = 1
                        if len(tree_layer_num) == 0:
                            tree_layer_num.append(0)
                        else:
                            tree_layer_num[0] += 1
                        tree_layer.append(('$', 0, tree_layer_num[0]))
                        tree_line.append([0, tree_layer_num[0], 0, 0])
                    go = self.LRTable[status_stack[-1]][left]  # 归约时判断接下来的状态
                    if next_line == len(tree_layer_num):
                        tree_layer_num.append(0)
                    else:
                        tree_layer_num[next_line] += 1
                    for i in tree_line[-right_length:]:
                        i[2], i[3] = next_line, tree_layer_num[next_line]
                    status_stack.append(go[1])
                    symbol_stack.append(
                        (left, next_line, tree_layer_num[next_line]))
                    tree_layer.append(
                        (left, next_line, tree_layer_num[next_line]))
            else:  # 无法进行状态转移，报错
                print('line %s' % now_line_num)
                print('found: %s' % now_token)
                print('expecting:')
                for exp in self.LRTable[top_status].keys():
                    print(exp)
                break
        return isSuccess, tree_layer, tree_line

    def get_tree(self, tree_layer, tree_line):
        pre_data = dict()
        for i in tree_layer:
            if i[1] not in pre_data:
                pre_data[i[1]] = list()
            pre_data[i[1]].append({'name': i[0]})
        for i in tree_line:
            if 'children' not in pre_data[i[2]][i[3]]:
                pre_data[i[2]][i[3]]['children'] = list()
            pre_data[i[2]][i[3]]['children'].insert(
                0, pre_data[i[0]][i[1]])
        data = pre_data[max(pre_data.keys())]
        Syn_tree = Tree().add("", data, orient="TB").set_global_opts(
            title_opts=opts.TitleOpts(title="Syn_Tree"))
        Syn_tree.render()

    def analyze(self, filename):
        token_table = open(filename, 'r')
        tokens = list()
        for line in token_table:
            line = line[:-1]
            next_token_type = line.split(' ')[1]
            if next_token_type == 'identifier' or next_token_type == 'number':
                tokens.append((line.split(' ')[0], next_token_type))
            else:
                next_token = line.split(' ')[2]
                tokens.append((line.split(' ')[0], next_token))
        tokens.append((str(0), '#'))
        isSuccess, tree_layer, tree_line = self.runOnLRTable(tokens)
        self.get_tree(tree_layer, tree_line)
        if isSuccess:
            print('Syntax Analyze Successfully!')
        else:
            print('Syntax Error!')


if __name__ == '__main__':
    SynGrammar_path = './SynGrammar.txt'  # 语法规则文件相对路径
    TokenTable_path = '../LexAnalyze/TOKEN-TABLE/token_table.data'  # 存储TOKEN表的相对路径
    LRTable_path = './LR-TABLE/LR-Table.csv'  # 存储LR表的相对路径

    syn_ana = SynAnalyze()
    syn_ana.readSynGrammar(SynGrammar_path)
    syn_ana.getTerminatorsAndNon()
    syn_ana.getFirstSets()
    syn_ana.createLRTable(LRTable_path)
    syn_ana.analyze(TokenTable_path)
