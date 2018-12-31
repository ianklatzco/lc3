; with thanks to https://stackoverflow.com/a/33401821/1234621
; and the patt/patel textbook
.ORIG x3000
  add r1, r1, #-1
  ld  r0, h
  out
  halt

STRING  .stringz  "1234\n"
INDIR   .fill AOEU
AOEU    .fill xfcef
h       .fill x68
.END