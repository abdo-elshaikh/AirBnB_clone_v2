#!/usr/bin/python3
"""
Fabric script that distributes an archive to your web servers
"""

from fabric.api import env, run, put, local
from os.path import exists
from datetime import datetime

env.hosts = ['54.175.223.125', '54.196.34.67']
env.user = 'ubuntu'


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception as e:
        print("Packaging failed: {}".format(e))
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to your web servers using the function do_deploy
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Get the base name of the archive without the extension
        archive_filename = archive_path.split('/')[-1].split('.')[0]

        # Create the destination directory for the uncompressed archive
        run('mkdir -p /data/web_static/releases/{}'
            .format(archive_filename))

        # Uncompress the archive to the destination directory
        run('tar -xzf /tmp/{}.tgz -C /data/web_static/releases/{}/'
            .format(archive_filename, archive_filename))

        # Remove the archive from the web server
        run('rm /tmp/{}.tgz'.format(archive_filename))

        # Move the contents of the uncompressed archive to the web server
        run('mv /data/web_static/releases/{}/web_static/* \
            /data/web_static/releases/{}/'
            .format(archive_filename, archive_filename))

        # Remove the web_static directory inside the destination directory
        run('rm -rf /data/web_static/releases/{}/web_static'
            .format(archive_filename))

        # Remove the current symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link linked to the new version of the code
        run('ln -s /data/web_static/releases/{}/ /data/web_static/current'
            .format(archive_filename))

        print("New version deployed!")
        return True

    except Exception as e:
        print("Deployment failed: {}".format(e))
        return False


if __name__ == '__main__':
    archive_path = do_pack()
    result = do_deploy(archive_path)
    if result:
        local('curl 54.157.32.137/hbnb_static/0-index.html')
