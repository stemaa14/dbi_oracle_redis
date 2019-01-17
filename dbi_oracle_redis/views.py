from pyramid.view import view_config
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer
from datetime import date

from .db.model import (Root, Product, Review, ReviewSchema)


@view_config(context=Root,
             renderer='templates/index.pt')
def index(context, request):
    return {}


@view_config(context=Product,
             renderer='templates/product.pt')
def product(context, request):
    form = Form(request, ReviewSchema)
    if 'review.submitted' in request.POST and form.validate():
        review = form.bind(Review())
        context.add_review(review)
    return {
        'customers': Root.get_instance().customers,
        'form': FormRenderer(form)
    }
