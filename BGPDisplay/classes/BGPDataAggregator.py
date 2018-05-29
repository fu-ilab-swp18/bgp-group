from datetime import datetime

from _pybgpstream import BGPStream, BGPRecord, BGPElem
from rtrlib import RTRManager, register_pfx_update_callback, register_spki_update_callback

from helper.db_connector import SQLiteConnector as DBConnector

if __name__ == '__main__':
	import click

	@click.command()
	def main():
		click.echo("Test")
		# data_aggregator = BGPDataAggregator()

	main()

