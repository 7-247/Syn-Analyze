/*int main() {
    int a = 3, b = 1, c = 1 + 2 * (3 + 4) - 6 / 3;
    a %= b;
    while (a <= !c && b < (a ^ a) || a > (b & c)) {
        c -= a + b * c;
        a = 1;
        if (a > c)
            b = 1;
        else
            c = 1;
    }
}*/
/*
�������ģ���޷������������Զ�ת��Ϊbool������ֱ��дif(a)�ᱨ��(a��һ��int)
�����Ҫ��while��if����дbool���ʽ(E1 nop E2),ͬʱ֧����&&��||����������
*/
int a = 5, b = 3;
int c = 15;
int main() {
    int d = 8, e = 9;
    int cnt = 4;
    int tep;
    while (cnt != 0) {
        if (a > b) {
            tep = a;
            a = b;
            b = tep;
        }
        if (b > c) {
            tep = b;
            b = c;
            c = tep;
        }
        if (c > d) {
            tep = c;
            c = d;
            d = tep;
        }
        if (d > e) {
            tep = d;
            d = e;
            e = tep;
        }
        cnt -= 1;
    }
}