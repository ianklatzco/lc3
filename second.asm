; lc3as second.asm
.ORIG x3000
  ADD r1, r2, #3
  ADD r1, r2, r3
  AND r1, r2, #3
  AND r1, r2, r3
  LEA r0, MYSTRING
  PUTS
  HALT

FOO    .FILL x0

MYSTRING .STRINGZ "Hello!\n"

.END