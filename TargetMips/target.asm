.text
add $2,$0,5
add $3,$0,3
add $4,$0,15
add $5,$0,8
add $6,$0,9
add $7,$0,4
myjump106:
bne $7,0,myjump108
j myjump130
myjump108:
beq $2,$3,myjump109
sltu $1,$2,$3
beq $1,$0,myjump110
myjump109:
j myjump113
myjump110:
add $8,$0,$2
add $2,$0,$3
add $3,$0,$8
myjump113:
beq $3,$4,myjump114
sltu $1,$3,$4
beq $1,$0,myjump115
myjump114:
j myjump118
myjump115:
add $8,$0,$3
add $3,$0,$4
add $4,$0,$8
myjump118:
beq $4,$5,myjump119
sltu $1,$4,$5
beq $1,$0,myjump120
myjump119:
j myjump123
myjump120:
add $8,$0,$4
add $4,$0,$5
add $5,$0,$8
myjump123:
beq $5,$6,myjump124
sltu $1,$5,$6
beq $1,$0,myjump125
myjump124:
j myjump128
myjump125:
add $8,$0,$5
add $5,$0,$6
add $6,$0,$8
myjump128:
sub $7,$7,1
j myjump106
myjump130:

