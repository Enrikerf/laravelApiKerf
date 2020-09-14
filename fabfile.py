import os

from fabric.operations import run
from fabric.state import env
from fabric.context_managers import cd
from fabric.api import warn_only

environments = {
    'production': {
        'hosts': 'enrikerf@0.tcp.ngrok.io',
        'port': '18923',
        'home': '~/workspace/laravelApiKerf',
        'docker_build_commands': [],
        'docker_clean_commands': [],
        'git': {
            'parent': 'origin',
            'branch': 'master',
        }
    },
    'stage': {
        'hosts': 'ec2-3-133-109-29.us-east-2.compute.amazonaws.com',
        'port': '22',
        'user':'ubuntu',
        'connect_kwargs':{
            'key_filename': '~/.ssh/kerf-1.pem',
        },
        'home': '~/home/ubuntu',
        'docker_build_commands': [],
        'docker_clean_commands': [],
        'git': {
            'parent': 'origin',
            'branch': 'develop',
        }
    },
    'local': {
        'hosts': 'enrikerf@0.tcp.ngrok.io',
        'port': '18923',
        'home': '~/workspace/laravelApiKerf',
        'app': '~/workspace/laravelApiKerf/app',
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
    env.port = environments['stage']['port']


def local():
    environments['default'] = environments['local']
    env.hosts = environments['local']['hosts']
    env.port = environments['local']['port']


def git_pull(sha1):
    with cd(environments['default']['home']):
        run('ls -la')
        run(f'echo "{sha1}"')
        run('git pull %s %s' % (environments['default']['git']['parent'],
                                environments['default']['git']['branch']))

def app_commands():
    with cd(environments['default']['app']):
        #run(f'./scripts/preDeployScript') # echo to environment an maintenance scripts
        run(f'composer install')
        #run(f'p do:mi:mi')
        #run(f'./scripts/postDeployScript') # echo to environment an maintenance scripts

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
    app_commands()
    docker_commands()
