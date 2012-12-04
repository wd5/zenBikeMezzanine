
from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

from mezzanine.core.views import direct_to_template

from registration.forms import RegistrationFormUniqueEmail
from djangobb_forum import settings as forum_settings
from django_authopenid.urls import urlpatterns as authopenid_urlpatterns
import settings
from sitemap import SitemapForum, SitemapTopic

# for forum
for i, rurl in enumerate(authopenid_urlpatterns):
    if rurl.name == "registration_register":
        authopenid_urlpatterns[i].default_args.update({"form_class": RegistrationFormUniqueEmail})
        break

admin.autodiscover()

# Add the urlpatterns for any custom Django applications here.
# You can also change the ``home`` view to add your own functionality
# to the project's homepage.

sitemaps = {
    "forum": SitemapForum,
    "topic": SitemapTopic,
}

urlpatterns = patterns("",
    ("^admin/", include(admin.site.urls)),
    ("^shop/", include("cartridge.shop.urls")),
    ("^bikelist/", include("zenbicycle.urls")),
    (r"^sitemap.xml$", "django.contrib.sitemaps.views.sitemap", {"sitemaps": sitemaps}),
    (r"^f/account/", include("django_authopenid.urls")),
    ("^f/", include("zenBikeMezzanine.djangobb_forum.urls",namespace="djangobb")),
    url("^account/orders/$", "cartridge.shop.views.order_history",
        name="shop_order_history"),

    # We don't want to presume how your homepage works, so here are a
    # few patterns you can use to set it up.

    # HOMEPAGE AS STATIC TEMPLATE
    # ---------------------------
    # This pattern simply loads the index.html template. It isn't
    # commented out like the others, so it's the default. You only need
    # one homepage pattern, so if you use a different one, comment this
    # one out.

    url("^$", direct_to_template, {"template": "index.html"}, name="home"),

    # HOMEPAGE AS AN EDITABLE PAGE IN THE PAGE TREE
    # ---------------------------------------------
    # This pattern gives us a normal ``Page`` object, so that your
    # homepage can be managed via the page tree in the admin. If you
    # use this pattern, you'll need to create a page in the page tree,
    # and specify its URL (in the Meta Data section) as "home", which
    # is the name used below in the ``{"slug": "home"}`` part. Make
    # sure to uncheck "show in navigation" when you create the page,
    # since the link to the homepage is always hard-coded into all the
    # page menus that display navigation on the site.

    # url("^$", "mezzanine.pages.views.page", {"slug": "home"}, name="home"),

    # HOMEPAGE FOR A BLOG-ONLY SITE
    # -----------------------------
    # This pattern points the homepage to the blog post listing page,
    # and is useful for sites that are primarily blogs. If you use this
    # pattern, you'll also need to set BLOG_SLUG = "" in your
    # ``settings.py`` module, and delete the blog page object from the
    # page tree in the admin if it was installed.

    # url("^$", "mezzanine.blog.views.blog_post_list", name="home"),


)

# PM Extension
if (forum_settings.PM_SUPPORT):
    urlpatterns += patterns('',
        (r'^f/pm/', include('django_messages.urls')),
   )

if (settings.DEBUG):
    urlpatterns += patterns('',
        (r'^%s(?P<path>.*)$' % settings.MEDIA_URL.lstrip('/'),
            'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )

urlpatterns += patterns('',
        ("^", include("mezzanine.urls")),

)

# Adds ``STATIC_URL`` to the context of error pages, so that error
# pages can use JS, CSS and images.
handler500 = "mezzanine.core.views.server_error"
