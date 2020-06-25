from typing import List

from Main import ClipchampCmds
from Main.Clipchamp import ClipChamp
from AutoClipper.Logger import ClippingSession


def main():
    clipchamp = ClipChamp()

    list_of_string_of_cmds = [f"|| [{i}] {clipchamp.repl.getPromptFromMap(i)} ||"
                              for i in range(1, clipchamp.repl.number_of_cmds + 1)]

    home_string = ""
    for string_of_cmd in list_of_string_of_cmds:
        home_string += string_of_cmd

    print("Clipchamp 2:")
    clipchamp.start_clipchamp(home_string)


if __name__ == '__main__':
    # File-global variables go here:
    main()
