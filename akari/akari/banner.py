from rich.text import Text
from rich.align import Align
from akari import __version__

AKARI_ASCII = """\
      ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
     █████╗ ██╗  ██╗ █████╗ ██████╗ ██╗
    ██╔══██╗██║ ██╔╝██╔══██╗██╔══██╗██║
    ███████║█████╔╝ ███████║██████╔╝██║
    ██╔══██║██╔═██╗ ██╔══██║██╔══██╗██║
    ██║  ██║██║  ██╗██║  ██║██║  ██║██║
    ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝
    ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
          ✧  ア カ リ  ✧   tu cliente de anime 🕊️
"""

def show_banner(console):
    lines = AKARI_ASCII.split("\n")
    styled = Text()
    for line in lines:
        if "✦" in line or "˚" in line:
            styled.append(line + "\n", style="bold color(183)")
        elif "░" in line:
            styled.append(line + "\n", style="color(225)")
        elif any(c in line for c in "█╗╝║╔╚"):
            styled.append(line + "\n", style="bold color(255)")
        elif "ア カ リ" in line or "✧" in line:
            styled.append(line + "\n", style="bold color(220)")
        elif "🕊️" in line:
            styled.append(line + "\n", style="italic color(219)")
        else:
            styled.append(line + "\n", style="color(255)")

    version_line = Text(f"          v{__version__}\n", style="color(183)")
    sep_line = Text("      ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦ · . ˚ ✦\n", style="bold color(183)")
    styled.append_text(version_line)
    styled.append_text(sep_line)

    console.print(Align.center(styled))
