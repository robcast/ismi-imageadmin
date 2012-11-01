from celery import task

@task()
def move_to_archive(directory):
    pass