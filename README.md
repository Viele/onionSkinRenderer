# OnionSkinRenderer

Hello there, I am an animator with some programming skills. If you are a programmer and roll your eyes going through my code, please point out any mistakes I made :)

I started writing this plugin after I finished a 2D animation project. Going back to 3D I really missed
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


##How to install
The onionSkinRenderer.py file should be put into your plugin folder which is located in 
C:\Program Files\Autodesk\[maya version]\bin\plug-ins
and the onionSkinRendererUI.py to 
C:\Users\[username]\Documents\maya\scripts

After Maya startup, check the plugin Manager under Windows->Settings/Preferences->Plug-in Manager. The plugin should be in the first submenu. Make sure it is loaded.


##How to use
Make sure the plugin is loaded, and in the 3D view, Onion Skin Renderer is active as renderer.
Fire up the UI. There are two lists. The top one displays which frames are onionised and the bottom with which objects.
Select an object and next to the object list, click on "add selected".
Now enter a frame number in the top field and hit "add". If you start scrubbing back and forth in the timeline now, you should see the onion appear.


##Future plans
1. I will do a refactor of the whole code and properly comment it.
2. The operation to blend onions is still ADD because the onions have a black background, so mix would make the rest of the scene darker. I'll probably have to write my own shader to fix this, OR somebody explains to me how MTargetBlend works ;)
3. Version testing. I want this working on older versions of Maya as well.
4. Maybe if possible get maya to calculate a frame in the background with an asynch task. Though that might not even be possible.
5. Coloring and user transparency of onions would be nice. That probably needs a custom shader again.
6. Have a UI element that shows which frames are buffered.
