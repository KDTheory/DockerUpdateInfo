INSTALLED_APPS = [
    #...
    "version_compare",
    #...
]

MIDDLEWARE = [
    #...
    "django.middleware.locale.LocaleMiddleware",
    #...
]

LANGUAGES = (
    ("en", _("English")),
    ("fr", _("Français")),
    # more than one language is expected here
)

LANGUAGE_CODE = "en"
USE_I18N = True
