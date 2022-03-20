from os import path
from pybmd.project import Project
from typing import TYPE_CHECKING, Dict, List
if TYPE_CHECKING:
    from pybmd.bmd import Bmd

DatabaseList = List[Dict]

#TODO add docstring to functions
class ProjectManager:

    project_manager = None
    _current_project = None

    def __init__(self, _local_davinci: 'Bmd.local_davinci'):
        self.project_manager = _local_davinci.GetProjectManager()
        self._current_project = self.project_manager.GetCurrentProject()


    def close_project(self, project: Project) -> bool:  
        return self.project_manager.CloseProject(project.get_self_project())

    def create_folder(self, folder_name: str) -> bool:
        return self.project_manager.CreateFolder(folder_name)

    def create_project(self, project_name: str) -> Project:
        return Project(_project=self.project_manager.CreateProject(project_name), _project_name=project_name)

    def delete_folder(self, folder_name: str) -> bool:
        return self.project_manager.DeleteFolder(folder_name)

    def delete_project(self, project_name: str) -> bool:
        return self.project_manager.DeleteProject(project_name)

    def export_project(self, project_name: str, file_path: path, with_stills_and_luts=True) -> bool:
        return self.project_manager.ExportProject(project_name, str(file_path), with_stills_and_luts)

    def get_current_database(self) -> dict:
        return self.project_manager.GetCurrentDatabase()

    def get_current_project(self) -> Project:
        return Project(_project=self._current_project, _project_name=self._current_project.GetName())

    def get_database_list(self) -> DatabaseList:
        return self.project_manager.GetDatabaseList()

    def get_folder_list_in_current_folder(self) -> List[str]:
        return self.project_manager.GetFolderListInCurrentFolder()

    def get_project_list_in_current_folder(self) -> List[str]:
        return self.project_manager.GetProjectListInCurrentFolder()

    def goto_parent_folder(self) -> bool:
        return self.project_manager.GotoParentFolder()

    def goto_root_folder(self) -> bool:
        return self.project_manager.GotoRootFolder()

    def import_project(self, file_path: path) -> bool:
        return self.project_manager.ImportPorject(str(file_path))

    def load_project(self, project_name) -> Project:
        return Project(_project=self.project_manager.LoadProject(project_name), _project_name=project_name)

    def open_folder(self, folder_name: str) -> bool:
        return self.project_manager.OpenFolder(folder_name)

    def restore_project(self, file_path: path) -> bool:
        return self.project_manager.RestoreProject(str(file_path))

    def save_project(self) -> bool:
        return self.project_manager.SaveProject()

    def set_current_database(self, database_info: dict) -> bool:
        return self.project_manager.SetCurrentDatabase(database_info)
    
# More function BELOW!

    def database_info(self, _DbType,_DbName,_IpAddress='127.0.0.1'):
        return dict(DbType=_DbType,DbName=_DbName,IpAddress=_IpAddress)
    
    def save_and_close_current_project(self)->bool:
        self.save_project()
        return self.close_project(self.get_current_project())