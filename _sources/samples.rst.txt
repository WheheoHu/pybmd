Samples
=========
.. code-block:: python

    from pybmd import Bmd
    LOCAL_RESOLVE = Bmd()
    #get current timeline
    project_manager=LOCAL_RESOLVE.get_project_manager()
    current_project=project_manager.get_current_project()
    current_timeline=current_project.get_current_timeline()
    #get timeline name
    current_timeline.get_name()
