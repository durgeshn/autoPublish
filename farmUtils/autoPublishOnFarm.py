import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import farmConfig

from utils.maya_talk import MayaTalk
from utils.mailing import send_mail


def publishOnFarm(episode, shot, task):
    # commands for initializing the autoPublish
    cmd1 = 'import sys, os'
    cmd2 = 'import pymel.core as pm'
    cmd3 = 'sys.path.append(\'P:/badgers_and_foxes/01_SAISON_1/00_PROGRAMMATION/shotgun_pipeline/tools\')'
    cmd4 = 'import auto_publish'
    cmd5 = 'reload(auto_publish)'
    cmd6 = 'pm.newFile(f=1)'
    pyCmd = 'import auto_publish;auto_publish.publish_shot_version({}, {}, "{}")'.format(episode, shot, task)
    
    # let's initialize the autoPublish now
    with MayaTalk(host=farmConfig.autoPublishMachine, port=farmConfig.mayaPort) as talk:
        talk.command(cmd=cmd1)
        talk.command(cmd=cmd2)
        talk.command(cmd=cmd3)
        talk.command(cmd=cmd4)
        talk.command(cmd=cmd5)
        talk.command(cmd=cmd6)
        result = talk.command(cmd=pyCmd)
        talk.command(cmd=cmd6)
        print result, '<--------------'
    # Mailing part here.
    sub = ''
    body = ''
    sender = 'shiva.admin@pcgi.com'
    to = ['durgesh.n@pcgi.com']

    # TODO : Latter add database entry here.
    # Sadly getting back the result is still a bit unpredictable. Still working on it. 
    retResult = True
    if 'ERROR:' in result or 'FAILURE:' in result:
        print 'Registering Failed Publish for the shot {}'.format('BDG{}_{}'.format(episode, shot))
        sub = 'AutoPublish Failed for {}_{}_{}'.format(episode, shot, task)
        body = result.rstrip()
        retResult = False
    else:
        print 'Registering Successful Publish for the shot {}'.format('BDG{}_{}'.format(episode, shot))
        sub = 'AutoPublish Success for {}_{}_{}'.format(episode, shot, task)
        body = 'SUCCESS...'
        retResult = True

    send_mail(mail_sub=sub, mail_body=body, sender=sender, receivers=to)


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
    result = publishOnFarm(episode=episode, shot=shot, task=task)
