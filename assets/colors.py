class bcolor:
    black="\u001b[30m"
    red="\u001b[31m"
    green="\u001b[32m"
    yellow="\u001b[33m"
    blue="\u001b[34m"
    magenta="\u001b[35m"
    cyan="\u001b[36m"
    white="\u001b[37m"
    reset="\u001b[0m"
    bblack="\u001b[30;1m"
    bred="\u001b[31;1m"
    bgreen="\u001b[32;1m"
    byellow="\u001b[33;1m"
    bblue="\u001b[34;1m"
    bmagenta="\u001b[35;1m"
    bcyan="\u001b[36;1m"
    bold="\u001b[1m"
    underline="\u001b[4m"
    blink="\u001b[5m"
    reverse="\u001b[7m"
    invisible="\u001b[8m"

    def colorize(self, text, color):
        return color + text + self.reset