import queue


class Msg:
    def __init__(self, tick, title, text):
        self.tick = str(tick)
        self.title = str(title)
        self.text = str(text)

    def getText(self):
        return "[" + self.tick + "] " + self.title + "\n" + self.text


class IMsgr:
    def __init__(self, q):
        self.q = q

    def addMsg(self, msg):
        self.q.put(msg)


class OMsgr:
    def __init__(self, q):
        self.q = q

    def getMsg(self):
        try:
            return self.q.get(block=False)
        except queue.Empty:
            raise
