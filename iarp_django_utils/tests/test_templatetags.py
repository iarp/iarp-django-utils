from django.template import RequestContext
from django.test import RequestFactory, TestCase
from django.utils import timezone

from iarp_django_utils.templatetags import request_tools, datetime_tools


class RequestToolsTests(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_posted_or_default_expecting_default(self):
        request = self.factory.post('/')
        context = RequestContext(request)
        data = request_tools.posted_or_default(context, 'test', 'default')
        self.assertEqual('default', data)

    def test_posted_or_default_with_posted_data(self):
        request = self.factory.post('/', {'test': 'data in here'})
        context = RequestContext(request)
        data = request_tools.posted_or_default(context, 'test', 'default data')
        self.assertEqual('data in here', data)

    def test_posted_or_not_posted_posted_but_not_exists(self):
        request = self.factory.post('/', {'test': 'data in here'})
        context = RequestContext(request)

        data = request_tools.posted_or_not_posted(context, 'test', 'true', '123', '123', 'selected')
        self.assertEqual(data, '')

    def test_posted_or_not_posted_posted_and_exists(self):
        request = self.factory.post('/', {'test': 'true'})
        context = RequestContext(request)

        data = request_tools.posted_or_not_posted(context, 'test', 'true', '123', '123', 'selected')
        self.assertEqual(data, 'selected')

    def test_posted_or_not_posted_posted_as_get_and_exists(self):
        request = self.factory.get('/')
        context = RequestContext(request)

        data = request_tools.posted_or_not_posted(context, 'test', 'true', '123', '123', 'selected')
        self.assertEqual(data, 'selected')

    def test_posted_or_not_posted_posted_as_get_and_not_exists(self):
        request = self.factory.get('/')
        context = RequestContext(request)

        data = request_tools.posted_or_not_posted(context, 'test', 'true', '123', '231', 'selected')
        self.assertEqual(data, '')

    def test_build_url_with_existing_params(self):
        request = self.factory.get('/?test=here')
        context = {'request': request}

        output = request_tools.build_url_with_existing_params(context, page=2)
        expected = '/?test=here&page=2'
        self.assertEqual(expected, output)

    def test_build_url_with_existing_params_alters_existing_param(self):
        request = self.factory.get('/?test=here')
        context = {'request': request}

        output = request_tools.build_url_with_existing_params(context, page=2, test='blah')
        expected = '/?test=blah&page=2'
        self.assertEqual(expected, output)


class DateTimeToolsPositiveTests(TestCase):

    def test_smooth_timedelta(self):
        end = timezone.now()
        start = end - timezone.timedelta(hours=1)
        delta = end - start

        output = datetime_tools.smooth_timedelta(delta)
        self.assertEqual("60 minutes", output)

    def test_smooth_timedelta_single_day(self):
        end = timezone.now()
        start = end - timezone.timedelta(days=1)
        delta = end - start

        output = datetime_tools.smooth_timedelta(delta)
        self.assertEqual("24 hours", output)

    def test_smooth_timedelta_singles(self):

        end = timezone.now()
        start = end - timezone.timedelta(days=1, hours=1, minutes=1, seconds=1)
        delta = end - start

        output = datetime_tools.smooth_timedelta(delta)
        self.assertEqual("1 day 1 hour 1 minute 1 second", output)

    def test_smooth_timedelta_multiples(self):

        end = timezone.now()
        start = end - timezone.timedelta(days=2, hours=2, minutes=2, seconds=2)
        delta = end - start

        output = datetime_tools.smooth_timedelta(delta)
        self.assertEqual("2 days 2 hours 2 minutes 2 seconds", output)


class DateTimeToolsNegativeTests(TestCase):

    def test_smooth_timedelta(self):
        end = timezone.now()
        start = end + timezone.timedelta(hours=1)
        delta = end - start

        output = datetime_tools.smooth_timedelta(delta)
        self.assertEqual("60 minutes", output)

    def test_smooth_timedelta_single_day(self):
        end = timezone.now()
        start = end + timezone.timedelta(days=1)
        delta = end - start

        output = datetime_tools.smooth_timedelta(delta)
        self.assertEqual("24 hours", output)

    def test_smooth_timedelta_singles(self):

        end = timezone.now()
        start = end + timezone.timedelta(days=1, hours=1, minutes=1, seconds=1)
        delta = end - start

        output = datetime_tools.smooth_timedelta(delta)
        self.assertEqual("1 day 1 hour 1 minute 1 second", output)

    def test_smooth_timedelta_multiples(self):

        end = timezone.now()
        start = end + timezone.timedelta(days=2, hours=2, minutes=2, seconds=2)
        delta = end - start

        output = datetime_tools.smooth_timedelta(delta)
        self.assertEqual("2 days 2 hours 2 minutes 2 seconds", output)

    def test_smooth_timedelta_with_different_strs_pluralized_spaced_joiner(self):

        end = timezone.now()
        start = end + timezone.timedelta(days=2, hours=2, minutes=2, seconds=2)
        delta = end - start

        output = datetime_tools.smooth_timedelta(
            timedeltaobj=delta,
            day_str="d", days_str="ds",
            hour_str="hr", hours_str="hrs",
            minute_str="min", minutes_str="mins",
            second_str="sec", seconds_str="secs"
        )
        self.assertEqual("2 ds 2 hrs 2 mins 2 secs", output)

    def test_smooth_timedelta_with_different_strs_pluralized_spaceless_joiner(self):

        end = timezone.now()
        start = end + timezone.timedelta(days=2, hours=2, minutes=2, seconds=2)
        delta = end - start

        output = datetime_tools.smooth_timedelta(
            timedeltaobj=delta,
            day_str="d", days_str="ds",
            hour_str="hr", hours_str="hrs",
            minute_str="min", minutes_str="mins",
            second_str="sec", seconds_str="secs",
            str_joiner="",
        )
        self.assertEqual("2ds 2hrs 2mins 2secs", output)

    def test_smooth_timedelta_with_different_strs_singular_spaced_joiner(self):

        end = timezone.now()
        start = end + timezone.timedelta(days=1, hours=1, minutes=1, seconds=1)
        delta = end - start

        output = datetime_tools.smooth_timedelta(
            timedeltaobj=delta,
            day_str="d",
            hour_str="hr",
            minute_str="min",
            second_str="sec",
        )
        self.assertEqual("1 d 1 hr 1 min 1 sec", output)

    def test_smooth_timedelta_with_different_strs_singular_spaceless_joiner(self):

        end = timezone.now()
        start = end + timezone.timedelta(days=1, hours=1, minutes=1, seconds=1)
        delta = end - start

        output = datetime_tools.smooth_timedelta(
            timedeltaobj=delta,
            day_str="d",
            hour_str="hr",
            minute_str="min",
            second_str="sec",
            str_joiner=""
        )
        self.assertEqual("1d 1hr 1min 1sec", output)
