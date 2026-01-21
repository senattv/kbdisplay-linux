# kbdisplay-linux

An open-source python-based keyboard display program that operates similarly to
nohboard on windows. Tested only on Arch (CachyOS). I'll try to add more
functionality and keep the JSON layout specification similar to the one in
nohboard.

Currently allows background and images to be set per key (see
`layout/sena.json`) as an example.

# Usage

Run it like this:
```
$ ./kbdisplay.py layout/sena.json
```

Internally, the program runs `showmethekey-cli` as superuser, so that keypresses
can be registered even when not in focus (e.g., when you're streaming/recording
a game). Thus, it may ask for your password if you run as a local user.

# Requirements

You need the following:
 - python3 or above
 - the `showmethekey` dependency
 - the `tk` libraries.

On arch, everything can be installed as follows

```
$ sudo pacman -Suy showmethekey tk
```

This should be all you need to run the `usage` example above.
