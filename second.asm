; with thanks to https://stackoverflow.com/a/33401821/1234621
; and the patt/patel textbook
.ORIG x3000
  ld r0, AOEU
  halt

neg:
  add r1, r1, #-1
  ret

STRING  .stringz  "1234\n"
AOEU    .fill xfcef
.END