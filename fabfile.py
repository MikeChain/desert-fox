import os

from fabric import Connection, task


@task
def deploy(c: Connection):
    c.config.sudo.password = os.getenv("SUDO_PASS")

    with c.cd("~/proyecto/desert-fox"):
        c.run("git pull")

        with c.prefix("source env/bin/activate"):
            c.run("python -m pip install --upgrade pip")

            c.run("flask --app main db upgrade")

    c.sudo("systemctl restart desertfox")
    c.sudo("systemctl restart nginx")

    print("Deploy completo")


@task
def error(c: Connection):
    c.config.sudo.password = os.getenv("SUDO_PASS")
    output = c.sudo("tail /var/log/nginx/error.log")
    print(output.stdout)


@task
def access(c: Connection):
    c.config.sudo.password = os.getenv("SUDO_PASS")
    output = c.sudo("tail /var/log/nginx/access.log")
    print(output.stdout)
