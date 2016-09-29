import sys, getopt
from subprocess import call
from subprocess import Popen,DEVNULL,PIPE


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
        command = input('Enter new state (unloaded_stopped,loaded_stopped,loaded_started,loaded_paused,exit):')
        if (command in ['unloaded_stopped','loaded_stopped','loaded_started','loaded_paused']):
            state = command
        elif command == 'exit':
            proc.kill()
            sys.exit()
        print('Current state: ' + state)
        if state == 'loaded_started':
            cmd = ['mplayer', '-slave', '-quiet', infile]
            proc = Popen(cmd, stdout=DEVNULL, stderr=DEVNULL, stdin=PIPE, universal_newlines=True, bufsize=1)
        elif (state in ['loaded_stopped','unloaded_stopped'] and proc):
            proc.kill()
        elif (state == 'loaded_paused' and proc):
            print('pause', flush=True, file=proc.stdin)


if __name__ == "__main__":
    main(sys.argv[1:])
