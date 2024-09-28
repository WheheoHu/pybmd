from os import path
from pybmd.project import Project
from typing import TYPE_CHECKING, Dict, List


if TYPE_CHECKING:
    from pybmd.settings import CloudProjectsSetting

DatabaseList = List[Dict]


class ProjectManager:

    _project_manager = None
    _current_project = None

    def __init__(self, project_manager):
        self._project_manager = project_manager
   
    def close_project(self, project: Project) -> bool:
        """close project

        Args:
            project (Project): project to close

        Returns:
            bool: true if project was closed, false otherwise
        """
        return self._project_manager.CloseProject(project.get_self_project())

    def create_folder(self, folder_name: str) -> bool:
        """Creates a folder if folderName(string) is unique.

        Args:
            folder_name (str): folder name to create

        Returns:
            bool: True if folder was created, False otherwise
        """
        return self._project_manager.CreateFolder(folder_name)

    def create_project(self, project_name: str) -> Project:
        """Creates and returns a project if projectName(string) is unique, and None if it is not.

        Args:
            project_name (str): Project name to create

        Returns:
            Project: created project object
        """
        return Project(project=self._project_manager.CreateProject(project_name))

    def delete_folder(self, folder_name: str) -> bool:
        """Deletes the specified folder if it exists

        Args:
            folder_name (str): Folder name to delete

        Returns:
            bool: True if folder was deleted, False otherwise
        """
        return self._project_manager.DeleteFolder(folder_name)

    def delete_project(self, project_name: str) -> bool:
        """Delete project in the current folder if not currently loaded"""
        return self._project_manager.DeleteProject(project_name)

    def export_project(self, project_name: str, file_path: path, with_stills_and_luts=True) -> bool:
        """Exports project to provided file path

        Args:
            project_name (str): project to export
            file_path (path): file path to export to
            with_stills_and_luts (bool, optional): export project with still and luts. Defaults to True.

        Returns:
            bool: True if project was exported, False otherwise
        """
        return self._project_manager.ExportProject(project_name, str(file_path), with_stills_and_luts)

    def get_current_database(self) -> dict:
        """Returns a dictionary (with keys DbType, DbName and optional IpAddress) corresponding to the current database connection

        Returns:
            dict: database infomation with keys DbType, DbName and optional IpAddress
        """
        return self._project_manager.GetCurrentDatabase()

    def get_current_project(self) -> Project:
        """Returns the current project"""
        return Project(project=self._project_manager.GetCurrentProject())

    def get_database_list(self) -> DatabaseList:
        """return database list"""
        return self._project_manager.GetDatabaseList()

    def get_folder_list_in_current_folder(self) -> List[str]:
        """Returns a list of folder names in current folder."""
        return self._project_manager.GetFolderListInCurrentFolder()

    def get_project_list_in_current_folder(self) -> List[str]:
        """Returns a list of project names in current folder."""
        return self._project_manager.GetProjectListInCurrentFolder()

    def goto_parent_folder(self) -> bool:
        """Opens parent folder of current folder in database if current folder has parent."""
        return self._project_manager.GotoParentFolder()

    def goto_root_folder(self) -> bool:
        """Opens root folder in database."""
        return self._project_manager.GotoRootFolder()

    #Modified at DR18.0.0
    def import_project(self, file_path: path, project_name: str = None) -> bool:
        """Imports a project from the file path provided with given project name. Returns True if successful."""
        return self._project_manager.ImportPorject(str(file_path), project_name)

    def load_project(self, project_name) -> "Project":
        """Loads and returns the@Project  with name = project_name (string) if there is a match found, and None if there is no matching Project."""
        return Project(project=self._project_manager.LoadProject(project_name))

    def open_folder(self, folder_name: str) -> bool:
        """Opens folder under given name."""
        return self._project_manager.OpenFolder(folder_name)

    #Modified at DR18.0.0
    def restore_project(self, file_path: path, project_name: str = None) -> bool:
        """Restores a project from the file path provided with given project name. Returns True if successful."""
        return self._project_manager.RestoreProject(str(file_path), project_name)

    def save_project(self) -> bool:
        """Saves the currently loaded project with its own name. Returns True if successful."""
        return self._project_manager.SaveProject()

    def set_current_database(self, database_info: dict) -> bool:
        """Switches current database connection to the database specified by the keys below, and closes any open project.

        Args:
            database_info (dict): DbType: 'Disk' or 'PostgreSQL' (string) DbName: database name (string) IpAddress: IP address of the PostgreSQL server (string, optional key - defaults to '127.0.0.1')

        Returns:
            bool: True if database was set, False otherwise
        """
        return self._project_manager.SetCurrentDatabase(database_info)
    
    ##########################################################################################################################
    #Add at DR18.0.0
    
    def archive_project(self, project_name, file_path, is_archive_src_media: bool = True, is_archive_render_cache: bool = True, is_archive_proxy_media: bool = False) -> bool:
        """Archives project to provided filePath with the configuration as provided by the optional arguments"""
        return self._project_manager.ArchiveProject(project_name, file_path, is_archive_src_media, is_archive_render_cache, is_archive_proxy_media)

    ##############################################################################################################################
    #Add at DR18.6.4
    def create_cloud_project(self,cloud_setting:"CloudProjectsSetting") -> Project:
        """Creates and returns a cloud project.

        Args:
            cloud_setting (CloudProjectsSetting):  settings for the cloud project

        Returns:
            Project: returns a cloud project
        """        
        return Project(self._project_manager.CreateCloudProject(cloud_setting.asdict()))
    
    def import_cloud_project(self,file_path:str,cloud_setting:"CloudProjectsSetting") -> bool:
        """

        Args:
            file_path (str): filePath of file to import
            cloud_setting (CloudProjectsSetting): setting for the cloud project

        Returns:
            bool: Returns True if import cloud project is successful; False otherwise
        """        
        return self._project_manager.ImportCloudProject(file_path,cloud_setting.asdict())
    
    def restore_cloud_project(self,folder_path:str,cloud_setting:"CloudProjectsSetting") -> bool:
        """

        Args:
            folder_path (str): path of folder to restore
            cloud_setting (CloudProjectsSetting): setting for the cloud project

        Returns:
            bool: Returns True if restore cloud project is successful; False otherwise
        """        
        return self._project_manager.RestoreCloudProject(folder_path,cloud_setting.asdict())
    
# More function BELOW!

    def database_info(self, _DbType, _DbName, _IpAddress='127.0.0.1') -> dict:
        """database_info(DbType, DbName, IpAddress) generated for the database connection"""
        return dict(DbType=_DbType, DbName=_DbName, IpAddress=_IpAddress)

    def save_and_close_current_project(self) -> bool:
        """Saves the current project and closes it"""
        self.save_project()
        return self.close_project(self.get_current_project())
