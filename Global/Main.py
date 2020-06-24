from typing import List

from Global.Clipchamp import ClipChamp

from Global import ClipchampCmds
from AutoClipper.Logger import LoggingSession


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
    sessions: List[LoggingSession] = ClipchampCmds.list_of_logging_sessions
    main()
