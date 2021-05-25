# Libloader

Libloader provides a way to quickly and easily load shared libraries on macOS, Windows and Linux.

It also provides a COM module (libloader.com), making it easier to load COM DLLs on Windows.

## Functions.

### com

* prepare_gencache(): Prepare the gencache for COM. Not mandatory to be called by you, because load_com() calls it.
* load_com(*names): Let's you load a COM object. If you pass more than one, if the first fails, it will try the next one, until one works, or it runs out of objects.

### libloader

* load_library(library, x86_path=".", x64_path=".", *args, **kwargs): Load a library with the given name.
* _do_load(file, *args, **kwargs): Attempts to actually load the library. Used by load_library, although you can call it yourself.
* find_library_path(libname, x86_path=".", x64_path="."): Finds the path of the given library.
* get_functype(): Returns the ctypes functype of the given platform.
* get_library_extension(): Get the extension of the library for your current platform.
