# Learning Log for IP Address Emailer
## Bash
In `bash`, functions can only return values `0` through `255`, signalling an exit code.
So we can't do functions as we would in other programming languages.

`echo` never reads from `stdin`, it just prints its arguments, so `cat file | echo` doesn't work.
Use `cat` in this case, i.e. `cat file | cat`.