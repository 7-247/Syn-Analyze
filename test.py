"""
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
"""
CPP_32 = "int cnt=31,tep;\nint main(){\n"
tmp = 1
for i in range(32):
    CPP_32 += f"int sort_test{tmp+i}={32-i};\n"
CPP_32 += "while(cnt!=0){\n"
for i in range(1, 32):
    tep_state = f"tep=sort_test{i};\nsort_test{i}=sort_test{i+1};\nsort_test{i+1}=tep;\n"
    CPP_32 += f"if(sort_test{i}>sort_test{i+1}) {'{'}{tep_state}{'}'}"

CPP_32 += "cnt -= 1;\n}\n}\n"
print(CPP_32)
with open("temp.cc", "w") as fp:
    fp.write(CPP_32)