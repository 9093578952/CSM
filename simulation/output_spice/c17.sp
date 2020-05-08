* Eda Yan
* USC - SPORT LAB
.option NOMOD
.global vdd
.param vdd=0.7
.include './gate_inventory_gen.sp'


vhi hi 0 vdd
vlo lo 0 0

XNAND2_1  hi  0  N1 N3    N10    NAND2
XNAND2_2  hi  0  N3 N6    N11    NAND2
XNAND2_3  hi  0  N2 N11    N16    NAND2
XNAND2_4  hi  0  N11 N7    N19    NAND2
XNAND2_5  hi  0  N10 N16    N22    NAND2
XNAND2_6  hi  0  N16 N19    N23    NAND2

* extra load at final output
cL1 N22 0 1e-16
cL2 N23 0 1e-16

* input signals
VN1 N1 0 0.7
VN2 N2 0 0.0
VN3 N3 0 0.7
VN6 N6 0 0.0
VN7 N7 0 pulse(0 0.7 5p 1p 1p 50.0p 100.0p)


.tran 10.0f 100.0p
.op
.print v(N22) v(N23) 
.end