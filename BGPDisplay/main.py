import click
from classes import BGPDataAggregator


@click.command()
def backend():
    aggregator = BGPDataAggregator()


if __name__ == '__main__':
    backend()
