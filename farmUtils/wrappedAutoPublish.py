import os
import sys
import pymel.core as pm
# sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from config import farmConfig

from utils.mailing import send_mail

def wrappedPublish(episode, shot, task):
    autoPublishPath = 'P:/badgers_and_foxes/01_SAISON_1/00_PROGRAMMATION/shotgun_pipeline/tools'
    if autoPublishPath not in sys.path:
        sys.path.append(autoPublishPath)
    import auto_publish
    reload(auto_publish)
    pm.newFile(f=1)
    # Mailing part here....
    sub = ''
    body = ''
    sender = 'shiva.admin@pcgi.com'
    to = ['durgesh.n@pcgi.com']
    # TODO : Latter add database entry here.
    # Sadly getting back the result is still a bit unpredictable. Still working on it. 
    try:
        auto_publish.publish_shot_version(episode, shot, task)
        # auto_publish.publish_shot_version(epi, sh, task)
        # ret = auto_publish.publish_shot_version(epi, sh, task)
        pm.newFile(f=1)
        print 'Job Sucessed.................................................'
        sub = 'AutoPublish SUCCESS for {}_{}_{}'.format(episode, shot, task)
        body = 'SUCCESS...'
        retResult = True
    except Exception as ERR:
        pm.newFile(f=1)
        print 'Job FAILED...................................................'
        sub = 'AutoPublish Failed for {}_{}_{}'.format(episode, shot, task)
        body = 'FAILED MESSAGE - %s' % ERR
        retResult = False
        send_mail(mail_sub=sub, mail_body=body, sender=sender, receivers=to)
    return retResult