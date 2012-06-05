# Create your views here.
from django.template import RequestContext, loader
from put.zenbicycle.models import bicycle
from django.http import HttpResponse, HttpResponseForbidden
from django.views import static
from django.shortcuts import redirect, get_object_or_404
#from reportlab.pdfgen import canvas
#from reportlab.lib.pagesizes import letter, A4
from django.core import mail
from put import settings

def index(request):
    bicycle_list = bicycle.objects.all().order_by('id')[:5]
    template = loader.get_template('index.html')
    context = RequestContext(request, {
                'bicycle_list': bicycle_list,
        })
    return HttpResponse(template.render(context))

def detail(request, cd_id):
    template = loader.get_template('details.html')
    cd = get_object_or_404(bicycle, id=cd_id)
    
    # check if this CD is currently in our cart
    cart = request.session.get('cart', {})
    cart_quantity = cart.get(cd_id, 0)
    
    context = RequestContext(request, {
                'cd': cd, 
                'cart_quantity': cart_quantity 
        })
    return HttpResponse(template.render(context))

'''def confirm(request):
    # we have to check if user is authenticated..
    if not request.user.is_authenticated():
        return HttpResponseForbidden()

    cart = request.session.get('cart', {})
    
    #if cart is empty return to cart view
    if not cart:
        return redirect('/zenbicycle/cart')

    #setting canvas in pdf
    p = canvas.Canvas('cart.pdf', pagesize=letter)
    (width, height) = letter
    
    total_price = 0
        
    # line counter
    line_counter = 1
    
    #creating the view of pdf
    p.drawString(10, height - 25 * line_counter, 'You have order: ')  
    
    line_counter = line_counter + 1
    
    #creating table headings
    p.drawString(10, height - 25 * line_counter, 'TITLE')
    p.drawString(220, height - 25 * line_counter, 'AUTHOR')
    p.drawString(350, height - 25 * line_counter, 'COUNT')
    p.drawString(400, height - 25 * line_counter, 'PRICE')
    p.drawString(450, height - 25 * line_counter, 'TOTAL PRICE')
    p.line(10, height - 25 * line_counter - 5, 560, height - 25 * line_counter - 5)
    
    line_counter = line_counter + 1
    
    for cd_id in cart.keys():
        cd = bicycle.objects.get(id=cd_id)
        total_one_price = int(cart[cd_id])*cd.price
        total_price = total_price + total_one_price
        p.drawString(10, height - 25 * line_counter, cd.title)
        p.drawString(220, height - 25 * line_counter, cd.author)
        p.drawString(350, height - 25 * line_counter, str(cart[cd_id]))
        p.drawString(400, height - 25 * line_counter, str(cd.price))
        p.drawString(450, height - 25 * line_counter, '= '+str(total_one_price))
        p.line(10, height - 25 * line_counter - 5, 560, height - 25 * line_counter - 5)
        line_counter = line_counter + 1

    p.drawString(350, height - 25 * line_counter, 'total price: ')
    p.drawString(460, height - 25 * line_counter, str(total_price))

    p.showPage()
    p.save()

    #sending email with pdf
    connection = mail.get_connection()
    connection.open()
    
    # to do -> msg body, title, from, to
    email = mail.EmailMessage('Order Confirmation',
                              'Please find your order as an attachment.',
                              settings.DEFAULT_FROM_EMAIL,
                              [request.user.email])
    attachment = open('cart.pdf', 'rb')
    email.attach('cart.pdf', attachment.read(),'application/pdf')
    connection.send_messages([email])
    connection.close()

    return redirect('/zenbicycle/cart/confirm/success')
'''
def success(request):
    # we have to check if user is authenticated..
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    
    #clearing the cart
    del request.session['cart']

    template = loader.get_template('success.html')
    context = RequestContext(request)
    return HttpResponse(template.render(context))
    

def cart(request):
    # we have to check if user is authenticated..
    if not request.user.is_authenticated():
        return HttpResponseForbidden()

    template = loader.get_template('cart.html')

    # initialing variables
    prod_count = []
    total_price = 0
    errors_found = False
    cart = request.session.get('cart', {})
    
    for cd_id in cart.keys():
        error_name = ''
        cd = bicycle.objects.get(id=cd_id)
        
        # process form (if refresh clicked) 
        if request.POST:
            newCount = request.POST[str(cd.id)]
            #check newCount is a int > 0
            if not newCount.isdigit():
                errors_found = True
                error_name = 'count is not integer' 
            elif int(newCount) == 0:
                errors_found = True
                error_name = 'count is less then 1'
            else:
                cart[cd_id] = newCount
                
        single_cd_total_price = float(cart[cd_id]) * cd.price
        total_price = total_price + single_cd_total_price
        prod_count.append({'cd': cd, 
                           'count': cart[cd_id], 
                           'totalOne': single_cd_total_price,
                           'errorName': error_name,  
                         })
    
    # to ensure that quantity changes will be stored in session data
    # otherwise, session variable cart won't change!
    request.session['cart'] = cart
    
    context = RequestContext(request, {
                'prodCount': prod_count,
                'total': total_price,
                'error': errors_found
    })
    return HttpResponse(template.render(context))

def confirm_cart(request):
    # we have to check if user is authenticated..
    if not request.user.is_authenticated():
        return HttpResponseForbidden()

    template = loader.get_template('confirm.html')
    
    # initialing variables
    prod_count = []
    total_price = 0
    cart = request.session.get('cart', {})
    
    for cd_id in cart.keys():
        cd = bicycle.objects.get(id=cd_id)
        
        single_cd_total_price = float(cart[cd_id]) * cd.price
        total_price = total_price + single_cd_total_price
        
        prod_count.append({'cd': cd, 
                              'count': cart[cd_id], 
                              'totalOne': single_cd_total_price,
                             })
    
    context = RequestContext(request, {
                'prodCount': prod_count,  'total': total_price
    })
    return HttpResponse(template.render(context))

def add_to_cart(request, cd_id):
    # we have to check if user is authenticated..
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    
    # setting default quantity for lately added CD
    cart = request.session.get('cart', {})
    cart[cd_id] = 1
    
    # storing data in session variable
    request.session['cart'] = cart
    
    return redirect('/zenbicycle/'+str(cd_id))

def remove_from_cart(request, cd_id):
    # we have to check if user is authenticated..
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    
    # actually removing CD from the cart
    cart = request.session.get('cart', {})
    if cd_id in cart:
        del cart[cd_id]
        
    # storing data in session variable
    request.session['cart'] = cart
    
    return redirect('/zenbicycle/cart')

def serve_covers(request, cover_path):
    if request.user.is_authenticated():
        return static.serve(request, path=cover_path, document_root='zenbicycle/covers/')
    else:
        return HttpResponseForbidden()