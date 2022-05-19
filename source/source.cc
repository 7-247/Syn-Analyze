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
语义分析模块无法将其它类型自动转化为bool，例如直接写if(a)会报错(a是一个int)
因此需要在while或if里面写bool表达式(E1 nop E2),同时支持用&&或||将它们连接
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