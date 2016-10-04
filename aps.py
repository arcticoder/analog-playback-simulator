import sys, getopt, wave, pyaudio, json, tkinter
from subprocess import call, Popen, DEVNULL, PIPE


class APS:
    """
    Analog Playback Simulator (APS)
    Simulate navigating machine states as it plays back media.

    """
    _state = None
    _mplayer_proc = None
    _state_graph = None
    _root = None
    _py_audio = None
    _sm_image_index = None
    _sm_image_ref = None
    _media_image_index = None
    _media_image_ref = None
    _canvas = None
    _infile = None

    def __init__(self):
        self._py_audio = pyaudio.PyAudio()

    def init_args(self, argv):
        opts, args = getopt.getopt(argv, "hi:s:", ["infile=", "machine="])
        smfile = None

        for opt, arg in opts:
            if opt == '-h':
                print(
                    'Usage:\npython self.py -i <infile> -s <sim_machine_file.json>\ninfile is audio media, sim_machine_file is json')
                sys.exit()
            elif opt in ("-i", "--infile"):
                self._infile = arg
            elif opt in ("-s", "--machine"):
                smfile = arg

        if (not self._infile or not smfile):
            print('Must specify infile and simulated machine file')
            sys.exit()

        with open(smfile) as json_file:
            self._state_graph = json.load(json_file)

    def init_canvas(self):
        # create window
        self._root = tkinter.Tk()
        self._canvas = tkinter.Canvas(self._root, width=1400, height=600)
        self._canvas.bind("<Button-1>", self._mouse_clicked)
        self._canvas.pack()
        self._state = self._state_graph['initial_state']

        if ('img' in self._state_graph[self._state]):
            self._sm_image_ref = tkinter.PhotoImage(file=self._state_graph[self._state]['img'])
            self._sm_image_index = self._canvas.create_image(400, 300, image=self._sm_image_ref)

    def init_media(self):
        self._media_image_ref = tkinter.PhotoImage(file=self._state_graph['media']['img'])
        self._media_image_index = self._canvas.create_image(1100, 300, image=self._media_image_ref)

    def main_loop(self):
        self._root.mainloop()

    def _mouse_clicked(self, event):
        """
        Main app logic (loop), traverses SM graph by image region

        :param self:
        :param event:
        :return:
        """
        wav_chunk_size = 1024

        for edge_key in self._state_graph[self._state]['edges']:
            edge_state = self._state_graph[self._state]['edges'][edge_key]
            if (edge_state['region']['start_x'] <= event.x and
                        edge_state['region']['start_y'] <= event.y and
                        edge_state['region']['end_x'] > event.x and
                        edge_state['region']['end_y'] > event.y):
                command = edge_key

        # check for transition audio, play if found
        if ('audio' in self._state_graph[self._state]['edges'][command]):
            audio_path = self._state_graph[self._state]['edges'][command]['audio']
            loading_sound = wave.open(audio_path, "rb")
            audio_stream = self._py_audio.open(format=self._py_audio.get_format_from_width(loading_sound.getsampwidth()),
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
        previous_state = self._state
        self._state = command
        if ('img' in self._state_graph[self._state]):
            print('changing to image ' + self._state_graph[self._state]['img'])
            self._sm_image_ref = tkinter.PhotoImage(file=self._state_graph[self._state]['img'])
            if (self._sm_image_index):
                self._canvas.itemconfig(self._sm_image_index, image=self._sm_image_ref)
            else:
                self._canvas.create_image(400, 300, image=self._sm_image_ref)

        if self._state == 'loaded_started':
            if (previous_state == 'loaded_paused'):
                print('pause', flush=True, file=self._mplayer_proc.stdin)
            else:
                cmd = ['mplayer', '-slave', '-quiet', self._infile]
                print('playing ' + self._infile)
                self._mplayer_proc = Popen(cmd, stdout=DEVNULL, stderr=DEVNULL, stdin=PIPE, universal_newlines=True,
                                          bufsize=1)
        elif (self._state in ['loaded_stopped', 'unloaded_stopped'] and self._mplayer_proc):
            self._mplayer_proc.kill()
        elif (self._state == 'loaded_paused' and self._mplayer_proc):
            print('pause', flush=True, file=self._mplayer_proc.stdin)

    def __del__(self):
        if self._mplayer_proc:
            self._mplayer_proc.kill()

        self._py_audio.terminate()


def main(argv):
    """
    main APS function. instantiates APS class, processes cli params

    :param argv:
    :return:
    """
    aps = APS()
    aps.init_args(argv)
    aps.init_canvas()
    aps.init_media()
    aps.main_loop()


if __name__ == "__main__":
    main(sys.argv[1:])
