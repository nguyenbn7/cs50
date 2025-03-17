from django.shortcuts import render, redirect
from markdown2 import Markdown
import random as rand
from . import util
from urllib.request import quote, unquote


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def wiki(request, title):
    if util.get_entry(title) == None:
        return error(request, "error.html", f"Can not find {title}", 404)
    markdower = Markdown()
    return render(
        request,
        "title.html",
        {"title": title, "entry": markdower.convert(util.get_entry(title))},
    )


def search(request):
    title = request.GET.get("q", "").lower()
    entries = [t for t in util.list_entries() if title in t.lower()]
    if len(entries) == 1:
        if entries[0].lower() == title:
            return redirect(f"/wiki/{quote(entries[0])}",)
    return render(request, "result.html", {"title": "Results", "entries": entries})


def new(request):
    if request.method == "POST":
        title = request.POST.get("title")
        content = request.POST.get("content")
        if util.get_entry(title) != None:
            return error(request, "error.html", f"Page {title} exists")
        if title == "":
            return error(request, "error.html", "Title can not be empty")
        if content == "":
            return error(request, "error.html", "Content can not be empty")

        util.save_entry(title, content.encode("utf-8"))

        return redirect("/")
    return render(request, "new.html", {"title": "New Page",})


def edit(request, title):
    if request.method == "POST":
        util.save_entry(title, request.POST.get("content").encode("utf-8"))
        return redirect(f"/wiki/{quote(title)}")
    return render(
        request, "edit.html", {"title": title, "content": util.get_entry(title)}
    )


def random(request):
    entries = [quote(entry) for entry in util.list_entries()]
    return redirect(f"/wiki/{rand.choice(entries)}")


def page_not_found(request, exception, template_name="error.html"):
    return error(request, template_name, "Page not found", 404)


def bad_request(request, exception, template_name="error.html"):
    return error(request, template_name, "Bad request", 400)


def error(request, template_name, message, status=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render(
        request,
        template_name,
        {"top": status, "bottom": escape(message)},
        status=status,
    )


def isValid(title):
    for letter in title:
        if (
            letter
            not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-._~+"
        ):
            return False
    return True
