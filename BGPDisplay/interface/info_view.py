from asciimatics.widgets import Layout, Label

from .column_view import BGPColumnView

class BGPInfoView(BGPColumnView):
  def __init__(self, screen, row, column, max_row, max_column):
    super(BGPInfoView, self).__init__(screen, row, column, max_row, max_column, title="Informationen")

    layout = Layout([1], fill_frame=True)
    self.add_layout(layout)

    layout.add_widget(Label("Hier werden die Informationstafeln durchlaufen."), 0)
    self.fix()
