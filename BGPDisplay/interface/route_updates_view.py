from asciimatics.renderers import BarChart
from asciimatics.effects import Print
from asciimatics.screen import Screen

from .column_view import BGPColumnView

class BGPRouteUpdatesView(BGPColumnView):
  def __init__(self, screen, row, column, max_row, max_column):
    super(BGPRouteUpdatesView, self).__init__(screen, row, column, max_row, max_column, title="BGP Route Updates")

    chart = Print(screen,
                  BarChart(
                      10, 20,
                      [self._wv(1), self._wv(2)],
                      colour=Screen.COLOUR_WHITE,
                      axes=BarChart.X_AXIS,
                      scale=2.0),
                  x=0, y=0, transparent=False, speed=2)

    # self.add_effect(chart)


  def _wv(self, x):
    return lambda: x + 1
