from textwrap import dedent


class MockFile(object):
    def __init__(self, data):
        self.data = dedent(data)
        self.lines = self.data.splitlines(True)
        self.curr_line = 0

    def readline(self):
        if self.curr_line < len(self.lines):
            self.curr_line += 1
            return self.lines[self.curr_line-1]
        else:
            return ''
