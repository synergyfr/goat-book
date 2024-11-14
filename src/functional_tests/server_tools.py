
from fabric import Connection


def _get_manage_dot_py(host):
    return f"/venv/bin/python manage.py"


def reset_database(host):
    manage_dot_py = _get_manage_dot_py(host)
    conn = Connection(host=f"synapse@{host}")
    # conn.run('sudo docker exec -it superlists bash')
    conn.run(f"{manage_dot_py} flush --noinput")


def _get_server_env_vars(host):
    conn = Connection(host=f"synapse@{host}")
    env_lines = conn.run(f"cat /home/synapse/superlists.env").stdout.splitlines()
    return dict(l.split("=") for l in env_lines if l)


def create_session_on_server(host, email):
    manage_dot_py = _get_manage_dot_py(host)
    conn = Connection(host=f"synapse@{host}")

    env_vars = _get_server_env_vars(host)
    with conn.cd(), conn.prefix(f"export {' && export '.join(f'{k}={v}' for k, v in env_vars.items())}"):
        session_key = conn.run(f"{manage_dot_py} create_session {email}").stdout
        return session_key.strip()
