# OnionSkinRenderer

Hello there, I am an animator with some programming skills. If you are a programmer and roll your eyes going through my code, please point out any mistakes I made :)

I started writing this script after I finished a 2D animation project. Going back to 3D I really missed
the onion skinning features of 2D applications and wondered if it wouldn't be possible to have it in 3D.
I know there are solutions like [bhGhost](http://www.graphite9.com/MayaDownloads.html) but they come with a render overhead and
always display the same frame. I wanted to have something like the ghosting functionality in maya, but unfortunately this doesn't work with skinned meshes.

With my limited programming skills i jumped headfirst into the Maya API and probably cracked my head doing so.
It really took me a lot of patience and learning to wrap my head around the maya api.


##Compatibility
As of now the plugin is only tested with Maya 2017. If you have a different version feel free to test it and please tell me if it worked or not. 

BE WARNED: The UI will not work woth any other version than 2017 because I used QT5 (pyside2) for it and anything below 2017 still uses QT4 (pyside). It is not that hard to recode but it wasn't a priority for me.


##How it works
This plugin is an extension to the standard viewport2.0 renderer. When Maya Renders a frame, a pass with the specified objects is created and stored. If you now tell the plugin to display information from another frame, it checks if that exists and if yes, draws it above the geometry.

####Pros
1. Little overhead. Since it happens in renderer there is no additional geometry needed. Rendering additional passes per frame is very fast.
2. Relative Onion Display. It is easy to display the Onion Relative to the current position because it is all buffered.
3. Actual display of the shape of the character on a different frame. Maya's internal onions (ghosting) cannot display skinned meshes, so you have to parent locators to it. Which is fine for tracking arcs but not to see how the shape moves through the scene.

###Cons
1. Since the onions are buffered when the frame is rendered, moving the camera or any object invalidates them.
2. Buffering alot of onions costs VRAM. If VRAM is full RAM is used which is a huge performance hit. That said, it shouldn't be an issue on any modern cards. My 3gb VRAM get me about 700 frames buffered on a 1080p screen. 


##How to install
Just copy the folder to your scripts folder
C:\Users\[username]\Documents\maya\scripts


##How to use
Open the UI with

import onionSkinRenderer.onionSkinRendererWindow as onionWindow
import onionSkinRenderer.onionSkinRendererCore as onionCore
if __name__ == "__main__":
    try:
        onionUI.close()
    except:
        pass


	reload(onionCore)

    onionUI = onionWindow.OnionSkinRendererWindow()
    onionUI.show()


With the UI open a new renderer appears (Onion Skin Renderer) in the dropdown where you can choose between Viewport 2.0 and Legacy Viewport. Select it.
Select an object and add it to Onion Objects
For relative display, activate a frame with the 'v' button. For absolute add current or type a number.
Scrub and as soon as the target onion is buffered it should be displayed.


##Future plans
1. I will do a refactor of the whole code and properly comment it.
2. Version testing. I want this working on older versions of Maya as well.
