import sys, getopt, wave, pyaudio, json, tkinter
from subprocess import call, Popen, DEVNULL, PIPE

state = None

def mouseClicked(event):
    global state, mplayer_proc, root, image_ref, infile
    wav_chunk_size = 1024
    
    for edge_key in state_graph[state]['edges']:
        edge_state = state_graph[state]['edges'][edge_key]
        if (edge_state['region']['start_x'] <= event.x and
                    edge_state['region']['start_y'] <= event.y and
                    edge_state['region']['end_x'] > event.x and
                    edge_state['region']['end_y'] > event.y):
            command = edge_key

    # check for transition audio, play if found
    if ('audio' in state_graph[state]['edges'][command]):
        audio_path = state_graph[state]['edges'][command]['audio']
        loading_sound = wave.open(audio_path, "rb")
        audio_stream = py_audio.open(format=py_audio.get_format_from_width(loading_sound.getsampwidth()),
                                     channels=loading_sound.getnchannels(),
                                     rate=loading_sound.getframerate(),
                                     output=True)
        audio_data = loading_sound.readframes(wav_chunk_size)

        while len(audio_data) != 0:
            audio_stream.write(audio_data)
            audio_data = loading_sound.readframes(wav_chunk_size)

        audio_stream.stop_stream()
        audio_stream.close()
        loading_sound.close()
    previous_state = state
    state = command
    if ('img' in state_graph[state]):
        print('changing to image ' + state_graph[state]['img'])
        image_ref = tkinter.PhotoImage(file=state_graph[state]['img'])
        if (image_index):
            canvas.itemconfig(image_index, image=image_ref)
        else:
            canvas.create_image(400, 300, image=image_ref)

    if state == 'loaded_started':
        if (previous_state == 'loaded_paused'):
            print('pause', flush=True, file=mplayer_proc.stdin)
        else:
            cmd = ['mplayer', '-slave', '-quiet', infile]
            print('playing ' + infile)
            mplayer_proc = Popen(cmd, stdout=DEVNULL, stderr=DEVNULL, stdin=PIPE, universal_newlines=True, bufsize=1)
    elif (state in ['loaded_stopped', 'unloaded_stopped'] and mplayer_proc):
        mplayer_proc.kill()
    elif (state == 'loaded_paused' and mplayer_proc):
        print('pause', flush=True, file=mplayer_proc.stdin)


def main(argv):
    """
    Analog Playback Simulator (APS)
    Simulate navigating machine states as it plays back media.

    :param argv:
    :return:
    """
    # TODO: Don't use global variables, refactor into OOP
    global state, state_graph, root, py_audio, image_index, canvas, mplayer_proc, image_ref, infile
    opts, args = getopt.getopt(argv, "hi:s:", ["infile=", "machine="])
    infile = None
    smfile = None
    mplayer_proc = None

    for opt, arg in opts:
        if opt == '-h':
            print(
                'Usage:\npython aps.py -i <infile> -s <sim_machine_file.json>\ninfile is audio media, sim_machine_file is json')
            sys.exit()
        elif opt in ("-i", "--infile"):
            infile = arg
        elif opt in ("-s", "--machine"):
            smfile = arg

    if (not infile or not smfile):
        print('Must specify infile and simulated machine file')
        sys.exit()

    with open(smfile) as json_file:
        state_graph = json.load(json_file)

    py_audio = pyaudio.PyAudio()

    # create window
    root = tkinter.Tk()
    canvas = tkinter.Canvas(root, width=800, height=600)
    canvas.bind("<Button-1>", mouseClicked)
    canvas.pack()
    state = state_graph['initial_state']
    print('Current state: ' + state)
    image_index = None

    if ('img' in state_graph[state]):
        image_ref = tkinter.PhotoImage(file=state_graph[state]['img'])
        image_index = canvas.create_image(400, 300, image=image_ref)

    root.mainloop()

    if mplayer_proc:
        mplayer_proc.kill()

    py_audio.terminate()
    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
