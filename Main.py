from SynAnalyze import SynAnalyze
from LexAnalyze import LexAnalyze

source_path='./source/source.cc'                            #源文件相对路径
LexGrammar_path='./LexAnalyze/LexGrammar.txt'               #词法规则文件相对路径
SynGrammar_path='./SynAnalyze/SynGrammar.txt'               #语法规则文件相对路径
TokenTable_path='./LexAnalyze/TOKEN-TABLE/token_table.data' #存储TOKEN表的相对路径
LRTable_path='./SynAnalyze/LR-TABLE/LR-Table.csv'           #存储LR表的相对路径

#词法分析
lex_ana = LexAnalyze()
lex_ana.readLexGrammar(LexGrammar_path)
lex_ana.createNFA()
lex_ana.createDFA()
lex_ana.analyze(source_path,TokenTable_path)

#语法分析
syn_ana = SynAnalyze()
syn_ana.readSynGrammar(SynGrammar_path)
syn_ana.getTerminatorsAndNon()
syn_ana.getFirstSets()
syn_ana.createLRTable(LRTable_path)
tree = syn_ana.analyze(TokenTable_path)