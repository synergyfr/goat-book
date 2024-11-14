import os


def _create_or_update_dotenv():

    append('.env', 'DJANGO_DEBUG_FALSE=y')
    append('.env', f'SITENAME={env.host}')
    current_contents = run('cat .env')
    if 'DJANGO_SECRET_KEY' not in current_contents:
        new_secret = ''.join(
            random.SystemRandom().choices('abcdefghijklmnopqrstuvwxyz0123456789', k=50)
        )
        append('.env', f'DJANGO_SECRET_KEY={new_secret}')
    email_password = os.environ['EMAIL_PASSWORD']
    append('.env', f'EMAIL_PASSWORD={email_password}')

