; with thanks to https://stackoverflow.com/a/33401821/1234621
; and the patt/patel textbook
.ORIG x3000
  ADD R0, R0, #-1 ; 0xffff
  AND R0, R0, #3 ;  0x0003 0b011
  AND R0, R0, #2  ; 0x0002 0b010
  AND R1, R2, R0
  ; LEA R0, STRING       ; pointer [mem]NUM
  ; PUTs              ; print our string starting from [mem]address in R0
  HALT              ; Trap x25

STRING  .stringz  "1234\n"
.END