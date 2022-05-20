.text
addiu $31,$0,0x10010000
add $3,$0,32
add $4,$0,31
add $5,$0,30
add $6,$0,29
add $7,$0,28
add $8,$0,27
add $9,$0,26
add $10,$0,25
add $11,$0,24
add $12,$0,23
add $13,$0,22
add $14,$0,21
add $15,$0,20
add $16,$0,19
add $17,$0,18
add $18,$0,17
add $19,$0,16
add $20,$0,15
add $21,$0,14
add $22,$0,13
add $23,$0,12
add $24,$0,11
add $25,$0,10
add $26,$0,9
add $27,$0,8
LW $28,0($31)
add $28,$0,7
SW $28,0($31)
LW $28,4($31)
add $28,$0,6
SW $28,4($31)
LW $28,8($31)
add $28,$0,5
SW $28,8($31)
LW $28,12($31)
add $28,$0,4
SW $28,12($31)
LW $28,16($31)
add $28,$0,3
SW $28,16($31)
LW $28,20($31)
add $28,$0,2
SW $28,20($31)
LW $28,24($31)
add $28,$0,1
SW $28,24($31)
LW $28,28($31)
add $28,$0,31
SW $28,28($31)
myjump133:
LW $30,28($31)
bne $30,0,myjump135
j myjump292
myjump135:
beq $3,$4,myjump136
sltu $1,$3,$4
beq $1,$0,myjump137
myjump136:
j myjump140
myjump137:
LW $28,32($31)
add $28,$0,$3
SW $28,32($31)
add $3,$0,$4
LW $30,32($31)
add $4,$0,$30
myjump140:
beq $4,$5,myjump141
sltu $1,$4,$5
beq $1,$0,myjump142
myjump141:
j myjump145
myjump142:
LW $28,32($31)
add $28,$0,$4
SW $28,32($31)
add $4,$0,$5
LW $30,32($31)
add $5,$0,$30
myjump145:
beq $5,$6,myjump146
sltu $1,$5,$6
beq $1,$0,myjump147
myjump146:
j myjump150
myjump147:
LW $28,32($31)
add $28,$0,$5
SW $28,32($31)
add $5,$0,$6
LW $30,32($31)
add $6,$0,$30
myjump150:
beq $6,$7,myjump151
sltu $1,$6,$7
beq $1,$0,myjump152
myjump151:
j myjump155
myjump152:
LW $28,32($31)
add $28,$0,$6
SW $28,32($31)
add $6,$0,$7
LW $30,32($31)
add $7,$0,$30
myjump155:
beq $7,$8,myjump156
sltu $1,$7,$8
beq $1,$0,myjump157
myjump156:
j myjump160
myjump157:
LW $28,32($31)
add $28,$0,$7
SW $28,32($31)
add $7,$0,$8
LW $30,32($31)
add $8,$0,$30
myjump160:
beq $8,$9,myjump161
sltu $1,$8,$9
beq $1,$0,myjump162
myjump161:
j myjump165
myjump162:
LW $28,32($31)
add $28,$0,$8
SW $28,32($31)
add $8,$0,$9
LW $30,32($31)
add $9,$0,$30
myjump165:
beq $9,$10,myjump166
sltu $1,$9,$10
beq $1,$0,myjump167
myjump166:
j myjump170
myjump167:
LW $28,32($31)
add $28,$0,$9
SW $28,32($31)
add $9,$0,$10
LW $30,32($31)
add $10,$0,$30
myjump170:
beq $10,$11,myjump171
sltu $1,$10,$11
beq $1,$0,myjump172
myjump171:
j myjump175
myjump172:
LW $28,32($31)
add $28,$0,$10
SW $28,32($31)
add $10,$0,$11
LW $30,32($31)
add $11,$0,$30
myjump175:
beq $11,$12,myjump176
sltu $1,$11,$12
beq $1,$0,myjump177
myjump176:
j myjump180
myjump177:
LW $28,32($31)
add $28,$0,$11
SW $28,32($31)
add $11,$0,$12
LW $30,32($31)
add $12,$0,$30
myjump180:
beq $12,$13,myjump181
sltu $1,$12,$13
beq $1,$0,myjump182
myjump181:
j myjump185
myjump182:
LW $28,32($31)
add $28,$0,$12
SW $28,32($31)
add $12,$0,$13
LW $30,32($31)
add $13,$0,$30
myjump185:
beq $13,$14,myjump186
sltu $1,$13,$14
beq $1,$0,myjump187
myjump186:
j myjump190
myjump187:
LW $28,32($31)
add $28,$0,$13
SW $28,32($31)
add $13,$0,$14
LW $30,32($31)
add $14,$0,$30
myjump190:
beq $14,$15,myjump191
sltu $1,$14,$15
beq $1,$0,myjump192
myjump191:
j myjump195
myjump192:
LW $28,32($31)
add $28,$0,$14
SW $28,32($31)
add $14,$0,$15
LW $30,32($31)
add $15,$0,$30
myjump195:
beq $15,$16,myjump196
sltu $1,$15,$16
beq $1,$0,myjump197
myjump196:
j myjump200
myjump197:
LW $28,32($31)
add $28,$0,$15
SW $28,32($31)
add $15,$0,$16
LW $30,32($31)
add $16,$0,$30
myjump200:
beq $16,$17,myjump201
sltu $1,$16,$17
beq $1,$0,myjump202
myjump201:
j myjump205
myjump202:
LW $28,32($31)
add $28,$0,$16
SW $28,32($31)
add $16,$0,$17
LW $30,32($31)
add $17,$0,$30
myjump205:
beq $17,$18,myjump206
sltu $1,$17,$18
beq $1,$0,myjump207
myjump206:
j myjump210
myjump207:
LW $28,32($31)
add $28,$0,$17
SW $28,32($31)
add $17,$0,$18
LW $30,32($31)
add $18,$0,$30
myjump210:
beq $18,$19,myjump211
sltu $1,$18,$19
beq $1,$0,myjump212
myjump211:
j myjump215
myjump212:
LW $28,32($31)
add $28,$0,$18
SW $28,32($31)
add $18,$0,$19
LW $30,32($31)
add $19,$0,$30
myjump215:
beq $19,$20,myjump216
sltu $1,$19,$20
beq $1,$0,myjump217
myjump216:
j myjump220
myjump217:
LW $28,32($31)
add $28,$0,$19
SW $28,32($31)
add $19,$0,$20
LW $30,32($31)
add $20,$0,$30
myjump220:
beq $20,$21,myjump221
sltu $1,$20,$21
beq $1,$0,myjump222
myjump221:
j myjump225
myjump222:
LW $28,32($31)
add $28,$0,$20
SW $28,32($31)
add $20,$0,$21
LW $30,32($31)
add $21,$0,$30
myjump225:
beq $21,$22,myjump226
sltu $1,$21,$22
beq $1,$0,myjump227
myjump226:
j myjump230
myjump227:
LW $28,32($31)
add $28,$0,$21
SW $28,32($31)
add $21,$0,$22
LW $30,32($31)
add $22,$0,$30
myjump230:
beq $22,$23,myjump231
sltu $1,$22,$23
beq $1,$0,myjump232
myjump231:
j myjump235
myjump232:
LW $28,32($31)
add $28,$0,$22
SW $28,32($31)
add $22,$0,$23
LW $30,32($31)
add $23,$0,$30
myjump235:
beq $23,$24,myjump236
sltu $1,$23,$24
beq $1,$0,myjump237
myjump236:
j myjump240
myjump237:
LW $28,32($31)
add $28,$0,$23
SW $28,32($31)
add $23,$0,$24
LW $30,32($31)
add $24,$0,$30
myjump240:
beq $24,$25,myjump241
sltu $1,$24,$25
beq $1,$0,myjump242
myjump241:
j myjump245
myjump242:
LW $28,32($31)
add $28,$0,$24
SW $28,32($31)
add $24,$0,$25
LW $30,32($31)
add $25,$0,$30
myjump245:
beq $25,$26,myjump246
sltu $1,$25,$26
beq $1,$0,myjump247
myjump246:
j myjump250
myjump247:
LW $28,32($31)
add $28,$0,$25
SW $28,32($31)
add $25,$0,$26
LW $30,32($31)
add $26,$0,$30
myjump250:
beq $26,$27,myjump251
sltu $1,$26,$27
beq $1,$0,myjump252
myjump251:
j myjump255
myjump252:
LW $28,32($31)
add $28,$0,$26
SW $28,32($31)
add $26,$0,$27
LW $30,32($31)
add $27,$0,$30
myjump255:
LW $29,0($31)
beq $27,$29,myjump256
sltu $1,$27,$29
beq $1,$0,myjump257
myjump256:
j myjump260
myjump257:
LW $28,32($31)
add $28,$0,$27
SW $28,32($31)
LW $30,0($31)
add $27,$0,$30
LW $30,32($31)
LW $28,0($31)
add $28,$0,$30
SW $28,0($31)
myjump260:
LW $30,0($31)
LW $29,4($31)
beq $30,$29,myjump261
sltu $1,$30,$29
beq $1,$0,myjump262
myjump261:
j myjump265
myjump262:
LW $30,0($31)
LW $28,32($31)
add $28,$0,$30
SW $28,32($31)
LW $30,4($31)
LW $28,0($31)
add $28,$0,$30
SW $28,0($31)
LW $30,32($31)
LW $28,4($31)
add $28,$0,$30
SW $28,4($31)
myjump265:
LW $30,4($31)
LW $29,8($31)
beq $30,$29,myjump266
sltu $1,$30,$29
beq $1,$0,myjump267
myjump266:
j myjump270
myjump267:
LW $30,4($31)
LW $28,32($31)
add $28,$0,$30
SW $28,32($31)
LW $30,8($31)
LW $28,4($31)
add $28,$0,$30
SW $28,4($31)
LW $30,32($31)
LW $28,8($31)
add $28,$0,$30
SW $28,8($31)
myjump270:
LW $30,8($31)
LW $29,12($31)
beq $30,$29,myjump271
sltu $1,$30,$29
beq $1,$0,myjump272
myjump271:
j myjump275
myjump272:
LW $30,8($31)
LW $28,32($31)
add $28,$0,$30
SW $28,32($31)
LW $30,12($31)
LW $28,8($31)
add $28,$0,$30
SW $28,8($31)
LW $30,32($31)
LW $28,12($31)
add $28,$0,$30
SW $28,12($31)
myjump275:
LW $30,12($31)
LW $29,16($31)
beq $30,$29,myjump276
sltu $1,$30,$29
beq $1,$0,myjump277
myjump276:
j myjump280
myjump277:
LW $30,12($31)
LW $28,32($31)
add $28,$0,$30
SW $28,32($31)
LW $30,16($31)
LW $28,12($31)
add $28,$0,$30
SW $28,12($31)
LW $30,32($31)
LW $28,16($31)
add $28,$0,$30
SW $28,16($31)
myjump280:
LW $30,16($31)
LW $29,20($31)
beq $30,$29,myjump281
sltu $1,$30,$29
beq $1,$0,myjump282
myjump281:
j myjump285
myjump282:
LW $30,16($31)
LW $28,32($31)
add $28,$0,$30
SW $28,32($31)
LW $30,20($31)
LW $28,16($31)
add $28,$0,$30
SW $28,16($31)
LW $30,32($31)
LW $28,20($31)
add $28,$0,$30
SW $28,20($31)
myjump285:
LW $30,20($31)
LW $29,24($31)
beq $30,$29,myjump286
sltu $1,$30,$29
beq $1,$0,myjump287
myjump286:
j myjump290
myjump287:
LW $30,20($31)
LW $28,32($31)
add $28,$0,$30
SW $28,32($31)
LW $30,24($31)
LW $28,20($31)
add $28,$0,$30
SW $28,20($31)
LW $30,32($31)
LW $28,24($31)
add $28,$0,$30
SW $28,24($31)
myjump290:
LW $30,28($31)
LW $28,28($31)
sub $28,$30,1
SW $28,28($31)
j myjump133
myjump292:

