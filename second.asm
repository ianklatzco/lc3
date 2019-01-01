; lc3as second.asm
.ORIG x3000
  ADD r1, r2, #3
  ADD r1, r2, r3
  AND r1, r2, #3
  AND r1, r2, r3
  BRnzp asdf
  JMP r3
  RET
  jsr asdf
  jsrr r3
  ld r6, foo
  ldi r6, foo
  ldr r4, r2, #-5
  LEA r0, foo
  NOT r1, r2
  ST R4, asdf
  sti r4, asdf
  str r4, r2, #5
  PUTS
asdf:
  HALT

FOO    .FILL x69


.END