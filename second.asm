; lc3as second.asm
.ORIG x3000
  LEA r0, MYSTRING
  PUTS
  HALT

FOO    .FILL x0

MYSTRING .STRINGZ "Hello!\n"

.END