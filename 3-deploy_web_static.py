#!/usr/bin/python3
"""
Fabric script that creates and distributes an archive to your web servers
"""

from fabric.api import env, local, run, put
from datetime import datetime
from os.path import exists

env.hosts = ["54.175.223.125", "54.196.34.67"]
""" The list of host server IP addresses. """


def do_pack():
    """
    Function to pack the web_static content into a .tgz file
    """
    try:
        now = datetime.now()
        time_format = now.strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(time_format)

        local("mkdir -p versions")
        local("tar -czvf {} web_static".format(archive_path))

        return archive_path
    except Exception as e:
        return None


def do_deploy(archive_path):
    """
    Function to deploy an archive to the web servers
    """
    if not exists(archive_path):
        return False

    try:
        # Upload archive
        put(archive_path, "/tmp/")

        # Create release folder
        release_folder = "/data/web_static/releases/{}".format(
            archive_path.split("/")[-1].split(".")[0]
        )
        run("mkdir -p {}".format(release_folder))

        # Unpack archive
        run("tar -xzf /tmp/{} -C {}"
            .format(archive_path.split("/")[-1], release_folder))

        # Remove uploaded archive
        run("rm /tmp/{}".format(archive_path.split("/")[-1]))

        # Move contents to release folder
        run("mv {}/web_static/* {}".format(release_folder, release_folder))

        # Remove symbolic link
        run("rm -rf /data/web_static/current")

        # Create new symbolic link
        run("ln -s {} /data/web_static/current".format(release_folder))

        print("New version deployed!")
        return True
    except Exception as e:
        return False


def deploy():
    """
    Function to deploy the latest version of the web_static folder
    """
    archive_path = do_pack()

    if not archive_path:
        return False

    return do_deploy(archive_path)


if __name__ == "__main__":
    deploy()
