import falcon

application = falcon.API(media_type=falcon.MEDIA_JSON)

if __name__ == '__main__':
    print(
        """
        To run source secrets and run with gunicorn or uwsgi:
        gunicorn --reload run
        uwsgi2.7 --ini ../fenixapi.ini:dev
        """
    )
