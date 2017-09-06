import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import farmConfig

from utils.maya_talk import MayaTalk
from utils.mailing import send_mail


def publishOnFarmNew(episode, shot, task):
    # commands for initializing the autoPublish
    cmd1 = 'import sys, os'
    cmd2 = 'import pymel.core as pm'
    pyCmd = 'from farmUtils import wrappedAutoPublish;reload(wrappedAutoPublish);wrappedAutoPublish.wrappedPublish({}, {}, "{}")'.format(episode, shot, task)
    
    # let's initialize the autoPublish now
    with MayaTalk(host=farmConfig.autoPublishMachine, port=farmConfig.mayaPort) as talk:
        talk.command(cmd=cmd1)
        talk.command(cmd=cmd2)
        result = talk.command(cmd=pyCmd)
        print result, '<--------------'
        talk.command(cmd='pm.newFile(f=1)')


if __name__ == '__main__':
    print len(sys.argv), '<----------------------------------------'
    print sys.argv, '<==========================================='
    print sys.argv[0]
    print sys.argv[1]
    print sys.argv[2]
    print sys.argv[3]
    episode, shot, task = None, None, None
    if len(sys.argv) == 4:
        episode, shot, task = sys.argv[1], sys.argv[2], sys.argv[3]
    else:
        print 'Please pass proper arguments.'
    result = publishOnFarmNew(episode=episode, shot=shot, task=task)
