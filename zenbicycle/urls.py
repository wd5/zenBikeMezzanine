from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('zenbicycle.views',
    # ...
    (r'^$', "bikelist"),
    (r'^bike/(\d+)$', "bike"), 
    (r'^addbike/$', "addbike"),
    (r'^ajax/getmodel/$', 'feeds_bikemodel'),
    # ...
)
'''
urlpatterns = patterns('put.zenbicycle.views',
    (r'^$', 'index'),
    (r'^cart/$', 'cart'),
    (r'^cart/confirm/$', 'confirm_cart'),
   # (r'^cart/confirm/pdf/$', 'confirm'),
    (r'^cart/confirm/success/$', 'success'),
    (r'^(?P<cd_id>\d+)/$', 'detail'),
    (r'^(?P<cd_id>\d+)/cartadd/$', 'add_to_cart'),
    (r'^(?P<cd_id>\d+)/cartremove/$', 'remove_from_cart'),
    (r'^covers/(?P<img>\d+\.([jJ][pP][gG]|[pP][nN][gG]|[gG][iI][fF]))/$', 'serve_covers')
)
'''