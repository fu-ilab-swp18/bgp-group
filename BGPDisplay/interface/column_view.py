from asciimatics.widgets import Frame

class BGPColumnView(Frame):
  def __init__(self, screen, row, column, max_row, max_column, title):
    width = screen.width // max_column
    height = screen.height // max_row

    super(BGPColumnView, self).__init__(screen,
                                   height,
                                   width,
                                   x=width * column,
                                   y=height * row,
                                   title=title,
                                   has_border=True)
