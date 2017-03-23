import simplejson as json
from django.contrib import messages



class AjaxMessaging(object):
    def process_response(self, request, response):
        print(request.GET)
        if request.is_ajax():
            if response['Content-Type'] in ['application/javascript', 'application/json']:
                try:
                    content = json.loads(response.content)
                except ValueError:
                    return response

                django_messages = []

                for message in messages.get_messages(request):
                    django_messages.append({
                        "level": message.level,
                        "message": message.message,
                        "extra_tags": message.tags
                    })

                # возникает ошибка при отображении question
                try:
                    content['django_messages'] = django_messages
                except Exception:
                    # возвращаем response без django_messages
                    return response

                response.content = json.dumps(content)

        return response
