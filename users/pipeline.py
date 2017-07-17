from urllib.parse import urlparse


def get_avatar(backend, strategy, details, response,
               user=None, *args, **kwargs):
    url = None
    if backend.name == 'google-oauth2':
        url = urlparse(response['image'].get('url'))
        url = '{}://{}{}'.format(url.scheme, url.netloc, url.path)
    if url:
        user.avatar = url
        user.save()
