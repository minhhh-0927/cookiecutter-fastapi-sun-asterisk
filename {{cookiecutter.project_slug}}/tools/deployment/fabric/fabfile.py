from fabric.api import env, local, run
from fabric.contrib.files import exists

REPO_URL = 'https://github.com/hjwp/book-example.git'  # 1

SITE_FOLDER = f'/home/{env.user}/sites/{env.host}'
SOURCE_FOLDER = f'{SITE_FOLDER}/source'


def deploy():
    _create_directory_structure_if_necessary(SITE_FOLDER)
    _get_latest_source()
    _update_settings(env.host)
    if env.use_docker == str(True):
        __build_within_docker()
    else:
        __build_without_docker()


def migrate_database():
    command_migrate = "alembic upgrade head"
    if env.use_docker == str(True):
        run(f'cd {SOURCE_FOLDER} && ../virtualenv/bin/{command_migrate} --noinput')
    else:
        run(f'cd {SOURCE_FOLDER} && docker-compose -f production.yml run --rm fastapi {command_migrate} --noinput')


def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')


def _get_latest_source():
    if exists(SOURCE_FOLDER + '/.git'):
        run(f'cd {SOURCE_FOLDER} && git fetch')
    else:
        run('git clone {REPO_URL} {source_folder}')
    current_commit = local("git log -n 1 --format=%H", capture=True)
    run(f'cd {SOURCE_FOLDER} && git reset --hard {current_commit}')


def _update_settings(site_name):
    pass
    # settings_path = source_folder + '/superlists/settings.py'
    # sed(settings_path, "DEBUG = True", "DEBUG = False")  # 1
    # sed(settings_path,
    #     'ALLOWED_HOSTS =.+$',
    #     'ALLOWED_HOSTS = ["%s"]' % (site_name,)  # 2
    #     )
    # secret_key_file = source_folder + '/superlists/secret_key.py'
    # if not exists(secret_key_file):  # 3
    #     chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    #     key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
    #     append(secret_key_file, "SECRET_KEY = '%s'" % (key,))
    # append(settings_path, '\nfrom .secret_key import SECRET_KEY')


def __build_within_docker():
    run(f'cd {SOURCE_FOLDER} & docker-compose -f production.yml up -d --build')


def __build_without_docker():
    _update_virtualenv()


def _update_virtualenv():
    virtualenv_folder = f'{SOURCE_FOLDER}/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'virtualenv --python=python3 {virtualenv_folder}')
    run(f'{virtualenv_folder}/bin/pip install -r {SOURCE_FOLDER}/production.txt')
