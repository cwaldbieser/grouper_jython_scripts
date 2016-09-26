
#export CLASSPATH=/opt/jyson-1.0.2/lib/jyson-1.0.2.jar

from edu.internet2.middleware.grouper.privs import Privilege
from jython_grouper import getGroup, getStem

def revokeGroupPrivByPredicate(session, groupName, predicate, privName="admin"):
    """
    Remove the privilege `privName` from all subjects that *immediately* have 
    the priv on `groupName` if `predicate` returns True for a subject.

    :param session:`Root session.`
    :param groupName:`The name of the Grouper group.`
    :param predicate:`A predicate that accepts a member as its argument.`
    :param privName:`The Privilege name to remove.  Default "admin".`
    """
    g = getGroup(session, groupName)
    privs = list(Privilege.getInstances(privName))
    priv = privs[0]
    membs = list(g.getImmediateMembers(priv.field))
    for memb in membs:
        if predicate(memb.subject):
            subject = memb.subject
            g.revokePriv(subject, priv)
    g.store()

def revokeStemPrivByPredicate(session, stemName, predicate, privNames=None):
    """
    Remove the privilege `privName` from all subjects that *immediately* have 
    the priv on `stemName` if `predicate` returns True for a subject.

    :param session:`Root session.`
    :param stemName:`The name of the Grouper stem.`
    :param predicate:`A predicate that accepts a member as its argument.`
    :param privNames:`The Privilege names to remove.  Default ["create", "stem"].`
    """
    if privNames is None:
        privNames = ["create", "stem"]
    stem = getStem(session, stemName)
    privs = [list(Privilege.getInstances(privName))[0] for privName in privNames]
    membs = set([])
    if "create" in privNames:
        for m in stem.creators:
            membs.add(m)
    if "stem" in privNames:
        for m in stem.stemmers:
            membs.add(m) 
    for memb in membs:
        if predicate(memb):
            for priv in privs:
                stem.revokePriv(memb, priv, False)
    stem.store()

def revokeGroupPrivBySubjectSourceId(session, groupName, subjectSourceId, privName="admin"):
    """
    Remove the privilege `privName` from all subjects that *immediately* have 
    the priv on `groupName` if a subject's source ID matches `subjectSourceId`.

    :param session:`Root session.`
    :param groupName:`The name of the Grouper group.`
    :param subjectSourceId:`Revoke only from subjects that have this source ID.`
    :param privName:`The Privilege name to remove.  Default "admin".`    
    """
    revokeGroupPrivByPredicate(
        session, 
        groupName, 
        makeSubjectSourceIdPredicate(subjectSourceId),
        privName)

def revokeStemPrivBySubjectSourceId(session, stemName, subjectSourceId, privNames=None):
    """
    Remove the privilege `privName` from all subjects that *immediately* have 
    the priv on `stemName` a subject's source ID matches `subjectSourceId`.

    :param session:`Root session.`
    :param stemName:`The name of the Grouper stem.`
    :param subjectSourceId:`Revoke only from subjects that have this source ID.`
    :param privNames:`The Privilege names to remove.  Default ["create", "stem"].`
    """
    revokeStemPrivByPredicate(
        session,
        stemName,
        makeSubjectSourceIdPredicate(subjectSourceId),
        privNames) 

def makeSubjectSourceIdPredicate(subjectSourceId):
    """
    Return a predicate that accepts a subject and
    returns True when its source ID matches `subjectSourceId`.
    """

    def _predicate(subject):
        return subject.sourceId == subjectSourceId
    
    return _predicate
