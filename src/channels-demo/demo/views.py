import random
from django.views import View
from django.http.response import JsonResponse

from .tasks import calculate
from .notify import notify


class StartJobView(View):

    def get(self, request, *args, **kwargs):
        print("Starting Job...")
        group_name = 'user-%s' % self.request.user.pk
        job_id = random.randint(10000000, 999999999999)

        calculate.delay(group_name, job_id)
        notify(group_name, "Started super expensive background job!")

        return JsonResponse({})
