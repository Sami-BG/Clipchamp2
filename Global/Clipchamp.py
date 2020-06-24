from Global import ClipchampCmds
from Global.Command import Command
from Global.REPL import REPL


class ClipChamp:

    def __init__(self):
        self.repl = REPL()
        add_log_cmd = Command("add", "Add a new Logging Session", ClipchampCmds.add_new_logging_session)
        view_logging_cmd = Command("view", "View logging sessions", ClipchampCmds.view_logging_sessions)
        remove_logging_cmd = Command("remove", "Remove a channel", ClipchampCmds.remove_logging_session)
        #TODO: Add start_logging_cmd & stop_logging_cmd
        quit_cmd = Command("quit", "Quit", self.repl.quit)

        self.repl.add_to_map(add_log_cmd)
        self.repl.add_to_map(view_logging_cmd)
        self.repl.add_to_map(remove_logging_cmd)
        self.repl.add_to_map(quit_cmd)

    def start_clipchamp(self, home_string):
        self.repl.start_repl(home_string)
