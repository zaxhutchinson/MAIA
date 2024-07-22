import queue


class Msg:
    def __init__(self, turn, title, text):
        """Initializes turn, title, and text with associated parameters"""
        self.turn = str(turn)
        self.title = str(title)
        self.text = str(text)

    def get_text(self):
        """Gets text"""
        return "[" + self.turn + "] " + self.title + "\n" + self.text


class IMsgr:
    def __init__(self, q):
        """Initializes q with associated parameter"""
        self.q = q

    def add_msg(self, msg):
        """Adds message"""
        self.q.put(msg)


class OMsgr:
    def __init__(self, q):
        """Initializes q with associated parameter"""
        self.q = q

    def get_msg(self):
        """Gets message"""
        try:
            return self.q.get(block=False)
        except queue.Empty:
            raise
