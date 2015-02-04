DocTree
=======

This is an elaboration on my Apropos application,
with a vertical rather than a horizontal organisation of notes,
based on a simple project management application I found on an IBM site.

I pretty much abandoned it in favour of Doctree, which I started after wondering
"If I'm going to have a tree in the left pane, why not one with more levels
than just one?"

I've been considering integrating this with DocTree by sharing the code base and
offering a simple and an extended version of the same application, or even combining
this with Apropos - so keeping this simplified version around would make researching
stuff like that easier.

In the mean time, I used this app to try out implementing classic gettext
multilanguage support.

Lately I kind of revived the app to serve as a standalone version of the Magiokis
Denk web application. For that I extended it with the ability to add keywords to
the notes and show only notes with a certain keyword.

Usage
-----

Call ``nt_start.pyw`` from the top directory to start with a standard file in the
working directory, or use a file name as an argument to work with that.


Requirements
------------

- Python
- PyQT4 for the current GUI version
- wxPython for the older GUI version

Note that the current implementation uses *pickle* for storing the data, I'm in the
process of changing that to something safer.
