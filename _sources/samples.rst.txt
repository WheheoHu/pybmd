Samples
=========


.. code-block:: python

    """
    How to get current timeline name
    """
    from pybmd import Bmd
    LOCAL_RESOLVE = Bmd()
    #get current timeline
    project_manager=LOCAL_RESOLVE.get_project_manager()
    current_project=project_manager.get_current_project()
    current_timeline=current_project.get_current_timeline()
    #get timeline name
    current_timeline.get_name()


.. code-block:: python
    
    """
    How to use StillManager to grab a still from timeline markers
    """
    import pybmd

    EXPORT_PATH = "./Stills"
    LOCAL_RESOLVE = pybmd.Bmd()

    current_project=LOCAL_RESOLVE.project_manager().get_current_project()
    still_manager = pybmd.toolkits.StillManager(current_project)
    
    still_manager.grab_still_from_timeline_markers()
    still_manager.export_stills(EXPORT_PATH)
