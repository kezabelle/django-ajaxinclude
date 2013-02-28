The ajax-include-pattern for `Django`_
======================================

:author: Keryn Knight:
:status: Proof of concept

If you've got a bunch of ajax requests in your app, you could potentially ease
the HTTP round-trips by using the `Ajax-include pattern`_ as `demonstrated`_ by
`Filament Group`_. They published the library, and a bunch of code into a
`GitHub repository`_, which inspired me to hack up this proof of concept.


.. _Ajax-include pattern: http://filamentgroup.com/lab/ajax_includes_modular_content/
.. _demonstrated: http://filamentgroup.com/examples/ajax-include/demo.html
.. _Filament Group: http://filamentgroup.com/
.. _GitHub repository: https://github.com/filamentgroup/Ajax-Include-Pattern/

Giving it a spin
----------------

This assumes you're familiar with `Django`_, `virtualenv`_,
`virtualenvwrapper`_, and `git`_, and are on a sensible operating system::

    $ mkvirtualenv throwaway
    $ git clone https://github.com/kezabelle/django-ajaxinclude.git
    $ cd django-ajaxinclude
    $ python setup.py develop
    $ cd demo
    $ ./run.py

Open your browser and point it at ``http://127.0.0.1:8000``, and see that
everything works. You'll probably need to open your browser's developer console
to see the number of requests being made.

.. _Django: https://www.djangoproject.com/
.. _virtualenv: http://www.virtualenv.org/
.. _virtualenvwrapper: http://virtualenvwrapper.readthedocs.org/
.. _git: http://git-scm.com/

What it does
------------

If you've had a quick look at it, you'll note that the data changes every time
you refresh. This is because behind the scenes, the provided
``AjaxIncludeProxy`` view actually attempts to resolve and call every URL
passed to it in ``request.GET['files']``. Currently it does so very naively,
but I'll flesh it out to handle errors and exceptions at some point.

