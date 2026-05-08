Samples
=========


.. code-block:: python

    """
    How to get current timeline name
    """
    from pybmd import Resolve
    LOCAL_RESOLVE = Resolve()
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
    from pybmd import Resolve
    from pybmd.toolkits import StillManager
    LOCAL_RESOLVE = Resolve()
    
    EXPORT_PATH = "./Stills"
    current_project=LOCAL_RESOLVE.get_project_manager().get_current_project()
    still_manager = StillManager(current_project)
    
    still_manager.grab_still_from_timeline_markers()
    still_manager.export_stills(EXPORT_PATH)
