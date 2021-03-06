# Setting Things Up

I'll be using the Python programming language for the tutorials in this 
book.  Why Python?  Several scripting languages are used by data scientists and 
developers of data products---R for statistical analysis and data visualization, 
Perl for text processing and shell scripting, JavaScript for creating 
data-driven web apps---but none of these can do *all* of those things well.  
Python is a popular, easy-to-learn language that can be used for all the 
different tasks that we'll explore in this book, and it has become the go-to 
tool for many data projects.

We'll use a number of extensions to the core Python language (called *packages*) 
such as `NumPy` and `pandas`.  Instead of installing these all manually, I 
strongly recommend that you download the Anaconda Scientific Python Distribution 
provided for free for Mac or Windows by Continuum at 
`http://www.continuum.io/`.  Anaconda includes Python itself with a large 
bundle of packages commonly used by 
data scientists.  Conveniently, it makes its own copy of Python, so if you are 
already using another version of Python for other projects, the Anaconda 
installation will not delete or alter it.

You'll interact with Python via the IPython shell, also included with Anaconda, 
or by writing scripts in a text editor such as Notepad++, Atom, Brackets, 
Sublime, emacs or vim.  Anaconda includes a free Python IDE called Spyder that 
integrates a text editor and an IPython console, which you might find 
valuable. (Users of R will find it very similar to the exceptional RStudio IDE.)

You will want to be able to launch Python and IPython from your computer's 
command line shell.  Mac users know this as the Terminal, and Windows users
may know it as the "DOS prompt", `cmd.exe`, or the newer PowerShell. To test
that this works, type "python -V" and then "ipython -V" at your command 
prompt.  This should confirm the versions of Python and IPython you have 
installed.  If you get an error, or are seeing the wrong version number, 
the easiest thing to do is update your `PATH` environment variable.  This 
is done differently on each
operating system and sometimes across versions.  For instructions,
these links may be helpful:
    - Mac (and Linux) users: 
      http://coolestguidesontheplanet.com/add-shell-path-osx/
    - Windows uers: http://www.computerhope.com/issues/ch000549.htm

Continuum offers Anaconda with your choice of Python version 2 and Python 3.  I 
developed these tutorials using Python 3.5, so if you are using any version of 
Python 3, they should work fine.  Where possible I will try to use code that's 
compatible with Python 2, but I won't guarantee it.  If you find any bugs that 
break Python 2, please let me know and I'll update the book's code to resolve 
them.

You may work on the tutorials in this book in any order.  However, for those new 
to Python, you'll find that the earlier ones serve as an introduction to Python 
programming that you won't want to skip, and the later tutorials are more 
challenging.