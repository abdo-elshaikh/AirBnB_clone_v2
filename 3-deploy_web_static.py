#!/usr/bin/env python3
"""
Fabric script that creates and distributes an archive to your web servers
"""

from fabric.api import local, task, run, env, put
from datetime import datetime
from os import path

env.hosts = ['54.175.223.125', '54.196.34.67']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/my_ssh_private_key'


@task
def do_pack():
    """Creates a compressed archive from the
    contents of the web_static folder."""
    try:
        current_time = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        archive_path = 'versions/web_static_{}.tgz'.format(current_time)
        local('mkdir -p versions')
        local('tar -cvzf {} web_static'.format(archive_path))
        print('web_static packed: {} -> {}Bytes'
              .format(archive_path, path.getsize(archive_path)))
        return archive_path
    except Exception as e:
        return None


@task
def do_deploy(archive_path):
    """Distributes an archive to your web servers.
    arg:
      archive_path: path of the archive to deploy
    """
    if not path.exists(archive_path):
        return False

    archive_filename = path.basename(archive_path)
    archive_no_extension = path.splitext(archive_filename)[0]

    try:
        # Upload archive to /tmp/ directory on the web servers
        put(archive_path, '/tmp/')

        # Create release directory
        run('mkdir -p /data/web_static/releases/{}/'
            .format(archive_no_extension))

        # Uncompress the archive to the release directory
        run('tar -xzf /tmp/{} -C /data/web_static/releases/{}/'.format(
            archive_filename, archive_no_extension))

        # Delete the uploaded archive from the web servers
        run('rm /tmp/{}'.format(archive_filename))

        # Move contents to the proper location
        run('mv /data/web_static/releases/{}/web_static/*\
             /data/web_static/releases/{}/'
            .format(archive_no_extension, archive_no_extension))

        # Remove the old symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s /data/web_static/releases/{}/\
             /data/web_static/current'.format(
            archive_no_extension))

        print('New version deployed!')
        return True

    except Exception as e:
        print('Deployment failed:', e)
        return False


@task
def deploy():
    """Creates and distributes an archive to your web servers."""
    archive_path = do_pack()
    if archive_path:
        return do_deploy(archive_path)
    else:
        return False
