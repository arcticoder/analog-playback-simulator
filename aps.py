import sys, getopt, wave, pyaudio
from subprocess import call, Popen, DEVNULL, PIPE


def main(argv):
    """
    Analog Playback Simulator (APS)
    Simulate navigating machine states as it plays back media.

    :param argv:
    :return:
    """
    state_graph = {
        'unloaded_stopped': {
            'loaded_stopped': {
                # transition sound effect, this will end up in a json file soon
                'audio': 'sound effects\load record short.wav'
            }
        },
        'loaded_stopped': {
            'loaded_started': {},
            'unloaded_stopped': {}
        },
        'loaded_started': {
            'loaded_paused': {
                'audio': 'sound effects\pause record short.wav'
            },
            'loaded_stopped': {}
        },
        'loaded_paused': {
            'loaded_started': {},
            'loaded_stopped': {}
        }
    }
    opts, args = getopt.getopt(argv, "hi:", ["infile="])
    proc = None
    for opt, arg in opts:
        if opt == '-h':
            print('aps.py -i <infile>')
            sys.exit()
        elif opt in ("-i", "--infile"):
            infile = arg
    py_audio = pyaudio.PyAudio()
    wavChunkSize = 1024

    state = 'unloaded_stopped'
    print('Current state: ' + state)
    while True:
        command = input('Enter new state (' + ','.join(state_graph[state]) + ') or exit):')

        if (command in state_graph[state]):
            # check for transition audio, play if found
            if ('audio' in state_graph[state][command]):
                audio_path = state_graph[state][command]['audio']
                loading_sound = wave.open(audio_path, "rb")
                audio_stream = py_audio.open(format = py_audio.get_format_from_width(loading_sound.getsampwidth()),
                                    channels = loading_sound.getnchannels(),
                                    rate = loading_sound.getframerate(),
                                    output=True)
                audio_data = loading_sound.readframes(wavChunkSize)

                while len(audio_data) != 0:
                    audio_stream.write(audio_data)
                    audio_data = loading_sound.readframes(wavChunkSize)

                audio_stream.stop_stream()
                audio_stream.close()
                loading_sound.close()
            state = command
        elif command == 'exit':
            if proc:
                proc.kill()
            py_audio.terminate()
            sys.exit()
        print('Current state: ' + state)
        if state == 'loaded_started':
            cmd = ['mplayer', '-slave', '-quiet', infile]
            print('playing ' + infile)
            proc = Popen(cmd, stdout = DEVNULL, stderr = DEVNULL, stdin = PIPE, universal_newlines = True, bufsize = 1)
        elif (state in ['loaded_stopped', 'unloaded_stopped'] and proc):
            proc.kill()
        elif (state == 'loaded_paused' and proc):
            print('pause', flush = True, file = proc.stdin)

if __name__ == "__main__":
    main(sys.argv[1:])
