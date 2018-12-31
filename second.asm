; with thanks to https://stackoverflow.com/a/33401821/1234621
; and the patt/patel textbook
.ORIG x3000
  NOT R0, R0
  ; LEA R0, STRING       ; pointer [mem]NUM
  ; PUTs              ; print our string starting from [mem]address in R0
  HALT              ; Trap x25

STRING  .stringz  "1234\n"
.END