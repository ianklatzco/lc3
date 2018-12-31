; with thanks to https://stackoverflow.com/a/33401821/1234621
; and the patt/patel textbook
.ORIG x3000
  LEA R0, NUM       ; pointer [mem]NUM
  PUTs              ; print our string starting from [mem]address in R0
  HALT              ; Trap x25

NUM   .fill  x31    ; Our Number to print
      .fill  x32     
      .fill  x33
      .fill  x34
      .fill  x0a
.END