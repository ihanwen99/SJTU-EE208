import web
from web import form
import urllib2
import os
import lab7_Search

urls = (
    '/', 'index_fengjingsheying',
    '/i_qiche', 'index_qiche',
    '/i_meinv', 'index_meinv',
    '/i_meishitupian', 'index_meishitupian',
    '/fengjingsheying', 'fengjingsheying_image',
    '/qiche', 'qiche_image',  # wudihaohua
    '/meinv', 'meinv_image',  # meizi
    '/meishitupian', 'meishi_image'
)

render = web.template.render('templates', cache=False)  # your templates

login = form.Form(
    form.Textbox('Searching'),
    form.Button('Search'),
)


def func_pic(command_practice, STORE_DIR_pic):
    return lab7_Search.lab7picSearch(command_practice, STORE_DIR_pic)


class index_fengjingsheying:
    def GET(self):
        f = login()
        return render.formfengjingsheying(f)


class index_qiche:
    def GET(self):
        f = login()
        return render.formqiche(f)


class index_meinv:
    def GET(self):
        f = login()
        return render.formmeinv(f)


class index_meishitupian:
    def GET(self):
        f = login()
        return render.formmeishitupian(f)


class qiche_image:
    def GET(self):
        user_data = web.input()
        STORE_DIR_pic = "qichetuku_pic_index"
        result_pic = func_pic(user_data.Searching, STORE_DIR_pic)

        return render.result_search_pic(user_data, result_pic)


class fengjingsheying_image:
    def GET(self):
        user_data = web.input()
        STORE_DIR_pic = "fengjingsheying_pic_index"
        result_pic = func_pic(user_data.Searching, STORE_DIR_pic)

        return render.result_search_pic(user_data, result_pic)


class meinv_image:
    def GET(self):
        user_data = web.input()
        STORE_DIR_pic = "meinvtupian_pic_index"
        result_pic = func_pic(user_data.Searching, STORE_DIR_pic)

        return render.result_search_pic(user_data, result_pic)


class meishi_image:
    def GET(self):
        user_data = web.input()
        STORE_DIR_pic = "meishitupian_pic_index"
        result_pic = func_pic(user_data.Searching, STORE_DIR_pic)

        return render.result_search_pic(user_data, result_pic)


if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
