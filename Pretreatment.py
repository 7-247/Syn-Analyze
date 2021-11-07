def removenote(string):
    CrossLine = False
    a, b = string.find('//'), string.find('/*')
    if a != -1 and (a < b or b == -1):
        string = string[:a]
    elif b != -1:
        c = string.find('*/')
        if c > b+1:
            string = string[c+2:]
            CrossLine, string = removenote(string)
        else:
            CrossLine = True
            string = string[:b]
    return CrossLine, string

# 入口参数为字符串型源代码,返回值为预处理之后包含每一行源代码的字符串


def Pretreatment(sourcecode):
    sourcecode = sourcecode.split('\n')
    lines = [i.strip() for i in sourcecode]
    newcode = list()
    CrossLine_note_Flag = False
    for i in lines:
        if len(i) == 0:
            continue
        if not CrossLine_note_Flag:
            CrossLine_note_Flag, i = removenote(i)
            if len(i):
                newcode.append(i)
        else:
            if i.find('*/') != -1:
                i = i[i.index('*/')+2:]
                CrossLine_note_Flag, i = removenote(i)
                if len(i):
                    newcode.append(i)
    return newcode
