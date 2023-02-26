from subprocess import call
# call(["amixer", "-D", "pulse", "sset", "Master", "10%+"])
call(["amixer", "-D", "pulse", "sset", "Master", "0%"])
