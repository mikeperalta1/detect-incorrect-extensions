

from domain.Detector import Detector


import argparse


def main():
	
	parser = argparse.ArgumentParser(prog="Mike's incorrect extension detector (woot)")
	
	parser.add_argument(
		"--source", "--dir",
		required=True,
		dest="source",
		help="Specify a directory to search through"
	)
	parser.add_argument(
		"--recurse-source", "--source-recursive",
		dest="source_recurse",
		default=True,
		action="store_true"
	)
	parser.add_argument(
		"--no-recurse-source", "--no-source-recursive",
		dest="source_recurse",
		required=False,
		action="store_false"
	)
	
	args = parser.parse_args()
	
	detector = Detector(
		source=args.source,
		source_recurse=args.source_recurse
	)
	detector.run()


if __name__ == "__main__":
	main()
