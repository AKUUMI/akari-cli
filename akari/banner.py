import sys
from rich.console import Console
from rich.align import Align

from akari import __version__ 


if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')

AKARI_MOE = f"""\
[bold #ffb3ba]✧･ﾟ: *✧･ﾟ:*  ♡ (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧  ♡  *:･ﾟ✧*:･ﾟ✧[/]
[bold #ff99cc]
      █████╗ ██╗  ██╗ █████╗ ██████╗ ██╗
     ██╔══██╗██║ ██╔╝██╔══██╗██╔══██╗██║
     ███████║█████╔╝ ███████║██████╔╝██║
     ██╔══██║██╔═██╗ ██╔══██║██╔══██╗██║
     ██║  ██║██║  ██╗██║  ██║██║  ██║██║
     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝[/]
[bold #ffb3ba]✧･ﾟ: *✧･ﾟ:*  ♡ ૮ ˶ᵔ ᵕ ᵔ˶ ა ♡  *:･ﾟ✧*:･ﾟ✧[/]

       [bold #ff66b2]🌸 ア カ リ 🌸[/]   [italic #ffcce6]Tu rinconcito de anime[/]
               [bold #ffb3ba]v{__version__}[/]
"""

def show_banner(console: Console):
    console.print(Align.center(AKARI_MOE))