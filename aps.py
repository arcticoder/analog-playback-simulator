import sys, getopt, wave, pyaudio
from subprocess import call, Popen, DEVNULL, PIPE


def main(argv):
    """
    Analog Playback Simulator (APS)
    Simulate navigating machine states as it plays back media.

    :param argv:
    :return:
    """
    stateGraph = {
        'unloaded_stopped': ['loaded_stopped'],
        'loaded_stopped': ['loaded_started','unloaded_stopped'],
        'loaded_started': ['loaded_paused', 'loaded_stopped'],
        'loaded_paused': ['loaded_started', 'loaded_stopped']
    }
    opts, args = getopt.getopt(argv, "hi:", ["infile="])
    proc = None
    for opt, arg in opts:
        if opt == '-h':
            print('aps.py -i <infile>')
            sys.exit()
        elif opt in ("-i", "--infile"):
            infile = arg
    pyAudio = pyaudio.PyAudio()
    wavChunkSize = 1024

    state = 'unloaded_stopped'
    print('Current state: ' + state)
    while True:
        command = input('Enter new state (' + ','.join(stateGraph[state]) + ') or exit):')
        if (command == ''):
            command = stateGraph[state][0]
        if (command in stateGraph[state]):
            if (state == 'unloaded_stopped' and command == 'loaded_stopped'):
                #transition sound effect, this will end up in a json file soon
                loadingSound = wave.open("sound effects\load record short.wav", "rb")
                audioStream = pyAudio.open(format=pyAudio.get_format_from_width(loadingSound.getsampwidth()),
                                    channels=loadingSound.getnchannels(),
                                    rate=loadingSound.getframerate(),
                                    output=True)
                audioData = loadingSound.readframes(wavChunkSize)

                while len(audioData) != 0:
                    audioStream.write(audioData)
                    audioData = loadingSound.readframes(wavChunkSize)

                audioStream.stop_stream()
                audioStream.close()
                loadingSound.close()
            state = command
        elif command == 'exit':
            if proc:
                proc.kill()
            pyAudio.terminate()
            sys.exit()
        print('Current state: ' + state)
        if state == 'loaded_started':
            cmd = ['mplayer', '-slave', '-quiet', infile]
            print('playing ' + infile)
            proc = Popen(cmd, stdout=DEVNULL, stderr=DEVNULL, stdin=PIPE, universal_newlines=True, bufsize=1)
        elif (state in ['loaded_stopped', 'unloaded_stopped'] and proc):
            proc.kill()
        elif (state == 'loaded_paused' and proc):
            print('pause', flush=True, file=proc.stdin)

if __name__ == "__main__":
    main(sys.argv[1:])
