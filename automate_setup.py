import os
import shutil
from pathlib import Path
import webbrowser
import threading


def create_django_project(project_name):
    os.system(f"django-admin startproject {project_name}")
    os.chdir(project_name)


def install_django_compressor():
    os.system("python -m pip install django-compressor")


def configure_django_settings(project_name):
    settings_path = os.path.join(os.getcwd(), project_name, "settings.py")
    with open(settings_path, "w") as f:
        f.write(
            """
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-2ye&_9@aev(f(8r&f$$e!o(*ycqi02b+-&r&utixj7a6(iyzws"

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "compressor",
    "app",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "app.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Compressor settings
COMPRESS_ROOT = BASE_DIR / "static"
COMPRESS_ENABLED = True
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)
"""
        )


def create_static_folders():
    os.makedirs("static/src", exist_ok=True)
    with open("static/src/input.css", "w") as f:
        f.write("@tailwind base;\n@tailwind components;\n@tailwind utilities;")


def create_views_and_templates():
    os.makedirs(f"{project_name}/templates", exist_ok=True)
    with open(f"{project_name}/templates/_base.html", "w") as f:
        f.write(
            """
<!-- templates/_base.html -->

{% load compress %}
{% load static %}

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Django + Tailwind</title>

    {% compress css %}
    <link rel="stylesheet" href="{% static 'src/output.css' %}">
    {% endcompress %}  
    <script src="https://unpkg.com/htmx.org@1.9.10"
        integrity="sha384-D1Kt99CQMDuVetoL1lrYwg5t+9QdHe7NLX/SoJYkXDFfX37iInKRy5xLSi8nO7UC"
        crossorigin="anonymous"></script> 

</head>

<body class="bg-gradient-to-r from-rose-100 to-teal-100">
    
    <div class="container mx-auto mt-4" id="content">
        {% block content %}
        {% endblock content %}
    </div>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.2.1/flowbite.min.js"></script>
</body>

</html>
"""
        )

    with open(f"{project_name}/views.py", "w") as f:
        f.write(
            """
from django.shortcuts import render


def index(request):
    return render(request, "index.html")
"""
        )

    with open(f"{project_name}/urls.py", "w") as f:
        f.write(
            f"""
from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
]    
"""
        )

    with open(os.path.join(project_name, "templates", "index.html"), "w") as f:
        f.write(
            """
{% extends "_base.html" %}

{% block content %}
<div class="flex justify-center items-center m-auto p-20 flex-col">
  <p class="text-5xl text-green-800 mb-5 font-black font-mono">Django and Tailwind CSS</p>
  <p class="text-xl font-medium font-mono font">Automated setup script by <a class="text-green-600 font-black text-xl hover:underline" href="https://github.com/mwwlean/django_tailwindcss_automated">@mwwlean</a></p>
</div>
{% endblock content %}
"""
        )


def setup_tailwind_outside_project():
    os.system("npm install -D tailwindcss")

    tailwind_config_content = """
/* Modified tailwind.config.js content */
module.exports = {
  content: ["../app/**/*.html"],
  theme: {
    extend: {},
  },
  plugins: [],
};
"""
    with open("tailwind.config.js", "w") as f:
        f.write(tailwind_config_content)

    # Run Tailwind CSS in watch mode
    os.system(
        "npx tailwindcss -i ./static/src/input.css -o ./static/src/output.css --watch"
    )


def main():
    global project_name
    project_name = "app"

    create_django_project(project_name)
    install_django_compressor()
    configure_django_settings(project_name)
    create_static_folders()
    create_views_and_templates()

    os.chdir(project_name)

    print(f"Django project '{project_name}' with Tailwind CSS has been created  ")


if __name__ == "__main__":
    main()
    os.chdir("..")
    setup_tailwind_outside_project()
