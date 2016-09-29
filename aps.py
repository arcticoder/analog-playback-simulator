import sys, getopt
from subprocess import call
from subprocess import Popen,PIPE


def main(argv):
    opts, args = getopt.getopt(argv,"hi:",["infile="])
    for opt, arg in opts:
        if opt == '-h':
            print('aps.py -i <infile>')
            sys.exit()
        elif opt in ("-i", "--infile"):
            infile = arg
    state = 'unloaded_stopped'
    print('Current state: ' + state)
    while True:
        command = input('Enter new state (unloaded_stopped,loaded_stopped,loaded_started,exit):')
        if (command in ['unloaded_stopped','loaded_stopped','loaded_started']):
            state = command
        elif command == 'exit':
            proc.kill()
            sys.exit()
        print('Current state: ' + state)
        if state == 'loaded_started':
            proc = Popen("mplayer -quiet \"" + infile + "\"", stdout=PIPE, stderr=PIPE)
        if (state in ['loaded_stopped','unloaded_stopped'] and proc):
            proc.kill()

if __name__ == "__main__":
    main(sys.argv[1:])
