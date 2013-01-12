from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('zenbicycle.views',
    # ...
    (r'^$', 'bikelist'),
    (r'^bike/(\d+)$', 'bike'),
    (r'^addbike/$', 'addbike'),
    (r'^mybikes/$', 'user_bike_list'),
    (r'^ajax/getmodel/$', 'feeds_bikemodel'),
    # ...
)
