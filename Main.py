from SynAnalyze import SynAnalyze
from LexAnalyze import LexAnalyze

source_path = './source/source.cc'  # 源文件相对路径
LexGrammar_path = './LexAnalyze/LexGrammar.txt'  # 词法规则文件相对路径
SynGrammar_path = './SynAnalyze/SynGrammar.txt'  # 语法规则文件相对路径
TokenTable_path = './LexAnalyze/TOKEN-TABLE/token_table.data'  # 存储TOKEN表的相对路径
LRTable_path = './SynAnalyze/LR-TABLE/LR-Table.csv'  # 存储LR表的相对路径
tree_path="./templates/render.html"#存储语法树的路径
SynAnalyzeProcess_path="./SynAnalyze/runOnLRTable/runOnLRTable.txt"#存储语法分析过程的路径


from flask import Flask,render_template,request
import os
app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])    
def index():
    if request.method == 'POST':
        user_input = request.form.get("name")
        print(user_input)
        fp=open(source_path,'w')
        fp.write(user_input)
        fp.close()

        # 词法分析
        lex_ana = LexAnalyze()
        lex_ana.readLexGrammar(LexGrammar_path)
        lex_ana.createNFA()
        lex_ana.createDFA()
        lex_ana.analyze(source_path, TokenTable_path)

        # 语法分析
        syn_ana = SynAnalyze()
        syn_ana.readSynGrammar(SynGrammar_path)
        syn_ana.getTerminatorsAndNon()
        syn_ana.getFirstSets()
        syn_ana.createLRTable(LRTable_path)
        Syn_flag,Syn_message=syn_ana.analyze(TokenTable_path,tree_path,SynAnalyzeProcess_path)
        if Syn_flag:
            return render_template('tree.html')
        else:
            print(Syn_message)
            return render_template('error.html',message=Syn_message)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8888, debug=True)

