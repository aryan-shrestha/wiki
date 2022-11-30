import random

from django.shortcuts import render, redirect

from . import util

def index(request):
    """
    If the user is searching for a page, then check if the page exists. If it does, then render the
    page. If it doesn't, then render a list of pages that contain the search keyword. On the otherhand,
    if the user is not searching for any page then it simply renders the index.html.
    
    :param request: The initial request sent from the client
    :return: the rendered template of the entry page.
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
    This is a function that is called when the user clicks on a entry listed on the index page. It checks if the
    entry exists, and if it does, it renders the entry_page.html page with the title and body of the
    entry 
    """
    body = util.get_entry(title)

    if body is not None:
        return render(request, 'encyclopedia/entry_page.html', {"title":title, "body":body})
    else:
        return render(request, "encyclopedia/page_not_found.html")


def create_entry(request):
    """
    If the request method is POST, then get the title and body from the request, and if the title
    already exists, then render the create_entry.html template with an error
    message. Otherwise, save the entry and redirect to the newly created entry page.
    
    :param request: The current request object
    :return: a render of the create_entry.html page.
    """
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
    """
    This function is called when the user clicks on the "Update Entry" link on the entry page. It checks if
    the entry exists, and if it does, it renders the update_entry.html page with form fields prefield
    with exisiting information".
    
    :param request: The current request object
    :param title: The title of the page to be updated
    :return: the rendered template.
    """

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
    """
    It redirects to a random page
    
    :param request: the HTTP request object
    :return: A redirect to the entry_page_view function with the random_title as the argument.
    """
    entries = util.list_entries()
    random_title = random.choice(entries)
    entry = util.get_entry(random_title)

    context = {
        "title": random_title,
        "body": entry,
    }

    return redirect('entry_page_view', random_title)