#!/usr/bin/python3
"""
Fabric script based on 2-do_deploy_web_static.py
"""
from fabric.api import env, local, put, run
from datetime import datetime
import os

env.user = 'ubuntu'
env.hosts = ['54.175.223.125', '54.196.34.67']


def do_pack():
    """
    Create a tar archive of the web_static folder
    """
    try:
        if not os.path.exists("versions"):
            local("mkdir -p versions")
        date_format = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(date_format)
        local("tar -cvzf {} web_static".format(archive_path))
        return archive_path
    except Exception as e:
        return None


def do_deploy(archive_path):
    """
    Deploy the archive to the web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        filename = archive_path.split("/")[-1]
        no_ext = filename.split(".")[0]
        remote_path = "/data/web_static/releases/{}/".format(no_ext)

        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(remote_path))
        run("tar -xzf /tmp/{} -C {}".format(filename, remote_path))
        run("rm /tmp/{}".format(filename))
        run("mv {0}web_static/* {0}".format(remote_path))
        run("rm -rf {0}web_static".format(remote_path))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(remote_path))
        return True
    except Exception as e:
        return False


def deploy():
    """
    Deploy the web_static archive to the web servers
    """
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
