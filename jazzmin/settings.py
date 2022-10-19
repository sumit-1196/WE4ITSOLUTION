import copy
import logging
from typing import Dict, Any
from django.conf import settings
from django.templatetags.static import static

from .utils import get_admin_url, get_model_meta

logger = logging.getLogger(__name__)

DEFAULT_SETTINGS: Dict[str, Any] = {
    "site_title": None,
    "site_header": None,
    "site_brand": None,
    "site_logo": "vendor/adminlte/img/AdminLTELogo.png",
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": "Welcome",
    "copyright": "",
    "search_model": None,
    "user_avatar": None,
    "topmenu_links": [],
    "usermenu_links": [],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": [],
    "custom_links": {},
    "icons": {"auth": "fas fa-users-cog", "auth.user": "fas fa-user", "auth.Group": "fas fa-users"},
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {},
    "language_chooser": False,
}

DEFAULT_UI_TWEAKS: Dict[str, Any] = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": False,
    "accent": "accent-primary",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": False,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": False,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success",
    },
}

THEMES = {
    "default": "vendor/bootswatch/default/bootstrap.min.css",
    "cerulean": "vendor/bootswatch/cerulean/bootstrap.min.css",
    "cosmo": "vendor/bootswatch/cosmo/bootstrap.min.css",
    "flatly": "vendor/bootswatch/flatly/bootstrap.min.css",
    "journal": "vendor/bootswatch/journal/bootstrap.min.css",
    "litera": "vendor/bootswatch/litera/bootstrap.min.css",
    "lumen": "vendor/bootswatch/lumen/bootstrap.min.css",
    "lux": "vendor/bootswatch/lux/bootstrap.min.css",
    "materia": "vendor/bootswatch/materia/bootstrap.min.css",
    "minty": "vendor/bootswatch/minty/bootstrap.min.css",
    "pulse": "vendor/bootswatch/pulse/bootstrap.min.css",
    "sandstone": "vendor/bootswatch/sandstone/bootstrap.min.css",
    "simplex": "vendor/bootswatch/simplex/bootstrap.min.css",
    "sketchy": "vendor/bootswatch/sketchy/bootstrap.min.css",
    "spacelab": "vendor/bootswatch/spacelab/bootstrap.min.css",
    "united": "vendor/bootswatch/united/bootstrap.min.css",
    "yeti": "vendor/bootswatch/yeti/bootstrap.min.css",
    "darkly": "vendor/bootswatch/darkly/bootstrap.min.css",
    "cyborg": "vendor/bootswatch/cyborg/bootstrap.min.css",
    "slate": "vendor/bootswatch/slate/bootstrap.min.css",
    "solar": "vendor/bootswatch/solar/bootstrap.min.css",
    "superhero": "vendor/bootswatch/superhero/bootstrap.min.css",
}

DARK_THEMES = ("darkly", "cyborg", "slate", "solar", "superhero")

CHANGEFORM_TEMPLATES = {
    "single": "jazzmin/includes/single.html",
    "carousel": "jazzmin/includes/carousel.html",
    "collapsible": "jazzmin/includes/collapsible.html",
    "horizontal_tabs": "jazzmin/includes/horizontal_tabs.html",
    "vertical_tabs": "jazzmin/includes/vertical_tabs.html",
}


def get_search_model_string(jazzmin_settings: Dict) -> str:
    """
    Get a search model string for reversing an admin url.

    Ensure the model name is lower cased but remain the app name untouched.
    """

    app, model_name = jazzmin_settings["search_model"].split(".")
    return "{app}.{model_name}".format(app=app, model_name=model_name.lower())


def get_settings() -> Dict:
    jazzmin_settings = copy.deepcopy(DEFAULT_SETTINGS)
    user_settings = {x: y for x, y in getattr(
        settings, "JAZZMIN_SETTINGS", {}).items() if y is not None}
    jazzmin_settings.update(user_settings)

    # Extract search url from search model
    if jazzmin_settings["search_model"]:
        jazzmin_settings["search_url"] = get_admin_url(
            get_search_model_string(jazzmin_settings))
        model_meta = get_model_meta(jazzmin_settings["search_model"])
        if model_meta:
            jazzmin_settings["search_name"] = model_meta.verbose_name_plural.title()
        else:
            jazzmin_settings["search_name"] = jazzmin_settings["search_model"].split(
                ".")[-1] + "s"

    # Deal with single strings in hide_apps/hide_models and make sure we lower case 'em
    if type(jazzmin_settings["hide_apps"]) == str:
        jazzmin_settings["hide_apps"] = [jazzmin_settings["hide_apps"]]
    jazzmin_settings["hide_apps"] = [x.lower()
                                     for x in jazzmin_settings["hide_apps"]]

    if type(jazzmin_settings["hide_models"]) == str:
        jazzmin_settings["hide_models"] = [jazzmin_settings["hide_models"]]
    jazzmin_settings["hide_models"] = [x.lower()
                                       for x in jazzmin_settings["hide_models"]]

    # Ensure icon model names and classes are lower case
    jazzmin_settings["icons"] = {x.lower(): y.lower()
                                 for x, y in jazzmin_settings.get("icons", {}).items()}

    # Default the site icon using the site logo
    jazzmin_settings["site_icon"] = jazzmin_settings["site_icon"] or jazzmin_settings["site_logo"]

    # ensure all model names are lower cased
    jazzmin_settings["changeform_format_overrides"] = {
        x.lower(): y.lower() for x, y in jazzmin_settings.get("changeform_format_overrides", {}).items()
    }

    return jazzmin_settings


def get_ui_tweaks() -> Dict:
    raw_tweaks = copy.deepcopy(DEFAULT_UI_TWEAKS)
    raw_tweaks.update(getattr(settings, "JAZZMIN_UI_TWEAKS", {}))
    tweaks = {x: y for x, y in raw_tweaks.items() if y not in (None, "", False)}

    # These options dont work well together
    if tweaks.get("layout_boxed"):
        tweaks.pop("navbar_fixed", None)
        tweaks.pop("footer_fixed", None)

    bool_map = {
        "navbar_small_text": "text-sm",
        "footer_small_text": "text-sm",
        "body_small_text": "text-sm",
        "brand_small_text": "text-sm",
        "sidebar_nav_small_text": "text-sm",
        "no_navbar_border": "border-bottom-0",
        "sidebar_disable_expand": "sidebar-no-expand",
        "sidebar_nav_child_indent": "nav-child-indent",
        "sidebar_nav_compact_style": "nav-compact",
        "sidebar_nav_legacy_style": "nav-legacy",
        "sidebar_nav_flat_style": "nav-flat",
        "layout_boxed": "layout-boxed",
        "sidebar_fixed": "layout-fixed",
        "navbar_fixed": "layout-navbar-fixed",
        "footer_fixed": "layout-footer-fixed",
        "actions_sticky_top": "sticky-top",
    }

    for key, value in bool_map.items():
        if key in tweaks:
            tweaks[key] = value

    def classes(*args: str) -> str:
        return " ".join([tweaks.get(arg, "") for arg in args]).strip()

    theme = tweaks["theme"]
    if theme not in THEMES:
        logger.warning("{} not found in {}, using default".format(
            theme, THEMES.keys()))
        theme = "default"

    dark_mode_theme = tweaks.get("dark_mode_theme", None)
    if dark_mode_theme and dark_mode_theme not in DARK_THEMES:
        logger.warning(
            "{} is not a dark theme, using darkly".format(dark_mode_theme))
        dark_mode_theme = "darkly"

    theme_body_classes = " theme-{}".format(theme)
    if theme in DARK_THEMES:
        theme_body_classes += " dark-mode"

    ret = {
        "raw": raw_tweaks,
        "theme": {"name": theme, "src": static(THEMES[theme])},
        "sidebar_classes": classes("sidebar", "sidebar_disable_expand"),
        "navbar_classes": classes("navbar", "no_navbar_border", "navbar_small_text"),
        "body_classes": classes(
            "accent", "body_small_text", "navbar_fixed", "footer_fixed", "sidebar_fixed", "layout_boxed"
        )
        + theme_body_classes,
        "actions_classes": classes("actions_sticky_top"),
        "sidebar_list_classes": classes(
            "sidebar_nav_small_text",
            "sidebar_nav_flat_style",
            "sidebar_nav_legacy_style",
            "sidebar_nav_child_indent",
            "sidebar_nav_compact_style",
        ),
        "brand_classes": classes("brand_small_text", "brand_colour"),
        "footer_classes": classes("footer_small_text"),
        "button_classes": tweaks["button_classes"],
    }

    if dark_mode_theme:
        ret["dark_mode_theme"] = {
            "name": dark_mode_theme,
            "src": static(THEMES[dark_mode_theme])
        }

    return ret
