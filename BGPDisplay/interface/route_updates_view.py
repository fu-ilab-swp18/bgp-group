from asciimatics.widgets import Layout

from .column_view import BGPColumnView

class BGPRouteUpdatesView(BGPColumnView):
  def __init__(self, screen, row, column, max_row, max_column):
    super(BGPRouteUpdatesView, self).__init__(screen, row, column, max_row, max_column, title="BGP Route Updates")

    layout = Layout([1, 1])
    self.add_layout(layout)

    self.fix()
