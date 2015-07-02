
from edu.internet2.middleware.grouper.privs import AccessPrivilege
from jython_grouper import addStem, addGroup, getRootSession, getStem

def createAppSkeleton(session, parent_stem_path, app_extension, app_name=None):
    """
    Create the skeleton folder structure for a new application including
    an administrative group.
    
    :param:`session`: Grouper session.
    :param:`parent_stem_path`: String path to parent folder.
    :param:`app_extension`: String name of the app folder (*not* full path).
    :param:`app_name`: String "friendly" name of app folder (defaults to app extension).
    """
    app_extension.replace(":", "")
    if app_name is None:
        app_name = app_extension
    session = getRootSession()
    parent_stem = getStem(session, parent_stem_path)
    stem = addStem(session, app_extension, app_name, parentStem=parent_stem)
    etc_stem = addStem(session, "etc", "etc", parentStem=stem)
    export_stem = addStem(session, "exports", "exports", parentStem=stem)
    group_name = "%s_access_admins" % app_extension
    admin_group = addGroup(session, etc_stem.name, group_name, group_name)
    admin_group.grantPriv(admin_group.toMember().getSubject(), AccessPrivilege.ADMIN)

