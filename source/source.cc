int main() {
    int a = 3, b = 1, c = 1 + 2 * (3 + 4) - 6 / 3;
    a %= b;
    while (a <= !c && b < (a ^ a) || a > (b & c)) {
        c -= a + b * c;
        a = 1;
        if (a > ~c)
            if (a > c)
                b = 1;
            else
                c = 1;
    }
}
/*
�޷������������Զ�ת��Ϊbool
�����Ҫ��while if����дbool���ʽ�����ǵ��߼��롢�򡢷�
*/