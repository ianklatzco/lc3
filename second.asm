; with thanks to https://stackoverflow.com/a/33401821/1234621
; and the patt/patel textbook
.ORIG x3000
  lea r0, neg
  jsr neg
  HALT
  and r0, r0, #0
  and r0, r0, #0
  and r0, r0, #0
  and r0, r0, #0
  and r0, r0, #0
  and r0, r0, #0

neg:
  add r1, r1, #-1
  ret

STRING  .stringz  "1234\n"
.END