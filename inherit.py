
from edu.internet2.middleware.grouper.privs import Privilege
from edu.internet2.middleware.grouper import Stem
from edu.internet2.middleware.grouper import SubjectFinder
from edu.internet2.middleware.grouper.rules import RuleApi
from jython_grouper import getGroup, getStem

def makeStemInheritable(session, stemName, adminGroupName):
    """
    Make a stem's permissions inheritable by all descendant stems and groups.

    :param session:`Grouper session`
    :param stemName:`Then name of the stem`
    :param adminGroupName:`The name of the group that confers administrative privs`
    """
    baseStem = getStem(session, stemName)              
    adminGroup = getGroup(session, adminGroupName)
    RuleApi.inheritFolderPrivileges(
        SubjectFinder.findRootSubject(), 
        baseStem, 
        Stem.Scope.SUB, 
        adminGroup.toSubject(), 
        Privilege.getInstances("stem, create"))
    RuleApi.inheritGroupPrivileges(
        SubjectFinder.findRootSubject(), 
        baseStem, 
        Stem.Scope.SUB, 
        adminGroup.toSubject(), 
        Privilege.getInstances("admin")) 
    RuleApi.reassignGroupPrivilegesIfFromGroup(
        SubjectFinder.findRootSubject(), 
        baseStem, 
        Stem.Scope.SUB)
    RuleApi.reassignStemPrivilegesIfFromGroup(
        SubjectFinder.findRootSubject(), 
        baseStem, 
        Stem.Scope.SUB) 
