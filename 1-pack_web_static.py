from datetime import datetime
from fabric.api import local, run, put, env
from os.path import isdir, exists

env.hosts = ['YOUR_SERVER_IP', 'YOUR_SERVER_IP']  # List of server IPs or hostnames

def do_pack():
    """
    Generate a .tgz archive from the contents of the web_static folder
    """
    try:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = f"versions/web_static_{now}.tgz"

        if not isdir("versions"):
            local("mkdir versions")

        local(f"tar -cvzf {archive_path} web_static")

        return archive_path
    except Exception as e:
        return None
