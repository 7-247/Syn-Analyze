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
无法将其它类型自动转化为bool
因此需要在while if里面写bool表达式和他们的逻辑与、或、非
*/