# analog-playback-simulator

Analog Playback Simulator (APS) simulates analog media (audio only for now) players such as record players, cassette players, 8-track players, reel-to-reel. Realistic model-specific behaviour is the goal of this project. CD players would work too, even though they're not analog.

Common state elements among analog devices for the purposes of this project are available commands (ie image region), audio clip (optional, state or transition), static image display (optional, state or transition). States and state transitions for each device model will have their own unique variations.

Media organization and selection is outside the scope of this project, playback will be from current directory only.

# Scope
* No artwork browsing yet. 
* No video (ex. RCA selectavision, VHS, Betamax, etc) yet, but anything mplayer can play should be doable in the long term.
* No animation (optional, state or transition). Will need to use pygame for this.
* Limiting rule complexity (ex. random noise from fault introduction) and global states (ex. dirty head/needle)
* This is not a DJ app nor is it intended to be, even though the first use case will be vinyl records. Standard usage only.
* Machine image sizes must be 800x600, JPEG not supported
* Media image sizes must be 600x600, JPEG not supported

# Requirements
* mplayer in system path
* python 3.x in system path
    * pyaudio
    * Pillow >= 2.0.0
    * Tkinter
* A simulated machine (JSON) and corresponding media for it. A sample file is included with the project but no media files yet (copyright issues).  

# Usage
python aps.py -i \<infile\> -s \<sim_machine_file.json\>

infile is audio media, sim_machine_file is a machine state graph

# Simulated Machine File
This is a state graph encoded as an adjacency list in JSON format(see sample_sm.json for example).
Sound effects and animation paths go in here. This must have initial_state, loaded_started, loaded_stopped, unloaded_stopped, and loaded_paused keys as they're the basic functionality common to all media players and they are used to send commands to mplayer.
