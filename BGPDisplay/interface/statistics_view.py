from asciimatics.widgets import Layout, Label

from .column_view import BGPColumnView

class BGPStatisticsView(BGPColumnView):
  def __init__(self, screen, row, column, max_row, max_column):
    super(BGPStatisticsView, self).__init__(screen, row, column, max_row, max_column, title="Statistik")

    layout = Layout([1, 1])
    self.add_layout(layout)

    layout.add_widget(Label("Gesehene Routen:"), 0)
    layout.add_widget(Label("1.234"), 1)

    layout.add_widget(Label("Updates pro Minute:"), 0)
    layout.add_widget(Label("431"), 1)

    self.fix()
