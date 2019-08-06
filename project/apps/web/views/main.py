from django.views import generic as g


class MainView(g.TemplateView):
    template_name = 'web/main.html'


main_view = MainView.as_view()
