import random

from django.shortcuts import render, redirect

from . import util

def index(request):
    """
    index view first looks if there is any search quries made by user,
    if yes the function will return accordingly. On the otherhand if 
    there is no search queries, the function will return index (Homepage) 
    with all the entries listed.
    """
    search_keyword = request.GET.get('q')

    if search_keyword:
        body = util.get_entry(search_keyword) 
        if body is not None:
            return render(request, 'encyclopedia/entry_page.html', {"title": search_keyword,"body":body})
        else: 
            all_entries = util.list_entries()
            entries = []
            for entry in all_entries:
                if search_keyword.lower() in entry.lower():
                    entries.append(entry)
            context = {
                "heading": f"search results for {search_keyword}",
                "entries": entries
            }
            return render(request, 'encyclopedia/index.html', context)

    else:
        context = {
            "heading": "All Pages",
            "entries": util.list_entries(),
        }
        return render(request, "encyclopedia/index.html", context)


def entry_page_view(request, title):
    """
    this page renders the page given if the title matches else shows error
    message to the
    """
    body = util.get_entry(title)

    if body is not None:
        return render(request, 'encyclopedia/entry_page.html', {"title":title, "body":body})
    else:
        return render(request, "encyclopedia/page_not_found.html")


def create_entry(request):
    if request.method == "POST": 
        title = request.POST.get("title")
        body = request.POST.get("body")

        if util.get_entry(title) is not None:
            context = {
                "title": title,
                "body": body,
                "message": f"Entry with title '{title}' already exists",
            }
            return render(request, 'encyclopedia/create_entry.html', context)
        else:
            util.save_entry(title, body)
            context = {
                "title": title,
                "body": body,
            }
            return redirect('entry_page_view', title)
        
    return render(request, 'encyclopedia/create_entry.html')


def update_entry(request, title):

    entry = util.get_entry(title)
    if entry is not None:
        if request.method == "POST":
            title = request.POST.get("title")
            context = request.POST.get("body")
            util.save_entry(title, context)
            return redirect('entry_page_view', title)

        context = {
            "page": "update",
            "title": title,
            "body": entry
        }

        return render(request, 'encyclopedia/update_entry.html', context)
    else:
        return render(request, "encyclopedia/page_not_found.html")


def random_page(request):
    entries = util.list_entries()
    random_title = random.choice(entries)
    entry = util.get_entry(random_title)

    context = {
        "title": random_title,
        "body": entry,
    }

    return redirect('entry_page_view', random_title)