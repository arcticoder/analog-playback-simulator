import sys, getopt, wave, pyaudio, json, tkinter
from subprocess import call, Popen, DEVNULL, PIPE


class APS:
    """
    Analog Playback Simulator (APS)
    Simulate navigating machine states as it plays back media.

    """
    state = None
    mplayer_proc = None
    state_graph = None
    root = None
    py_audio = None
    image_index = None
    image_ref = None
    canvas = None
    infile = None

    def __init__(self):
        self.py_audio = pyaudio.PyAudio()

    def init_args(self, argv):
        opts, args = getopt.getopt(argv, "hi:s:", ["infile=", "machine="])
        smfile = None

        for opt, arg in opts:
            if opt == '-h':
                print(
                    'Usage:\npython self.py -i <infile> -s <sim_machine_file.json>\ninfile is audio media, sim_machine_file is json')
                sys.exit()
            elif opt in ("-i", "--infile"):
                self.infile = arg
            elif opt in ("-s", "--machine"):
                smfile = arg

        if (not self.infile or not smfile):
            print('Must specify infile and simulated machine file')
            sys.exit()

        with open(smfile) as json_file:
            self.state_graph = json.load(json_file)

    def init_canvas(self):
        # create window
        self.root = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.root, width=800, height=600)
        self.canvas.bind("<Button-1>", self.mouse_clicked)
        self.canvas.pack()
        self.state = self.state_graph['initial_state']

        if ('img' in self.state_graph[self.state]):
            self.image_ref = tkinter.PhotoImage(file=self.state_graph[self.state]['img'])
            self.image_index = self.canvas.create_image(400, 300, image=self.image_ref)

    def main_loop(self):
        self.root.mainloop()

    def mouse_clicked(self, event):
        """
        Main app logic (loop), traverses SM graph by image region

        :param self:
        :param event:
        :return:
        """
        wav_chunk_size = 1024

        for edge_key in self.state_graph[self.state]['edges']:
            edge_state = self.state_graph[self.state]['edges'][edge_key]
            if (edge_state['region']['start_x'] <= event.x and
                        edge_state['region']['start_y'] <= event.y and
                        edge_state['region']['end_x'] > event.x and
                        edge_state['region']['end_y'] > event.y):
                command = edge_key

        # check for transition audio, play if found
        if ('audio' in self.state_graph[self.state]['edges'][command]):
            audio_path = self.state_graph[self.state]['edges'][command]['audio']
            loading_sound = wave.open(audio_path, "rb")
            audio_stream = self.py_audio.open(format=self.py_audio.get_format_from_width(loading_sound.getsampwidth()),
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
        previous_state = self.state
        self.state = command
        if ('img' in self.state_graph[self.state]):
            print('changing to image ' + self.state_graph[self.state]['img'])
            self.image_ref = tkinter.PhotoImage(file=self.state_graph[self.state]['img'])
            if (self.image_index):
                self.canvas.itemconfig(self.image_index, image=self.image_ref)
            else:
                self.canvas.create_image(400, 300, image=self.image_ref)

        if self.state == 'loaded_started':
            if (previous_state == 'loaded_paused'):
                print('pause', flush=True, file=self.mplayer_proc.stdin)
            else:
                cmd = ['mplayer', '-slave', '-quiet', self.infile]
                print('playing ' + self.infile)
                self.mplayer_proc = Popen(cmd, stdout=DEVNULL, stderr=DEVNULL, stdin=PIPE, universal_newlines=True,
                                          bufsize=1)
        elif (self.state in ['loaded_stopped', 'unloaded_stopped'] and self.mplayer_proc):
            self.mplayer_proc.kill()
        elif (self.state == 'loaded_paused' and self.mplayer_proc):
            print('pause', flush=True, file=self.mplayer_proc.stdin)

    def __del__(self):
        if self.mplayer_proc:
            self.mplayer_proc.kill()

        self.py_audio.terminate()


def main(argv):
    """
    main APS function. instantiates APS class, processes cli params

    :param argv:
    :return:
    """
    aps = APS()
    aps.init_args(argv)
    aps.init_canvas()
    aps.main_loop()


if __name__ == "__main__":
    main(sys.argv[1:])
