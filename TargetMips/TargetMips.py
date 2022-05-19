TargetMap = dict()  #二元组 {序号:(myjump,mips语句)}
regMap = dict()
tep = 2  #$1 $0另有用处


def is_number(s):
    try:  # 如果能运行float(s)语句，返回True（字符串s是浮点数）
        float(s)
        return True
    except ValueError:  # ValueError为Python的一种标准异常，表示"传入无效的参数"
        pass  # 如果引发了ValueError这种异常，不做任何事情（pass：不做任何事情，一般用做占位语句）
    try:
        import unicodedata  # 处理ASCii码的包
        unicodedata.numeric(s)  # 把一个表示数字的字符串转换为浮点数返回的函数
        return True
    except (TypeError, ValueError):
        pass
    return False


def to_number_or_reg(s):
    try:
        return int(s)
    except:
        try:
            return float(s)
        except:
            try:
                return regMap[s]
            except:
                return s


def tranToMips(code: tuple):
    a = to_number_or_reg(code[1][1])
    b = to_number_or_reg(code[1][2])
    c = to_number_or_reg(code[1][3])
    if "j" in code[1][0]:
        jump_note = f"myjump{code[1][3]}"  #成功分支跳转地
        TargetMap[code[1][3]][0] = jump_note  #跳转的地方加个myjump标记
        jump_next = f"myjump{code[0]+1}"  #下一条
        if code[1][0] == 'j':
            TargetMap[code[0]][1] = f"j {jump_note}"  #翻译
        elif code[1][0] == 'j>':
            if is_number(code[1][1]):  #a是数字
                if is_number(code[1][2]):  #b也是数字
                    if (a > b):
                        TargetMap[code[0]][1] = f"j {jump_note}"  #翻译
                    else:  #不可能执行到这里
                        TargetMap[code[0]][1] = ""  #空即可
                        pass
                else:  #b不是数字
                    TargetMap[code[0]][1] = f"sltiu $1,{b},{a}" + "\n"

                    #b<a时(判定为1)跳
                    TargetMap[code[0]][1] += f"bne $1,$0,{jump_note}"

            else:  #a不是数字
                TargetMap[code[0] + 1][0] = jump_next  #若相等直接下一条
                TargetMap[code[0]][1] = f"beq {a},{b},{jump_next}" + "\n"

                if is_number(code[1][2]):  #b是数字
                    TargetMap[code[0]][1] += f"sltiu $1,{a},{b}" + "\n"
                else:  #b也不是数字
                    TargetMap[code[0]][1] += f"sltu $1,{a},{b}" + "\n"

                #a<b时(判定为1)不跳
                TargetMap[code[0]][1] += f"beq $1,$0,{jump_note}"
        elif code[1][0] == 'j>=':
            if is_number(code[1][1]):  #a是数字
                if is_number(code[1][2]):  #b也是数字
                    if (a >= b):
                        TargetMap[code[0]][1] = f"j {jump_note}"  #翻译
                    else:  #不可能执行到这里
                        TargetMap[code[0]][1] = ""  #空即可
                        pass
                else:  #b不是数字
                    TargetMap[code[0]][1] = f"beq {b},{a},{jump_note}" + "\n"
                    TargetMap[code[0]][1] += f"sltiu $1,{b},{a}" + "\n"

                    #b<a时(判定为1)跳
                    TargetMap[code[0]][1] += f"bne $1,$0,{jump_note}"

            else:  #a不是数字
                TargetMap[code[0]][1] = f"beq {a},{b},{jump_note}" + "\n"
                if is_number(code[1][2]):  #b是数字
                    TargetMap[code[0]][1] += f"sltiu $1,{a},{b}" + "\n"
                else:  #b也不是数字
                    TargetMap[code[0]][1] += f"sltu $1,{a},{b}" + "\n"

                #a<b时(判定为1)不跳
                TargetMap[code[0]][1] += f"beq $1,$0,{jump_note}"
        elif code[1][0] == 'j<':
            if is_number(code[1][1]):  #a是数字
                if is_number(code[1][2]):  #b也是数字
                    if (a < b):
                        TargetMap[code[0]][1] = f"j {jump_note}"  #翻译
                    else:  #不可能执行到这里
                        TargetMap[code[0]][1] = ""  #空即可
                        pass
                else:  #b不是数字
                    TargetMap[code[0]][1] = f"sltiu $1,{b},{a}" + "\n"

                    #b<a时(判定为1)不跳
                    TargetMap[code[0]][1] += f"beq $1,$0,{jump_note}"

            else:  #a不是数字
                TargetMap[code[0] + 1][0] = jump_next  #若相等直接下一条
                TargetMap[code[0]][1] = f"beq {a},{b},{jump_next}" + "\n"

                if is_number(code[1][2]):  #b是数字
                    TargetMap[code[0]][1] += f"sltiu $1,{a},{b}" + "\n"
                else:  #b也不是数字
                    TargetMap[code[0]][1] += f"sltu $1,{a},{b}" + "\n"

                #a<b时(判定为1)跳
                TargetMap[code[0]][1] += f"bne $1,$0,{jump_note}"
        elif code[1][0] == 'j<=':
            if is_number(code[1][1]):  #a是数字
                if is_number(code[1][2]):  #b也是数字
                    if (a <= b):
                        TargetMap[code[0]][1] = f"j {jump_note}"  #翻译
                    else:  #不可能执行到这里
                        TargetMap[code[0]][1] = ""  #空即可
                        pass
                else:  #b不是数字
                    TargetMap[code[0]][1] = f"beq {b},{a},{jump_note}" + "\n"
                    TargetMap[code[0]][1] += f"sltiu $1,{b},{a}" + "\n"

                    #b<a时(判定为1)不跳
                    TargetMap[code[0]][1] += f"beq $1,$0,{jump_note}"

            else:  #a不是数字
                TargetMap[code[0]][1] = f"beq {a},{b},{jump_note}" + "\n"

                if is_number(code[1][2]):  #b是数字
                    TargetMap[code[0]][1] += f"sltiu $1,{a},{b}" + "\n"
                else:  #b也不是数字
                    TargetMap[code[0]][1] += f"sltu $1,{a},{b}" + "\n"

                #a<b时(判定为1)跳
                TargetMap[code[0]][1] += f"bne $1,$0,{jump_note}"
        elif code[1][0] == 'j==':
            if is_number(code[1][1]):  #a是数字
                if is_number(code[1][2]):  #b也是数字
                    if (a == b):
                        TargetMap[code[0]][1] = f"j {jump_note}"  #翻译
                    else:  #不可能执行到这里
                        TargetMap[code[0]][1] = ""  #空即可
                        pass
                else:  #b不是数字
                    TargetMap[code[0]][1] = f"beq {b},{a},{jump_note}"
            else:  #a不是数字
                TargetMap[code[0]][1] = f"beq {a},{b},{jump_note}"
        elif code[1][0] == 'j!=':
            if is_number(code[1][1]):  #a是数字
                if is_number(code[1][2]):  #b也是数字
                    if (a != b):
                        TargetMap[code[0]][1] = f"j {jump_note}"  #翻译
                    else:  #不可能执行到这里
                        TargetMap[code[0]][1] = ""  #空即可
                        pass
                else:  #b不是数字
                    TargetMap[code[0]][1] = f"bne {b},{a},{jump_note}"
            else:  #a不是数字
                TargetMap[code[0]][1] = f"bne {a},{b},{jump_note}"
    elif code[1][0] == '=':  #赋值
        TargetMap[code[0]][1] = f"add {c},$0,{a}"
    elif code[1][0] == '!':  #逻辑非
        if is_number(code[1][1]):  #a是数字
            if a != 0:
                TargetMap[code[0]][1] = f"add {c},$0,0"
            else:
                TargetMap[code[0]][1] = f"add {c},$0,1"
        else:  #a不是数字
            bne_branch = f"bne_branch{code[0]}"
            TargetMap[code[0]][1] = f"bne {a},$0,{bne_branch}" + "\n"  #a不等于0就跳
            TargetMap[code[0]][1] += f"add {c},$0,1" + '\n'
            TargetMap[code[0]][1] += f"{bne_branch}:" + '\n' + f"add {c},$0,0"
    elif code[1][0] == '~':  #按位取反
        if is_number(code[1][1]):  #a是数字
            TargetMap[code[0]][1] = f"add {c},$0,{~a}"
        else:  #a不是数字
            TargetMap[code[0]][1] = f"xori {c},{a},0xffffffff"  #与全1按位异或即可取反
    elif code[1][0] == '+':
        if is_number(code[1][1]):  #a是数字
            if is_number(code[1][2]):  #b也是数字
                TargetMap[code[0]][1] = f"add {c},$0,{a+b}"  #翻译
            else:  #b不是数字
                TargetMap[code[0]][1] = f"add {c},{b},{a}"
        else:  #a不是数字
            TargetMap[code[0]][1] = f"add {c},{a},{b}"
    elif code[1][0] == '-':
        if is_number(code[1][1]):  #a是数字
            if is_number(code[1][2]):  #b也是数字
                TargetMap[code[0]][1] = f"add {c},$0,{a-b}"  #翻译
            else:  #b不是数字
                TargetMap[code[0]][1] = f"sub {c},{b},{a}"
        else:  #a不是数字
            TargetMap[code[0]][1] = f"sub {c},{a},{b}"
    elif code[1][0] == '&':  #按位与
        if is_number(code[1][1]):  #a是数字
            if is_number(code[1][2]):  #b也是数字
                TargetMap[code[0]][1] = f"add {c},$0,{a&b}"  #翻译
            else:  #b不是数字
                TargetMap[code[0]][1] = f"and {c},{b},{a}"
        else:  #a不是数字
            TargetMap[code[0]][1] = f"and {c},{a},{b}"
    elif code[1][0] == '|':  #按位或
        if is_number(code[1][1]):  #a是数字
            if is_number(code[1][2]):  #b也是数字
                TargetMap[code[0]][1] = f"add {c},$0,{a|b}"  #翻译
            else:  #b不是数字
                TargetMap[code[0]][1] = f"or {c},{b},{a}"
        else:  #a不是数字
            TargetMap[code[0]][1] = f"or {c},{a},{b}"
    elif code[1][0] == '^':  #按位异或
        if is_number(code[1][1]):  #a是数字
            if is_number(code[1][2]):  #b也是数字
                TargetMap[code[0]][1] = f"add {c},$0,{a^b}"  #翻译
            else:  #b不是数字
                TargetMap[code[0]][1] = f"xor {c},{b},{a}"
        else:  #a不是数字
            TargetMap[code[0]][1] = f"xor {c},{a},{b}"
    elif code[1][0] == '*':  #乘法
        if is_number(code[1][1]):  #a是数字
            if is_number(code[1][2]):  #b也是数字
                TargetMap[code[0]][1] = f"add {c},$0,{a*b}"  #翻译
            else:  #b不是数字
                TargetMap[code[0]][1] = f"mul {c},{b},{a}"
        else:  #a不是数字
            TargetMap[code[0]][1] = f"mul {c},{a},{b}"
    elif code[1][0] == '%':  #取模
        if is_number(code[1][1]):  #a是数字
            if is_number(code[1][2]):  #b也是数字
                TargetMap[code[0]][1] = f"add {c},$0,{a%b}"  #翻译
            else:  #b不是数字
                TargetMap[code[0]][1] = f"add $1,$0,{a}" + '\n'
                TargetMap[code[0]][1] += f"div {b},$1" + '\n'
                TargetMap[code[0]][1] += f"mfhi {c}"
        else:  #a不是数字
            TargetMap[code[0]][1] = f"add $1,$0,{b}" + '\n'
            TargetMap[code[0]][1] += f"div {a},$1" + '\n'
            TargetMap[code[0]][1] += f"mfhi {c}"
    elif code[1][0] == '/':  #除法
        if is_number(code[1][1]):  #a是数字
            if is_number(code[1][2]):  #b也是数字
                TargetMap[code[0]][1] = f"add {c},$0,{a//b}"  #翻译
            else:  #b不是数字
                TargetMap[code[0]][1] = f"add $1,$0,{a}" + '\n'
                TargetMap[code[0]][1] += f"div {b},$1" + '\n'
                TargetMap[code[0]][1] += f"mflo {c}"
        else:  #a不是数字
            TargetMap[code[0]][1] = f"add $1,$0,{b}" + '\n'
            TargetMap[code[0]][1] += f"div {a},$1" + '\n'
            TargetMap[code[0]][1] += f"mflo {c}"


def regInit(id: str):
    global tep
    if id not in regMap and not is_number(id):
        regMap[id] = f"${tep}"
        tep += 1


def ToMips(codes, reg_num=32) -> str:  #中间代码转mips汇编
    mips_code = ".text\n"

    for code in codes:
        #print(code)
        TargetMap[code[0]] = ["", ""]  #全填上去
        if 'j' not in code[1][0]:
            regInit(code[1][1])
            if code[1][0] != '=' and code[1][0] != '!' and code[1][0] != '~':
                regInit(code[1][2])  #单目运算符号和赋值语句除外
            regInit(code[1][3])
    TargetMap[codes[-1][0] + 1] = ["", ""]  #最后一个空的
    #print(regMap)

    for code in codes:
        tranToMips(code)
    #print(TargetMap)

    mips = sorted(list(TargetMap.items()), key=lambda x: x[0])
    for code in mips:
        if code[1][0] != "":
            mips_code += code[1][0] + ":" + "\n"
        mips_code += code[1][1] + "\n"
    return mips_code