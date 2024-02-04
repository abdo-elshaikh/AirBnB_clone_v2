#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive from the contents of the web_static
"""

from fabric.api import local
from datetime import datetime
from os.path import exists


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
