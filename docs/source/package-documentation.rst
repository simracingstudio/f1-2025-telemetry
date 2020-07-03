.. _package-documentation:

=====================
Package Documentation
=====================

The *f1-2020-telemetry* package provides support for interpreting telemetry information as sent out over the network by `the F1 2020 game by CodeMasters <https://www.codemasters.com/game/f1-2020/>`_.
It also provides :ref:`command line tools <command_line_tools>` to record, playback, and monitor F1 2020 session data.

With each yearly release of the F1 series game, CodeMasters post a descripton of the corresponding telemetry packet format on their forum.
For F1 2020, the packet format is described here:

  https://forums.codemasters.com/topic/54423-f1%C2%AE-2020-udp-specification/

A formatted version of this specification, with some small issues fixed, is included in the *f1-2020-telemetry* package and can be found :ref:`here <telemetry-specification>`.

The *f1-2020-telemetry* package should work on Python 3.6 and above.

------------
Installation
------------

The f1-2020-telemetry package is `hosted on PyPI <https://pypi.org/project/f1-2020-telemetry/>`_.
To install it in your Python 3 environment, type:

.. code-block:: console

   pip3 install f1-2020-telemetry

When this completes, you should be able to start your Python 3 interpreter and execute this:

.. code-block:: python

   import f1_2020_telemetry.packet

   help(f1_2020_telemetry.packet)

Apart from the *f1_2020_telemetry* package (and its main module *f1_2020_telemetry.packet*), the ``pip3 install`` command will also install some command-line utilities that can be used to record, playback, and monitor F1 2020 telemetry data.
Refer to the :ref:`command_line_tools` section for more information.

-----
Usage
-----

If you want to write your own Python script to process F1 2020 telemetry data, you will need to set up the reception of UDP packets yourself.
After that, use the function *unpack_udp_packet()* to unpack the binary packet to an appropriate object with all the data fields present.

A minimalistic example is as follows:

.. literalinclude:: minimal_example.py
    :language: python
    :linenos:

This example opens a UDP socket on port 20777, which is the default port that the F1 2020 game uses to send packages;
it then waits for packages and, upon reception, prints their full contents.

To generate some data, start your F1 2020 game, and go to the Telemetry Settings (these can be found under Game Options / Settings).

* Make sure that the *UDP Telemetry* setting is set to *On*.
* The *UDP Broadcast* setting should be either set to *On*, or it should be set to *Off*, and then the *UDP IP Address* setting should be set to the IP address of the computer on which you intend to run the Python script that will capture game session data.
  For example, if you want the Python script to run on the same computer that runs the game, and you don't want to send out UDP packets to all devices in your home network, you can set the *UDP Broadcast* setting to *Off* and the *UDP IP Address* setting to *127.0.0.1*.
* The *UDP Port* setting can be keep its default value of *20777*.
* The *UDP Send Rate* setting can be set to *60*, assuming you have a sufficiently powerful computer to run the game.
* The *UDP Format* setting should be set to *2020*.

Now, if you start a race session with the Python script given above running, you should see a continuous stream of game data being printed to your command line terminal.

The example script given above is about as simple as it can be to capture game data.
For more elaborate examples, check the source code of the provided :ref:`f1_2020_telemetry.cli.monitor <source_monitor>` and :ref:`f1_2020_telemetry.cli.recorder <source_recorder>` scripts. Note that those examples are considerably more complicated because they use multi-threading.

.. _command_line_tools:

------------------
Command Line Tools
------------------

The f1-2020-telemetry package installs three command-line tools that provide basic recording, playback, and session monitoring support.
Below, we reproduce their command-line help for reference.

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
f1-2020-telemetry-recorder script
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   usage: f1-2020-telemetry-recorder [-h] [-p PORT] [-i INTERVAL]

   Record F1 2020 telemetry data to SQLite3 files.

   optional arguments:
     -h, --help                          show this help message and exit
     -p PORT, --port PORT                UDP port to listen to (default: 20777)
     -i INTERVAL, --interval INTERVAL    interval for writing incoming data to SQLite3 file, in seconds (default: 1.0)

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
f1-2020-telemetry-player script
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   usage: f1-2020-telemetry-player [-h] [-r REALTIME_FACTOR] [-d DESTINATION] [-p PORT] filename

   Replay an F1 2020 session as UDP packets.

   positional arguments:
     filename                                     SQLite3 file to replay packets from

   optional arguments:
     -h, --help                                   show this help message and exit
     -r REALTIME_FACTOR, --rtf REALTIME_FACTOR    playback real-time factor (higher is faster, default=1.0)
     -d DESTINATION, --destination DESTINATION    destination UDP address; omit to use broadcast (default)
     -p PORT, --port PORT                         destination UDP port (default: 20777)

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
f1-2020-telemetry-monitor script
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: console

   usage: f1-2020-telemetry-monitor [-h] [-p PORT]

   Monitor UDP port for incoming F1 2020 telemetry data and print information.

   optional arguments:
     -h, --help              show this help message and exit
     -p PORT, --port PORT    UDP port to listen to (default: 20777)

-------------------
Package Source Code
-------------------

The source code of all modules in the package is pretty well documented and easy to follow. We reproduce it here for reference.

.. _source_packets:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Module: f1_2020_telemetry.packets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Module *f1_2020_telemetry.packets* is the main module of the package. It implements ctypes *struct* types for all kinds of packets, and it implements the *unpack_udp_packet()* function that take the contents of a raw UDP packet and interprets is as the appropriate telemetry packet, if possible.

.. literalinclude:: ../../f1_2020_telemetry/packets.py
    :language: python
    :linenos:

.. _source_recorder:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Module: f1_2020_telemetry.cli.recorder
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Module *f1_2020_telemetry.cli.recorder* is a script that implements session data recorder functionality.

The script starts a thread to capture incoming UDP packets, and a thread to write captured UDP packets to an SQLite3 database file.

.. literalinclude:: ../../f1_2020_telemetry/cli/recorder.py
    :language: python
    :linenos:


.. _source_player:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Module: f1_2020_telemetry.cli.player
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Module *f1_2020_telemetry.cli.player* is a script that implements session data playback functionality.

The script starts a thread to read session data packets stored in a SQLite3 database file, and plays them back as UDP network packets. The speed at which playback happens can be changed by a command-line parameter.

.. literalinclude:: ../../f1_2020_telemetry/cli/player.py
    :language: python
    :linenos:

.. _source_monitor:

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Module: f1_2020_telemetry.cli.monitor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Module *f1_2020_telemetry.cli.monitor* is a script that prints live session data.

The script starts a thread to capture incoming UDP packets, and outputs a summary of incoming packets.

.. literalinclude:: ../../f1_2020_telemetry/cli/monitor.py
    :language: python
    :linenos:
