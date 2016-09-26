
#export CLASSPATH=/opt/jyson-1.0.2/lib/jyson-1.0.2.jar

from edu.internet2.middleware.grouper.privs import Privilege
from edu.internet2.middleware.grouper import Stem
from edu.internet2.middleware.grouper import SubjectFinder
from edu.internet2.middleware.grouper.rules import RuleApi
from jython_grouper import getGroup, getStem

def makeStemInheritable(session, stemName, groupName, priv="admin"):
    """
    Make all descendant stems and groups created in a stem have the `priv`
    permission granted to `groupName`.

    :param session:`Grouper session`
    :param stemName:`Then name of the stem`
    :param groupName:`The name of the group that will have the permission on new child objects.`
    :param priv:`Optional: The privilege to grant.  Default 'admin'.`
    """
    baseStem = getStem(session, stemName)
    aGroup = getGroup(session, groupName)
    RuleApi.inheritGroupPrivileges(
        SubjectFinder.findRootSubject(),
        baseStem,
        Stem.Scope.SUB,
        aGroup.toSubject(),    
        Privilege.getInstances(priv))
    RuleApi.runRulesForOwner(baseStem)
    if priv == 'admin':
        RuleApi.inheritFolderPrivileges(
            SubjectFinder.findRootSubject(), 
            baseStem, 
            Stem.Scope.SUB, 
            aGroup.toSubject(),     
            Privilege.getInstances("stem, create"))
    RuleApi.runRulesForOwner(baseStem)

def normalizeInheritedPermissions(session, stemName):
    """
    Normalize the permissions inherited from a stem.
    """
    baseStem = getStem(session, stemName)
    RuleApi.reassignGroupPrivilegesIfFromGroup(
        SubjectFinder.findRootSubject(),
        baseStem,
        Stem.Scope.SUB)
    RuleApi.reassignStemPrivilegesIfFromGroup(
        SubjectFinder.findRootSubject(), 
        baseStem, 
        Stem.Scope.SUB) 
    RuleApi.runRulesForOwner(baseStem)
