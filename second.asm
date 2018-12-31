; with thanks to https://stackoverflow.com/a/33401821/1234621
; and the patt/patel textbook
.ORIG x3000
  lea r0, neg
  jmp r0
  HALT

NEG:
  add r1, r1, #-1
  HALT              ; Trap x25

STRING  .stringz  "1234\n"
.END