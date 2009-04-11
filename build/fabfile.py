import os, os.path

config.project = 'caffette'

# Targets:

def local_dev():
    config.fab_hosts = ['sambulldevbox.local']
    config.target_dir = '/home/sam/'
    config.target = 'local_dev'
    config.restart_apache = False


def preview():
    config.fab_hosts = ['caffette.pocketuniverse.ca']
    config.target_dir = '/home/sam/projects/'
    config.target = 'preview'
    config.restart_apache = True


# Operations:

def build(tree_ish):
    config.tree_ish = tree_ish
    local('rm -rf /var/tmp/%(project)s')
    local('git archive --format=tar --prefix=%(project)s/ %(tree_ish)s site conf/%(target)s'
            '| (cd /var/tmp/ && tar xf -)', fail='abort')
    local('mv /var/tmp/%(project)s/conf/%(target)s/* /var/tmp/%(project)s/conf/')
    local('rmdir /var/tmp/%(project)s/conf/%(target)s')


@requires('fab_hosts', 'target', 'target_dir', provided_by = [local_dev, preview])
def deploy(tag=None, branch='master'):
    "Build the project and deploy it to a specified environment."
    if tag:
        tree_ish = '%s-%s' % (config.project, tag)
    else:
        tree_ish = branch
    invoke((build, (tree_ish,)))
    old_dir = os.getcwd()
    os.chdir('/var/tmp/%s' % config.project)
    rsync_project(config.target_dir, exclude=['log', 'site/media/dynamic', 'settings_local.py'],
            delete=True, extra_opts='-l')
    os.chdir(old_dir)
    if config.restart_apache:
        sudo('/etc/init.d/apache2 restart')
