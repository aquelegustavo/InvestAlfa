import os


def start():
    os.system("python manage.py runserver")


def docs():
    command = ""
    cmds = ["pydoctor",
            "--project-name=InvestAlfa",
            "--project-version=0.1.0",
            "--project-url=https://github.com/aquelegustavo/InvestAlfa",
            "--html-viewsource-base=https://github.com/aquelegustavo/InvestAlfa/tree/main",
            "--make-html",
            "--html-output=./investalfa/client/build/static/ref",
            "--docformat=google",
            "--intersphinx=https://docs.python.org/3/objects.inv",
            "./investalfa"]

    for cmd in cmds:
        command += cmd + " "

    os.system(command)
