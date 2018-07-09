import click
from classes import BGPDataAggregator


@click.command()
def backend():
    aggregator = BGPDataAggregator()


@click.command()
def interface():
    last_scene = None
    while True:
        try:
            Screen.wrapper(display, catch_interrupt=False,
                           arguments=[last_scene])
            sys.exit(0)
        except ResizeScreenError as e:
            last_scene = e.scene


if __name__ == '__main__':
    backend()
