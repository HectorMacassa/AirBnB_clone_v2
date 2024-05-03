from fabric.api import run, put, env, sudo
from os.path import exists, isfile
from datetime import datetime

env.hosts = ['YOUR_SERVER_IP', 'YOUR_SERVER_IP']  # List of server IPs or hostnames
env.user = 'YOUR_USERNAME'  # Replace with your username
env.key_filename = 'PATH_TO_YOUR_PRIVATE_KEY'  # Replace with the path to your private key

def do_pack():
    """
    Generate a .tgz archive from the contents of the web_static folder
    """
    try:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = f"versions/web_static_{now}.tgz"

        if not exists("versions"):
            run("mkdir versions")

        run(f"tar -cvzf {archive_path} web_static")

        return archive_path
    except Exception as e:
        return None

def do_deploy(archive_path):
    """
    Distribute an archive to your web servers
    """
    if not exists(archive_path):
        return False

    try:
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        path = "/data/web_static/releases/{}/".format(no_ext)

        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Uncompress the archive to the folder /data/web_static/releases/<archive filename without extension>
        run("mkdir -p {}".format(path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, path))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(file_name))

        # Delete the symbolic link /data/web_static/current
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current
        run("ln -sf {}/ /data/web_static/current".format(path))

        return True
    except Exception as e:
        return False

def deploy():
    """
    Create and distribute an archive to your web servers
    """
    archive_path = do_pack()
    if not archive_path:
        return False

    return do_deploy(archive_path)
