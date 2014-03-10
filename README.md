PyVec is my journeyman attempt at creating a rudimentary 3D graphics engine. It's built on top of PyGame.

This is mostly just a neat learning experience for me - if I get something workable out of this, great; if I end up yanking my hair out and switching to C++... well, that too!

At present the game renders 3D shapes 'well enough' and has a modest if inaccurate and ineffectual collision detection system. There's also a ton of cruft under the main controller, because yeah.

It also has this weird habit of making pulse crash which causes a core dump -- which is weird because at present it makes no (intentional?) use of pygame.mixer, or any sound whatsoever. Unfortunately I have no idea what actually makes this happen, and while the Internet reports this behavior intermittently under PyGame as well, there appear to be no solutions at present. (apart from that C++ thing)

Anyway, since I don't want to be late to work, there are no instructions in this readme yet. What can I say, I suck. I'll have instructions one day, not because I think someone else will ever read this, but because otherwise I just might forget, and THEN where would I be?
