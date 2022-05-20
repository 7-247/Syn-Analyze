from flask import Flask, render_template, request
from Main import Main

app = Flask(__name__)

source_path = "./source/source.cc"  # 源文件相对路径
LexGrammar_path = "./LexAnalyze/LexGrammar.txt"  # 词法规则文件相对路径
SynGrammar_path = "./SynAnalyze/new.txt"  # 语法规则文件相对路径
TokenTable_path = "./LexAnalyze/TOKEN-TABLE/token_table.data"  # 存储TOKEN表的相对路径
LRTable_path = "./SynAnalyze/LR-TABLE/LR-Table.pkl"  # 存储LR表的相对路径
tree_path = "./templates/render.html"  # 存储语法树的路径
SynAnalyzeProcess_path = "./SynAnalyze/runOnLRTable/runOnLRTable.txt"  # 存储语法分析过程的路径
target_path = "./TargetMips/target.asm"  #目标代码
object_path = "./SemAnalyze/intermediate_representation.txt"  #中间代码


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        user_input = request.form.get("name")
        user_input = user_input.replace('\r', "")
        fp = open(source_path, 'w')
        fp.write(user_input)
        fp.close()
        Syn_flag, Syn_message, mips_code = Main()
        if Syn_flag:
            return render_template('tree.html', message=mips_code)
        else:
            print(Syn_message)
            return render_template('error.html', message=Syn_message)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8888, debug=True)
