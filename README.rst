====
spec
====

Bash implementation of color spectrum for IP subneting

tcpdump live output
^^^^^^^^^^^^^^^^^^^

.. figure:: http://i.imgur.com/0iKAcJu.png
    :figwidth: image
    
tail on a nginx log file
^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: http://i.imgur.com/HgXTS5c.png
    :figwidth: image

How it works
------------

The theory is easy, every IP is unique and can be matched to a also unique color code.

Therefor every IP can be color-coded.

This is a Bash implementation of this idea, however since Bash is limited to 256 colors
it uses some trickery to make it still useful.

Usage examples
---------------

.. code-block:: bash

    $ tcpdump -nUl | spec
    $ tshark | spec
    $ tail -f /var/log/nginx/access.log | spec

Arguments
---------

.. figure:: http://i.imgur.com/7Hd5KUu.png
    :figwidth: image

Octets
^^^^^^

- **8**: Use the first 3 octets
- **16**: Use the first 2 octets
- **24**: Use the first octet

.. code-block:: bash
    
    $ tcpdump -nUl | spec --octet=24


Modes
^^^^^

- **octets**: Color the octets (default)
- **dots**: Color the dots

.. code-block:: bash
    
    $ tcpdump -nUl | spec --mode=dots


Why it matters
--------------

It matters because of a neuroscience theory called *Cognitive neuroscience of visual object recognition* which
states that the stage 1 of object recognition is *Processing of basic object components, such as _colour_, depth, and form.*

Read more: http://en.wikipedia.org/wiki/Cognitive_neuroscience_of_visual_object_recognition

This is all good, but IPs aren't object .. arn't they ?

Well yes and no. While analyzing logs our brain process them like object and try to remember, make grouping, relations and such.

But IPs are abstract numbers, written in white on a terminal. This offers little grip to our brain to store and process that information.

By associating more real world quality to IPs they become easier to remember, scan, group and make relations.

Yes, this is all about efficiency.

Performances
------------

It is quite fast. There is no real processing involved, it boils down to passing the output of your command to `sed`.

I don't have time to run any benchmarks, but if someone does, please share!


Enabling permanently
--------------------

The "good way" of using `spec` is to pipe it a text stream. However
for everyday use it can get old quite fast.

Fortunatly we can monkey patch our favorite commands to always use spec:

tcpdump
^^^^^^^

With this alias `spec` will be used only if the `-n` flag is passed to `tcpdump`.

.. code-block:: bash

    if $(command -v tcpdump >/dev/null 2>&1) ; then 
        _TCPDUMP=$(whereis tcpdump | cut -d" " -f2)
        alias tcpdump.nocolors="exec $_TCPDUMP $@"
        function tcpdump () {
            if [[ $1 =~ "-n" ]] ; then
                exec $_TCPDUMP -Ul $@ | spec
            else
                exec $_TCPDUMP $@
            fi
        }
    fi

tshark
^^^^^^

.. code-block:: bash

    if $(command -v tshark >/dev/null 2>&1) ; then 
        _TSHARK=$(whereis tshark | cut -d" " -f2)
        alias tshark.nocolor="exec $_TSHARK $@"
        function tshark () {
            if [[ $1 =~ "-n" ]] ; then
                exec $_TSHARK -l $@ | spec
            else
                exec $_TSHARK $@
            fi
        }
    fi

**Limitation**: this method has the disadvantage that you cannot pass arguments to `spec`. You must hardcode that flags you pass to it in your bash profile.
