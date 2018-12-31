; with thanks to https://stackoverflow.com/a/33401821/1234621
; and the patt/patel textbook
.ORIG x3000
  add r0, r0, #0

  BRn NEG
  HALT

NEG:
  add r1, r1, #-1
  HALT              ; Trap x25

STRING  .stringz  "1234\n"
.END