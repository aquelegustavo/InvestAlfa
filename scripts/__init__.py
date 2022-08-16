import os


def start():
    os.system("python manage.py runserver")


def docs():
    command = ""
    cmds = ["pydoctor",
            "--project-name=APIAN",
            "--project-version=1.0.0",
            "--project-url=https://github.com/sghufsc/apian",
            "--html-viewsource-base=https://github.com/apian/authuser/tree/main",
            "--project-base-dir='.'",
            "--make-html",
            "--html-output=docs/build",
            "--docformat=google",
            "--template-dir=docs/theme",
            "--intersphinx=https://docs.python.org/3/objects.inv",
            "./apian"]

    for cmd in cmds:
        command += cmd + " "

    os.system(command)
