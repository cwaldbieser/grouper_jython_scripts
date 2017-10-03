
from jython_grouper import *
from edu.internet2.middleware.grouper import MemberFinder

def getMembershipsForSubject(session, subj, immediate=True):
    """
    Given a subject, return all the memberships for that subject.
    """
    o = MemberFinder.findBySubject(session, subj)
    memberships = list(o.getMemberships())
    if not immediate:
        return memberships
    temp = []
    for m in memberships:
        if m.type == 'immediate':
            temp.append(m)
    return temp

def copyMembershipsToSubject(session, src_subj, dst_subj):
    """
    Copy all the immediate memberships from `src_subj` to `dst_subj`.
    """
    memberships = getMembershipsForSubject(session, src_subj)
    for m in memberships:
        group = m.group
        group.addMember(dst_subj, False)
        group.store()

