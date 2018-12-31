; with thanks to https://stackoverflow.com/a/33401821/1234621
; and the patt/patel textbook
.ORIG x3000
  ldi r0, INDIR
  halt

neg:
  add r1, r1, #-1
  ret

STRING  .stringz  "1234\n"
INDIR   .fill AOEU
AOEU    .fill xfcef
.END