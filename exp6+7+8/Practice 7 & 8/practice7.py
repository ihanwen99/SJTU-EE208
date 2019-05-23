import web
from web import form
import urllib2
import os
import lab7_Search

urls = (
    '/', 'index',
    '/s', 'text',
    '/im', 'index_img',
    '/i', 'image'
)

render = web.template.render('templates', cache=False)  # your templates

login = form.Form(
    form.Textbox('Searching'),
    form.Button('Search'),
)


def func_txt(command_practice):
    return lab7_Search.lab7txtSearch(command_practice)


def func_pic(command_practice):
    return lab7_Search.lab7picSearch(command_practice)


class index:
    def GET(self):
        f = login()
        return render.formtxt(f)


class index_img:
    def GET(self):
        f = login()
        return render.formimg(f)


class text:
    def GET(self):
        user_data = web.input()
        result_txt = func_txt(user_data.Searching)
        return render.result_search_txt(user_data.Searching, result_txt)


class image:
    def GET(self):
        user_data = web.input()
        result_pic = func_pic(user_data.Searching)
        return render.result_search_pic(user_data, result_pic)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
