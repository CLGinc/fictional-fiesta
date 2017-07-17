from urllib.parse import urlparse


def get_avatar(backend, strategy, details, response,
               user=None, *args, **kwargs):
    if not user.avatar:
        url = None
        if backend.name == 'google-oauth2':
            url = urlparse(response['image'].get('url'))
            url = '{}://{}{}'.format(url.scheme, url.netloc, url.path)
        elif backend.name == 'facebook':
            url = 'http://graph.facebook.com/{}/picture?type=large'.format(response['id'])
        if url:
            user.avatar = url
            user.save()
