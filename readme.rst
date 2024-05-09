NoteTree
========

This is an elaboration on my Apropos application,
with a vertical rather than a horizontal organisation of notes,
based on a simple project management application I found on an IBM site.

At somepoint ago I pretty much abandoned it in favour of Doctree,
which I had started after wondering "If I'm going to have a tree in the left pane,
why not one with more levels than just one?"

I've been considering integrating this with DocTree by sharing the code base and
offering a simple and an extended version of the same application, or even combining
this with Apropos - so keeping this simplified version around would make researching
stuff like that easier.

In the mean time, I used this app to try out implementing classic gettext
multilanguage support.

Later I kind of revived the app to serve as a standalone version of the `Magiokis
Denk` web application. For that I extended it with the ability to add keywords to
the notes and show only notes with or without a certain keyword or text.

The application started out using *pickle* for storing the data. When I read it was
deemed unsafe or at least riskful, I decided to make the data backend configurable,
so now it's also possible to store in *json* format or even use an SQLite database.

Usage
-----

Call ``start.py`` from the top directory to start with a standard file in the
working directory, or use a file name as an argument to work with that.

Edit ``notetree/settings.py`` to select a gui frontend and a data backend (it defaults to
PyQt and pickle). You can even define your own file extension for notetree datafiles there.

Requirements
------------

- Python
- PyQT5 / wxPython (Pnoenix) for the GUI part

