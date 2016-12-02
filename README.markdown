MacModelShelf
=============

What?
-----

A small Python module that gives you nice human readable Macintosh model
names, e.g. "iMac (27-inch, Late 2009)", when given a serial number or model
code. It uses shelve to keep a persistent dictionary of model codes, and looks
up unknown model codes from Apple's servers.

How?
----

In your code:

    import macmodelshelf
    macmodelshelf.model_code("W12345825RU") # Returns the model code "5RU"
    macmodelshelf.model("5RU")              # Returns "iMac (27-inch, Late 2009)"

On the commandline:

    % ./macmodelshelf.py 5RU
    iMac (27-inch, Late 2009)

Dump?
-----

% ./macmodelshelf.py dump-json
macmodelshelfdump = {
    "000": "Power Mac G5",
    "00W": "Xserve (Late 2006)",
    "01P": "MacBook (13-inch, Late 2007)",
`…`
}
% ./macmodelshelf.py dump-markdown
Code | Model
:--- | :---
`000` | Power Mac G5
`00W` | Xserve (Late 2006)
`01P` | MacBook (13-inch, Late 2007)
`…`

For a dump of all the models in the current cache, see [`dump.markdown`](dump.markdown).
