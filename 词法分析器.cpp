#include <fstream>
#include <iostream>
#include <map>
#include <regex>
using namespace std;

void err(string s) {
    cout << "\nERROR: " << s << endl;
    exit(0);
}

int cnt;  // ��ǰ�ս����ŵ����
map<string, int> word;
string wordList[] = {"!=", "(",   ")",      "*",    "+",     ",", "-",  "/",
                     ";",  "<",   "<=",     "=",    "==",    ">", ">=", "else",
                     "if", "int", "return", "void", "while", "{", "}"};

void init() {
    cnt = 70;
    for (auto i : wordList) word[i] = ++cnt;
}

ofstream program("intermediate\\processed_sourceCode.txt");
ofstream iden("intermediate\\names.txt");
// string newProgram = "";

//���ұ�����
int searchReserve(string s) {
    auto iter = word.find(s);
    return (iter != word.end())
               ? iter->second
               : -1;  //���ɹ����ң��򷵻��ֱ��룻���򷵻�100��������Ҳ��ɹ�����Ϊ��ʶ��
}

// �����ӳ����㷨����
// ���룺�������ַ����͵�ǰָ��
// �������ǰ������ַ�Ⱥtoken�Լ������ڵ�����syn
void Scanner(string resProgram, int &pointer) {
    int syn = 0;
    string token = "";
    char ch;  //��Ϊ�ж�ʹ��
    ch = resProgram[pointer];
    while (ch == ' ')
        ch = resProgram[++pointer];  //���˿ո񣬷�ֹ������ʶ���˿ո������
    if (isalpha(resProgram[pointer]) || isdigit(resProgram[pointer])) {
        if (isalpha(resProgram[pointer])) {  //��ͷΪ��ĸ�������ĸ������
            while (isalpha(resProgram[pointer]) || isdigit(resProgram[pointer]))
                token += resProgram[pointer++];  //�ռ���Ȼ������
            syn = searchReserve(
                token);  // ������Ǳ����ֻ��ѳ��ֹ����ս���������ֱ��룻
            if (syn == -1) {
                iden << token << endl;
                token = "identifier";
            }
            // ���ޣ�˵���Ǳ�ʶ����
        } else {
            while (isdigit(resProgram[pointer]))
                token += resProgram[pointer++];  //��ͷΪ���֣�������֡�
            syn = searchReserve(token);
            if (syn == -1) {
                iden << token << endl;
                token = "number";
            }
        }

        // word[token] = syn = ++cnt;  // ���򣬼����ս����
    } else {  // ��ͷΪ�����ַ�
        token = resProgram[pointer];
        token += resProgram[pointer + 1];
        if ((syn = searchReserve(token)) != -1) {  // != <= == >=
            pointer += 2;
        } else {
            token = resProgram[pointer];
            if ((syn = searchReserve(token)) != -1) {  // ( ) * + , - / ; < >
                pointer += 1;
            } else
                err("unknown character " + to_string(int(token[0])) + " " +
                    token);
        }
    }
    program << token << endl;
    // newProgram += char(syn);
}

//����Ԥ����ȡ�����õ��ַ���ע��
string filterResource(string r) {
    r = regex_replace(r, regex("(\\s){2,}"), " ");  // ɾ������ո�

    // ��Ȼע��Ҳ����ͨ������ȥ�������ǻ����ֶ�д�ˡ�
    string filStr = "";
    for (int i = 0; i <= r.length(); i++) {
        if (r[i] == '/' && r[i + 1] == '/')  // ����ע��ȥ��[ע�ͷ�//, �س�����]
            while (r[i] != '\n') i++;
        if (r[i] == '/' && r[i + 1] == '*') {  // ����ע��ȥ��[/* , */]
            i += 2;
            while (i + 1 < r.length() && (r[i] != '*' || r[i + 1] != '/')) ++i;
            if (i + 1 >= r.length()) err("û���ҵ� */");
            i += 2;
        }
        filStr += r[i];
    }

    filStr = regex_replace(filStr, regex("[\n\t\v\r]"), "");  // ���������ַ�

    return filStr;
}

int main() {
    // �������
    ifstream t("input\\Դ����.txt");
    string str((std::istreambuf_iterator<char>(t)),
               std::istreambuf_iterator<char>());

    //��Դ������й���
    string resProgram = filterResource(str);

    init();           // ���ر����ֱ�����������
    int pointer = 0;  // Դ����ָ��
    while (pointer < resProgram.length()) {
        Scanner(resProgram, pointer);
        if (!resProgram[pointer]) break;
    }

    for (auto i : word) {
        printf("%03d  ", i.second);
        cout << i.first << endl;
    }
    return 0;
}