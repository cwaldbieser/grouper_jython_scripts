
#export CLASSPATH=/opt/jyson-1.0.2/lib/jyson-1.0.2.jar

from edu.internet2.middleware.grouper import Group
from edu.internet2.middleware.grouper import Stem
from edu.internet2.middleware.grouper.privs import Privilege
from jython_grouper import getGroup, getStem

def walk_stems(session, stem):
    """
    Walk the trree rooted at `stem_name` and yield tuples of 
    (stem, sub_stems, groups).
    """
    if isinstance(stem, basestring):
        stem = getStem(session, stem_name)
    child_stems = tuple(stem.getChildStems())
    groups = tuple(stem.getChildGroups())
    for child_stem in child_stems:
        for result in walk_stems(session, child_stem):
            yield result
    yield (stem, child_stems, groups)

