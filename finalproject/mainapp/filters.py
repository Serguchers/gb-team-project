from .models import Article
from .forms import ArticleSearchForm


class ArticleFilter:
    def __init__(self, view, articles=None):
        self.view = view
        self.form_fields = ArticleSearchForm.base_fields.keys()
        if articles:
            self.articles = articles
        else:
            self.articles = None
            
        self.filters = {
            'tags': self.filter_by_tags,
            'title': self.filter_by_title,
            'created_order': self.filter_by_created_time
        }
    
    def run_filter(self):
        for field in self.form_fields:
            filter_param = self.view.request.GET.get(field, None)
            if filter_param:
                self.articles = self.filters.get(field)(filter_param)
                if self.articles is None:
                    return self.articles
        return self.articles
        
    def filter_by_title(self, title):
        self.articles = self.articles.filter(title__icontains=title)
        return self.articles
            
    def filter_by_tags(self, tags):
        tags = tags.replace(',', ' ').split(' ')
        self.articles = self.articles.filter(tags__name__in=tags)
        return self.articles

    def filter_by_created_time(self, ordering):
        self.articles = self.articles.order_by(ordering)
        return self.articles