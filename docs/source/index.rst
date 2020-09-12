===========================================
Welcome to the *f1-2020-telemetry* package!
===========================================

The *f1-2020-telemetry* package provides support for interpreting telemetry information as sent out over the network by `the F1 2020 game by CodeMasters <https://www.codemasters.com/game/f1-2020/>`_.
It also provides :ref:`command line tools <command_line_tools>` to record, playback, and monitor F1 2020 session data.

-------------------
Project information
-------------------

The *f1-2020-telemetry* package and its documentation are currently at version **0.2.0**.

The project is distributed as a standard *wheel* package on PyPI.
This allows installation using the standard Python 3 *pip* tool as follows:

    pip install f1-2020-telemetry

The project source code is hosted as a Git repository on `GitLab <https://gitlab.com>`_:

  https://gitlab.com/gparent/f1-2020-telemetry/

The pip-installable package is hosted on `PyPI <https://pypi.org>`_:

  https://pypi.org/project/f1-2020-telemetry/

The documentation is hosted on `Read the Docs <https://readthedocs.org>`_:

  https://f1-2020-telemetry.readthedocs.io/en/latest/

-------------
Documentation
-------------

The documentation comes in two parts:

* The :ref:`package-documentation` provides guidance on installation and usage of the f1-2020-telemetry package, and documents the included command-line tools.
* The :ref:`telemetry-specification` is a non-authoritative copy of the CodeMasters telemetry packet specification, with some corrections applied.

.. toctree::
   :hidden:

   package-documentation
   telemetry-specification
