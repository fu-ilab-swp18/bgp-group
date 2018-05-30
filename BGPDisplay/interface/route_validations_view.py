from asciimatics.widgets import Layout

from .column_view import BGPColumnView


class BGPRouteValidationsView(BGPColumnView):
    def __init__(self, screen, row, column, max_row, max_column):
        super(BGPRouteValidationsView, self).__init__(screen, row,
                                                      column, max_row, max_column, title="RPKI-validierte Routen")

        layout = Layout([1, 1])
        self.add_layout(layout)

        self.fix()
