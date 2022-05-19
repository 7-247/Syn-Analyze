from flask import Flask, render_template, request
import os
from SynAnalyze import SynAnalyze
from LexAnalyze import LexAnalyze
from SemAnalyze import SemAnalyze

source_path = "./source/source.cc"  # 源文件相对路径
LexGrammar_path = "./LexAnalyze/LexGrammar.txt"  # 词法规则文件相对路径
SynGrammar_path = "./SynAnalyze/new.txt"  # 语法规则文件相对路径
TokenTable_path = "./LexAnalyze/TOKEN-TABLE/token_table.data"  # 存储TOKEN表的相对路径
LRTable_path = "./SynAnalyze/LR-TABLE/LR-Table.csv"  # 存储LR表的相对路径
tree_path = "./templates/render.html"  # 存储语法树的路径
SynAnalyzeProcess_path = "./SynAnalyze/runOnLRTable/runOnLRTable.txt"  # 存储语法分析过程的路径


def Main():
    fp = open(source_path, "r")
    user_input = fp.read()
    fp.close()

    # 词法分析
    lex_ana = LexAnalyze()
    lex_ana.readLexGrammar(LexGrammar_path)
    lex_ana.createNFA()
    lex_ana.createDFA()
    codelist = lex_ana.Pretreatment(user_input)
    Lex_flag, Lex_message = lex_ana.analyze(codelist, TokenTable_path)
    if Lex_flag == False:
        print("词法分析有误")
        print(Lex_message)
        return
    # 语法分析
    sem_ana = SemAnalyze()
    syn_ana = SynAnalyze()
    syn_ana.readSynGrammar(SynGrammar_path)
    syn_ana.getTerminatorsAndNon()
    syn_ana.getFirstSets()
    syn_ana.createLRTable(LRTable_path)
    Syn_flag, Syn_message = syn_ana.analyze(TokenTable_path, tree_path,
                                            SynAnalyzeProcess_path, sem_ana)
    code = sorted(list(sem_ana.map.items()), key=lambda x: x[0])
    for i in code:
        print(i)
    if Syn_flag:
        print("结果已输出至render.html")
    else:
        print(Syn_message)


if __name__ == "__main__":
    Main()
"""


app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        user_input = request.form.get("name")
        user_input = user_input.replace('\r', "")
        fp = open(source_path, 'w')
        fp.write(user_input)
        fp.close()

        # 词法分析
        lex_ana = LexAnalyze()
        lex_ana.readLexGrammar(LexGrammar_path)
        lex_ana.createNFA()
        lex_ana.createDFA()
        codelist = lex_ana.Pretreatment(user_input)
        Lex_flag,Lex_message=lex_ana.analyze(codelist, TokenTable_path)
        if Lex_flag==False:
            return render_template("error.html",message=Lex_message)

        # 语法分析
        sem_ana = SemAnalyze()
        syn_ana = SynAnalyze()
        syn_ana.readSynGrammar(SynGrammar_path)
        syn_ana.getTerminatorsAndNon()
        syn_ana.getFirstSets()
        syn_ana.createLRTable(LRTable_path)
        Syn_flag, Syn_message = syn_ana.analyze(
            TokenTable_path, tree_path, SynAnalyzeProcess_path, sem_ana
        )
        code = sorted(list(sem_ana.map.items()), key=lambda x: x[0])
        message="四元式如图："
        for i in code:
            message+=(str(i)+'\n')
        if Syn_flag:
            print("四元式见上，结果已输出至render.html")
            return render_template('tree.html',message=message)
        else:
            print(Syn_message)
            return render_template('error.html', message=Syn_message)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8888, debug=True)

"""