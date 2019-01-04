; lc3as first.asm
; prints "H" to screen.
.ORIG x3000
  LD R0, INPUT
  OUT
  HALT
  HALT
  HALT
  HALT

INPUT      .FILL  x48 ; H
.END
