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

  LEA r0, MYSTRING
  PUTS
asdf:
  HALT

FOO    .FILL x0

MYSTRING .STRINGZ "Hello!\n"

.END