from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError

from interface import BGPInfoView, BGPRouteUpdatesView, BGPRouteValidationsView, BGPStatisticsView


def display(screen, scene):
    rows = 2
    columns = 2

    route_updates = BGPRouteUpdatesView(screen, 0, 0, rows, columns)
    info = BGPInfoView(screen, 0, 1, rows, columns)
    route_validations = BGPRouteValidationsView(screen, 1, 0, rows, columns)
    statistics = BGPStatisticsView(screen, 1, 1, rows, columns)

    scenes = [Scene([route_updates, info, route_validations, statistics], -1)]
    screen.play(scenes, stop_on_resize=True, start_scene=scene)


if __name__ == '__main__':
    last_scene = None
    while True:
        try:
            Screen.wrapper(display, catch_interrupt=False,
                           arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene
