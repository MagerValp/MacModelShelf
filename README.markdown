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
    ...
    }
    % ./macmodelshelf.py dump-markdown
    Code | Model
    :--- | :---
    `000` | Power Mac G5
    `00W` | Xserve (Late 2006)
    `01P` | MacBook (13-inch, Late 2007)
    ...

For a dump of all the models in the current cache, see [`dump.markdown`](dump.markdown).


License
-------

    Copyright 2012-2018 Per Olofsson, University of Gothenburg. All rights reserved.
    
    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at
    
        http://www.apache.org/licenses/LICENSE-2.0
    
    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
