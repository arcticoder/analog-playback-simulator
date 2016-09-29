import sys, getopt
from subprocess import call


def main(argv):
    opts, args = getopt.getopt(argv,"hi:",["infile="])
    for opt, arg in opts:
        if opt == '-h':
            print('aps.py -i <infile>')
            sys.exit()
        elif opt in ("-i", "--infile"):
            infile = arg
    print('Current state: loaded_stopped')
    while True:
        command = input('Enter new state (loaded_started,exit):')
        if command == 'loaded_started':
            call("mplayer -quiet \"" + infile + "\"", shell=True)
        elif command == 'exit':
            sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])
