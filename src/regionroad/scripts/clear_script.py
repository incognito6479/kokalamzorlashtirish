from regionroad.models import Road


def clear_roads():
    Road.objects.all().delete()


def run():
    clear_roads()
