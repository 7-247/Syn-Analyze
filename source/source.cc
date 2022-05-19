int main() {
    int a = 1, b, c = 1 + 2 * (3 + 4) - 6 / 3;
    a %= b;
    while (a <= !c && b > a) {
        c -= a + b * c;
    }
}
/*
int a = 1, b = 3;
int main() {
    while (a > b) a = b;
}*/
