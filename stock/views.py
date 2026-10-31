from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from.models import Product, Sale, MatumiziYaFaida, RepotiYaMwezi, RepotYaMwaka 
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.db import IntegrityError
from django.utils import timezone
from django.db.models import Sum
import calendar
from django.db.models import Sum

@login_required
def home(request):
    leo = timezone.localtime(timezone.now())

    # Tunaanza na mwezi wa mwisho
    last_sale = Sale.objects.order_by('-tarehe').first()
    if last_sale:
        mwaka_huu = last_sale.tarehe.year
        mwezi_huu = last_sale.tarehe.month
    else:
        mwaka_huu = leo.year
        mwezi_huu = leo.month

    leo_siku = leo.day
    siku_za_mwezi = calendar.monthrange(mwaka_huu, mwezi_huu)[1]

    # zote
    sales_zote = list(Sale.objects.all())
    mat_zote = list(MatumiziYaFaida.objects.all())


    #===  
    sales_mwezi = [s for s in sales_zote if s.tarehe.year == mwaka_huu and s.tarehe.month == mwezi_huu]
    mat_mwezi = [m for m in mat_zote if m.tarehe.year == mwaka_huu and m.tarehe.month == mwezi_huu]

    sales_mwaka = [s for s in sales_zote if s.tarehe.year == mwaka_huu]
    mat_mwaka = [m for m in mat_zote if m.tarehe.year == mwaka_huu]

    # hesabu za mwezi
    faida_kabla = sum((s.faida_yake or 0 ) for s in sales_mwezi)
    matumizi_mwezi = sum((m.matumizi or 0) for m in mat_mwezi)

    jumla_faida = faida_kabla - matumizi_mwezi

    bidhaa = sum((s.kiasi or 0) for s in sales_mwezi)
    faida_mwaka = sum((s.faida_yake or 0) for s in sales_mwaka) - sum((m.matumizi or 0) for m in mat_mwaka)

    # GRAPH /  PROGRES YA KILASIKU
    progress_siku = []
    faida_kumulia = 0
    matumizi_kumulia = 0        
    bidhaa_kumulia = 0

    for siku in range(1, siku_za_mwezi + 1):
        mauzo_siku = [s for s in sales_mwezi if s.tarehe.day == siku]
        mat_list = [m for m in mat_mwezi if m.tarehe.day == siku]

        faida_siku = sum((s.faida_yake or 0) for s in mauzo_siku)
        bidhaa_siku = sum((s.kiasi or 0) for s in mauzo_siku)
        mat_siku = sum((m.matumizi or 0) for m in mat_list)
        
        faida_kumulia += faida_siku
        matumizi_kumulia += mat_siku
        bidhaa_kumulia += bidhaa_siku

        if siku <= leo_siku:
            jumla_hadi_siku = faida_kumulia - matumizi_kumulia
        else:
            jumla_hadi_siku = None
        

        progress_siku.append({
            'siku': siku,
            'faida_siku': faida_siku,
            'faida_total': faida_kumulia,
            'matumizi_siku': mat_siku,
            'matumizi_total': matumizi_kumulia,
            'bidhaa_siku': bidhaa_siku,
            'bidhaa_total': bidhaa_kumulia,
            'jumla': jumla_hadi_siku
        })
    jumla_zote = [p['jumla'] for p in progress_siku if p['jumla'] is not None]
    max_faida = max([abs(x) for x in jumla_zote]) if jumla_zote else 1
    if max_faida == 0:
        max_faida = 1 

    return render(request, 'stock/index.html',{
        'products': Product.objects.all(),
        'faida_yote': faida_kabla,
        'faida_baada': jumla_faida,
        'mauzo': len(sales_mwezi),
        'matumizi': matumizi_mwezi,
        'matumizi_mwezi': matumizi_mwezi,
        'bidhaa': bidhaa,
        'progress_siku': progress_siku,
        'mwaka_huu': mwaka_huu,
        'mwezi_huu': mwezi_huu,
        'mwezi_huu_jina': calendar.month_name[mwezi_huu],
        'leo_siku': leo_siku,
        'max_faida': max_faida,
        'mwaka_jana': mwaka_huu - 1,
        'mwaka_kesho': mwaka_huu + 1,
        'leo': leo,
        'is_boss': request.user.is_superuser,
        })       


@login_required
def ongeza_bidhaa(request):

    # kama sio admin asione
    if not request.user.is_superuser:
        return redirect('/')
    
    if request.method == 'POST':
        jina_input =request.POST.get('jina', '').strip()

        # angalia kamajia lipotayari.
        bidhaa_zilizopo = Product.objects.filter(jina__iexact=jina_input).first()

        if bidhaa_zilizopo:
            #Ipo tayari ongeza strok tu
            
            bidhaa_zilizopo.stock += int(request.POST.get('stock') or 0)
            bidhaa_zilizopo.bei_kununua = int(request.POST.get('bei_kununua') or 0)
            bidhaa_zilizopo.bei_kuuza = int(request.POST.get('bei_kuuza') or 0)
            bidhaa_zilizopo.barcode = request.POST.get('barcode', '')
            bidhaa_zilizopo.save()

        else:

            Product.objects.create(
                jina=request.POST.get('jina'),
                barcode=request.POST.get('barcode', ''),
                stock=int(request.POST.get('stock') or 0),
                bei_kununua=int(request.POST.get('bei_kununua') or 0),
                bei_kuuza=int(request.POST.get('bei_kuuza') or 0)
            )
        return redirect('/')
    return render(request, 'stock/add.html')


@login_required
def uza(request, id, kiasi=1):
    product = get_object_or_404(Product, id=id)
    try:
        kiasi = int(kiasi)
        
    except:
        kiasi = 1
    if kiasi <= 0:
        kiasi = 1

    if product.stock >= kiasi and product.stock > 0:
        product.stock -= kiasi
        product.save()
        Sale.objects.create(product=product, kiasi=kiasi, muuzaji=request.user)
    return redirect('/')


@login_required
def futa(request, id):
    if request.user.is_superuser:
        Product.objects.get(id=id).delete()
    return redirect('/')

def login_user(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('/')
        return render(request, 'stock/login.html', {'error': 'Login Imegoma!'})
    return render(request, 'stock/login.html')

def logout_user(request):
    logout(request)
    return redirect('/login/')


@login_required
def change_password(request):
    if request.method == 'POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        # Kuangalia kama password nimsahihi
        if not request.user.check_password(old_password):
            return render(request, 'stock/change_password.html', {'errror': 'Password ya zamani Si sahihi!'})

        if new_password != confirm_password:
            return render(request, 'stock/change_password.html', {'error': 'Password mpya hazifanani!'})

        if len(new_password) < 4:
            return render(request, 'stock/change_password.html', {'error': 'Password fupi sana! Weka angalau Herufi 4'})

        # Badilisha
        request.user.set_password(new_password)
        request.user.save()
        update_session_auth_hash(request, request.user) # Asi logout
        messages.success(request, 'Password imebadilishwa!')
        return redirect('/change_password/')
    return render(request, 'stock/change_password.html')


@login_required(login_url='/login/')
def user_list(request):
    #bosi aruhusiwe
    if not request.user.is_superuser:
        return redirect('/')

    #bosi aongeze user / muuzaji
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        if User.objects.filter(username=username).exists():
            error = f"Muuzaji '{username}' Tayari yupo! Chagua jinajingine"
        elif username and password:
            User.objects.create_user(username=username, password=password)
            return redirect('/users/')
        
    users = User.objects.all().order_by('id')
    return render(request, 'stock/users.html', {'users': users, 'error': error})

def futa_user(request, id):
    if not request.user.is_superuser:
        return redirect('/')
    # kama anajifuta mwenyewe
    if id == request.user.id:
        return redirect('/users/')

    User.objects.get(id=id).delete()
    return redirect('/users/')  

@login_required
def toa_faida(request):
    if request.method == 'POST':
        MatumiziYaFaida.objects.creat(
            matumizi =int(request.POST.get('kiasi')),
            maelezo = request.POST.get('maelezo'),
            aliyetoa=request.user
        )
    return redirect('/')

@login_required
def ripoti_mwaka(request, mwaka):
    # Itaonyesha miezi 12
    mwaka = int(mwaka)
    ripoti_miezi = []
    total_faida_yote = 0
    total_matumizi =  0
    total_baki = 0
    total_bidhaa = 0
    total_mauzo = 0

    sales_zote = list(Sale.objects.all())
    mat_zote = list(MatumiziYaFaida.objects.all())

    sales_mwaka = [s for s in sales_zote if s.tarehe.year == mwaka]
    mat_mwaka = [m for m in mat_zote if m.tarehe.year == mwaka]
    

    for m in range(1, 13):
        s_m = [s for s in sales_mwaka if s.tarehe.month == m]
        mat_m = [mt for mt in mat_mwaka if mt.tarehe.month == m]

        faida_m = sum((s.faida_yake or 0) for s in s_m)
        mat_m_sum = sum((x.matumizi or 0) for x in mat_m)
        baki_m = faida_m - mat_m_sum
        bidhaa_m = sum((s.kiasi or 0) for s in s_m)

        total_faida_yote += faida_m
        total_matumizi += mat_m_sum
        total_baki += baki_m
        total_bidhaa += bidhaa_m
        total_mauzo += len(s_m)

        ripoti_miezi.append({
            'mwezi': m,
            'jina': calendar.month_name[m],
            'faida_yote': faida_m,
            'matumizi': mat_m_sum,
            'baki': baki_m,
            'bidhaa': bidhaa_m,
            'mauzo': len(s_m),
            'faida': baki_m,
            'faida_kamili': baki_m,
        })

    return render(request, 'stock/ripoti_mwaka.html', {
        'mwaka': mwaka,
        'ripoti_miezi': ripoti_miezi,
        'faida_yote': total_faida_yote,
        'matumizi': total_matumizi,
        'matumizi_yote': total_matumizi,
        'baki': total_baki,
        'jumla_bidhaa': total_bidhaa,
        'bidhaa': total_bidhaa,
        'mauzo': total_mauzo,
        'jumla_faida_mwaka': total_baki,
        'jumla_bidhaa_mwaka': total_bidhaa,
        'mwaka_jana': mwaka - 1,
    })

# Kupunguza mapato 
@login_required
def toa_matumizi(request):
    if request.method == 'POST':
        try:
            kiasi = int(request.POST.get('matumizi', '0') or '0')
            maelezo = request.POST.get('maelezo', 'matumizi ya Biashara!')

            sales_zote = Sale.objects.all()
            faida_yote = sum((s.faida_yake or 0) for s in sales_zote)
            matumizi_yote = sum((m.matumizi or 0) for m in MatumiziYaFaida.objects.all())
            faida_baki = faida_yote - matumizi_yote

            # Validation
            if kiasi < 100:
                messages.error(request, f"X Kiasi {kiasi}Tsh Si sahihi!  Kiasi lazima kianzie 100Tsh.")
                return redirect('/')

            if kiasi > faida_baki:
                messages.error(request, f"X Huezi Kupunguza {kiasi}Tsh. Faida Baki ni {faida_baki}Tsh tu.")
                return redirect('/')

            # kama yote sawa toa
            MatumiziYaFaida.objects.create(
                matumizi=int(kiasi),
                maelezo=maelezo
            )
            messages.success(request, f" Umepunguza {kiasi}Tsh Umebakiwa na {faida_baki} kwenye faida yako!") 
        except ValueError:
            messages.error(request, f"X Weka namba sahihi!") 
    return redirect('/')           