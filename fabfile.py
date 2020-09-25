import os

from fabric.api import local

POSTGRES_DB = 'postgres_db'
POSTGRES_USER = 'postgres_db_user'


def load_dump():
    current_path = os.path.dirname(__file__)
    list_filename = [file for file in os.listdir(current_path) if file.endswith('.dump') or file.endswith('.sql')]

    if not list_filename:
        return

    backup_path = '{}/{}'.format(current_path, list_filename[0])

    if '.dump' in backup_path:
        cmd = "docker exec -i $(docker ps | grep db_ | awk '{{ print $1 }}') pg_restore --no-acl " \
              '--no-owner -U {0} -d {1} < {2}'.format(POSTGRES_USER, POSTGRES_DB, backup_path)
    else:
        cmd = "docker exec -i $(docker ps | grep db_ | awk '{{ print $1 }}') psql -U {0} -d {1} < {2}" \
            .format(POSTGRES_USER, POSTGRES_DB, backup_path)

    local(cmd)


def makemigrations(app=''):
    local("docker exec -i $(docker ps | grep server_ | awk '{{ print $1 }}') python manage.py makemigrations {}".format(app))


def migrate(app=''):
    local("docker exec -i $(docker ps | grep server_ | awk '{{ print $1 }}') python manage.py migrate {}".format(app))


def createsuperuser():
    local("docker exec -it $(docker ps | grep server_ | awk '{{ print $1 }}') python manage.py createsuperuser")


def bash():
    local("docker exec -it $(docker ps | grep server_ | awk '{{ print $1 }}') bash")


def shell():
    local("docker exec -it $(docker ps | grep server_ | awk '{{ print $1 }}') python manage.py shell")


def dev():
    local('docker-compose run --rm --service-ports server')


def worker():
    local('docker-compose run --rm --service-ports worker')


def kill():
    local('docker kill $(docker ps -q)')


def remove_none_images():
    local('docker rmi -f $(docker images -f "dangling=true" -q)')
