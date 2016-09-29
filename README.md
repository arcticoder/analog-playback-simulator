# analog-playback-simulator

Analog Playback Simulator (APS) simulates analog media (audio only for now) players such as record players, cassette players, 8-track players, reel-to-reel. Realistic model-specific behaviour is the goal of this project. CD players would work too, but then again so would a monkey eating a banana. If you want digital, mash your palm against/shout into your phone until media comes out.

Common state elements among analog devices for the purposes of this project are available commands (hotkey and/or image region), audio clip (optional, state or transition), static image display (optional, state-only), animation (optional, state or transition). States and state transitions for each device model will have their own unique variations.

Media organization and selection is outside the scope of this project, playback will be from current directory only.
Console application.

# Scope
* No artwork browsing yet. 
* No video (ex. RCA selectavision, VHS, Betamax, etc) yet, but anything mplayer can play should be doable in the long term.
* Limiting rule complexity (ex. random noise from fault introduction) and global states (ex. dirty head/needle) for initial milestones
* This is not a DJ app nor is it intended to be, even though the first use case will be vinyl records. Standard usage only.

# Requirements
mplayer in system path
python in system path

