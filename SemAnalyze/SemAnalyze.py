type_start = 5
type_end = 8
dep_start = 10
dep_end = 11
pri_start = 14
pri_end = 15
two_op_list = [
    45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 77, 78, 79, 80, 81, 82
]
assign_op_list = [18, 19, 20, 21, 22, 23, 24, 25, 26]
operator = [41, 39, 83, 85, 87]


class SemAnalyze(object):
    def __init__(self):
        self.temp = 0
        self.now = 100
        self.map = dict()
        self.varStack = list()
        self.opStack = list()
        self.TypeStack = list()
        self.gIdTable = list()
        self.iIdTable = list()
        self.error = list()
        self.warning = list()
        self.Mark = list()
        self.inMain = False
        self.linklist = list()
        self.nextlist = list()

    def show(self):
        print("codes:")
        for i in self.map:
            print(i, self.map[i])
        print("linklist:")
        print(self.linklist)
        print("nextlist:")
        print(self.nextlist)
        print("mark:")
        print(self.Mark)

    def SemAct(self, prod_id, token_list, line):
        #print(prod_id)
        if prod_id >= type_start and prod_id <= type_end:
            self.TypeStack.append(token_list[0][1])
        elif prod_id == 9:
            self.TypeStack.pop()
        elif prod_id == dep_start:
            name = token_list[0][0]
            if not self.inMain:
                for i in self.gIdTable:
                    if i[0] == name:
                        self.error.append(
                            f"line {line}:{token_list[0][0]} is Redefined")
                        return
            else:
                for i in self.iIdTable:
                    if i[0] == name:
                        self.error.append(
                            f"line {line}:{token_list[0][0]} is Redefined")
                        return
            tempName = self.varStack.pop()
            self.map[self.now] = ["=", tempName, "-", token_list[0][0]]
            self.now += 1
            if self.inMain:
                self.iIdTable.append([name, self.TypeStack[-1]])
            else:
                self.gIdTable.append([name, self.TypeStack[-1]])
        elif prod_id == dep_end:
            name = token_list[0][0]
            if not self.inMain:
                for i in self.gIdTable:
                    if i[0] == name:
                        self.error.append(
                            f"line {line}:{token_list[0][0]} is Redefined")
                        return
            else:
                for i in self.iIdTable:
                    if i[0] == name:
                        self.error.append(
                            f"line {line}:{token_list[0][0]} is Redefined")
                        return
            if self.inMain:
                self.iIdTable.append([name, self.TypeStack[-1]])
            else:
                self.gIdTable.append([name, self.TypeStack[-1]])
        elif prod_id >= pri_start and prod_id <= pri_end:
            if prod_id == pri_start:  #标识符
                exist = False
                for i in self.gIdTable:
                    if i[0] == token_list[0][0]:
                        exist = True
                if self.inMain:
                    for i in self.iIdTable:
                        if i[0] == token_list[0][0]:
                            exist = True
                if not exist:
                    self.warning.append(
                        f"line {line}:{token_list[0][0]} is Undefined")
            self.varStack.append(token_list[0][0])
        elif (prod_id in two_op_list) or (prod_id in assign_op_list):
            self.opStack.append(token_list[0][1])
        elif prod_id in operator:
            a = self.varStack.pop()
            b = self.varStack.pop()
            op = self.opStack.pop()
            self.temp += 1
            self.varStack.append(f"$TEMP{self.temp}")
            self.map[self.now] = [op, b, a, f"$TEMP{self.temp}"]
            self.now += 1
        elif prod_id == 27:
            op = self.opStack.pop()
            a = self.varStack.pop()
            if len(op) == 1:
                self.map[self.now] = [op, a, "-", token_list[0][0]]
            else:
                op = op[0]
                self.map[self.now] = [
                    op, token_list[0][0], a, token_list[0][0]
                ]
            self.now += 1
        elif prod_id == 36:  #E->id 布尔表达式变成标识符或数字
            #self.linklist.append([[], []])
            #self.linklist[-1][0].extend(e2[0])
            #self.linklist[-1][0].extend(e1[0])
            #self.linklist[-1][1].extend(e2[1])
            pass
        elif prod_id == 43:
            #e = self.linklist.pop()
            #self.linklist.append([[], []])  ##gzy
            #self.linklist[-1][0].extend(e[1])
            #self.linklist[-1][1].extend(e[0])

            a = self.varStack.pop()
            op = self.opStack.pop()
            self.temp += 1
            self.varStack.append(f"$TEMP{self.temp}")
            self.map[self.now] = [op, a, "-", f"$TEMP{self.temp}"]
            self.now += 1
        elif prod_id in [58, 59]:
            self.inMain = True
        elif prod_id == 76:
            self.nextlist.append([self.now])
            self.map[self.now] = ["j", "-", "-", 0]
            self.now += 1
        elif prod_id == 75:
            self.Mark.append(self.now)
        elif prod_id == 73:
            self.map[self.now] = ["return", "-", "-", self.varStack.pop()]
            self.now += 1
            self.inMain = False
        elif prod_id == 74:
            self.map[self.now] = ["return", "-", "-", "-"]
            self.now += 1
            self.inMain = False
            self.warning.append(f"line {line} : functio main has no return")
        elif prod_id == 37:
            self.linklist.append([[self.now], [self.now + 1]])
            a = self.varStack.pop()
            b = self.varStack.pop()
            op = self.opStack.pop()
            self.map[self.now] = ["j" + op, b, a, 0]
            self.map[self.now + 1] = ["j", "-", "-", 0]
            self.now += 2
        elif prod_id == 35:
            e2 = self.linklist.pop()
            e1 = self.linklist.pop()
            mark = self.Mark.pop()
            for i in e1[0]:
                self.map[i][3] = mark
            self.linklist.append([[], []])
            self.linklist[-1][0].extend(e2[0])
            self.linklist[-1][1].extend(e1[1])
            self.linklist[-1][1].extend(e2[1])
        elif prod_id == 33:
            e2 = self.linklist.pop()
            e1 = self.linklist.pop()
            mark = self.Mark.pop()
            for i in e1[1]:
                self.map[i][3] = mark
            self.linklist.append([[], []])  ##gzy
            self.linklist[-1][0].extend(e2[0])
            self.linklist[-1][0].extend(e1[0])
            self.linklist[-1][1].extend(e2[1])
        elif prod_id in [62, 63, 64, 65, 66, 67, 68]:
            self.nextlist.append([])
        elif prod_id == 69:
            m2 = self.Mark.pop()
            m1 = self.Mark.pop()
            e = self.linklist.pop()
            s2 = self.nextlist.pop()
            n = self.nextlist.pop()
            s1 = self.nextlist.pop()
            for i in e[0]:
                self.map[i][3] = m1
            for i in e[1]:
                self.map[i][3] = m2
            s = s1 + s2 + n
            self.nextlist.append(s)
        elif prod_id == 70:
            e = self.linklist.pop()
            m = self.Mark.pop()
            s1 = self.nextlist.pop()
            for i in e[0]:
                self.map[i][3] = m
            s = s1 + e[1]
            #print("s:", s)
            self.nextlist.append(s)
        elif prod_id == 71:
            m2 = self.Mark.pop()
            m1 = self.Mark.pop()
            s1 = self.nextlist.pop()
            e = self.linklist.pop()
            for i in s1:
                self.map[i][3] = m1
            for i in e[0]:
                self.map[i][3] = m2
            self.nextlist.append(e[1])
            self.map[self.now] = ["j", "-", "-", m1]
            self.now += 1
        elif prod_id == 61:
            s = self.nextlist.pop()
            L1 = self.nextlist.pop()
            m = self.Mark.pop()
            for i in L1:
                self.map[i][3] = m
            self.nextlist.append(s)
        #elif prod_id == 60:
        #    m = self.Mark.pop()
        #    for i in self.nextlist[-1]:
        #        self.map[i][3] = m
        #self.show()  #  display
