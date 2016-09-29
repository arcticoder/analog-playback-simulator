import sys, getopt
from subprocess import call

def main(argv):	
	opts, args = getopt.getopt(argv,"hi:",["ifile="])
	for opt, arg in opts:
		if opt == '-h':
			print('aps.py -i <inputfile>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputfile = arg	
	call("mplayer -quiet \"" + inputfile + "\"", shell=True)	
	
if __name__ == "__main__":
   main(sys.argv[1:])