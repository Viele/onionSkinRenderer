# OnionSkinRenderer

Hello there, I am a technical animator or animTD or whatever you want to call it.

I started writing this script after I finished a 2D animation project. Going back to 3D I really missed
the onion skinning features of 2D applications and wondered if it wouldn't be possible to have it in 3D.
I know there are solutions like [bhGhost](http://www.graphite9.com/MayaDownloads.html) but they always display the same frame. I wanted to have something like the ghosting functionality in maya, but unfortunately this doesn't work with skinned meshes.

With my limited programming skills i jumped headfirst into the Maya API and probably cracked my head doing so.
It really took me a lot of patience and learning to wrap my head around the maya api.

It's also on gumroad, so if you like it please consider buying it for a few bucks.
https://gum.co/IDfYg


## Compatibility
It is now tested and working with 2016, 2017, 2018 and 2019.
Due to time constraints I will not work on this anymore, unless there are critical bugs that appear from the latest updates.

## How it works
This plugin is an extension to the standard viewport2.0 renderer. When Maya Renders a frame, a pass with the specified objects is created and stored. If you now tell the plugin to display information from another frame, it checks if that exists and if yes, draws it above the geometry.

### Pros
1. Independent of geometry complexity. Any polycount renders at the same speed.
2. Relative Onion Display. It is easy to display the Onion Relative to the current position because it is all buffered.
3. Actual display of the shape of the character on a different frame. Maya's internal onion skins (ghosting) cannot display skinned meshes, so you have to parent locators to it. Which is fine for tracking arcs but not to see how the shape moves through the scene.

### Cons
1. Since the onion skins are buffered when the frame is rendered, moving the camera or any object invalidates them.
2. Buffering alot of onion skins costs VRAM. If VRAM is full RAM is used which is a huge performance hit. That said, it shouldn't be an issue on any modern cards. My 3gb VRAM get me about 700 frames buffered on a 1080p screen. 


## How to install
Just copy the correct version to your scripts folder
Windows:
C:\Users\[username]\Documents\maya\scripts
Mac:
/Users/[UserName]/Library/Preferences/Autodesk/maya/2019/scripts

so it should be like 
C:\Users\[username]\Documents\maya\scripts\onionSkinRenderer\[all the files]


## How to use
Open the UI with
```
import onionSkinRenderer.controller as ctl
ctl.show()
```

Docking support has been removed from the latest version because it was too unstable on Maya 2019

Select an object and add it to Onion Skin Objects
Hit the toggle renderer button.
For relative display, activate a frame with the 'v' button. For absolute add current or type a number.
Scrub and as soon as the target onion is buffered it should be displayed.
