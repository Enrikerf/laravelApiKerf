import os

from fabric.operations import run
from fabric.state import env
from fabric.context_managers import cd
from fabric.api import warn_only

environments = {
    'production': {
        'hosts': 'enrikerf@2.tcp.ngrok.io',
        'port': '15050',
        'home': '~/workspace/clase_6_pipeline',
        'docker_build_commands': [],
        'docker_clean_commands': [],
        'git': {
            'parent': 'origin',
            'branch': 'master',
        }
    },
    'stage': {
        'hosts': 'enrikerf@2.tcp.ngrok.io',
        'port': '15050',
        'home': '~/workspace/clase_6_pipeline',
        'docker_build_commands': [],
        'docker_clean_commands': [],
        'git': {
            'parent': 'origin',
            'branch': 'develop',
        }
    },
    'local': {
        'hosts': 'enrikerf@2.tcp.ngrok.io',
        'port': '15050',
        'home': '~/workspace/clase_6_pipeline',
        'docker_build_commands': [],
        'docker_clean_commands': [],
        'git': {
            'parent': 'origin',
            'branch': 'develop',
        }
    }
}


# setup
def production():
    environments['default'] = environments['production']
    env.hosts = environments['production']['hosts']
    env.port = environments['production']['port']


def stage():
    environments['default'] = environments['stage']
    env.hosts = environments['stage']['hosts']
    env.port = environments['production']['port']


def git_pull(sha1):
    with cd(environments['default']['home']):
        run(f'echo "{sha1}"')
        run('git pull %s %s' % (environments['default']['git']['parent'],
                                environments['default']['git']['branch']))


def docker_commands():
    with cd(environments['default']['home']):
        for command in environments['default']['docker_build_commands']:
            run(command)
    with warn_only():
        with cd(environments['default']['home']):
            for command in environments['default']['docker_clean_commands']:
                run(command)


def deploy():
    sha1 = os.environ.get('CI_COMMIT_SHA')
    print("SHA Commit", os.environ.get('CI_COMMIT_SHA'))
    print("SHA Commit", os.environ.get('CI_COMMIT_SHA'))
    git_pull(sha1)
    docker_commands()
