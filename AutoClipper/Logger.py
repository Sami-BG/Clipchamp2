from Twitch import TwitchAPI as ttv


class ClippingSession:

    def __init__(self, channel_name):
        self.channel_name: str = channel_name
        self.user_id: str= ttv.get_user_id(channel_name)
        self.is_visited: bool = False
        self.log_file_string: str = ""

    # TODO: Make sure that concurrent process works, and that you can cancel this from another thread.
    def start_logging_until_stopped(self):
        # https://www.learndatasci.com/tutorials/how-stream-text-data-twitch-sockets-python/
        pass
