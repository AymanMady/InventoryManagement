from django.shortcuts import render, redirect, HttpResponse
from accounts.models import Materiel,Employee,Etablissement,Emplacement,Affectation
from .forms import materielForm,employeForm,etablissementForm,emplacementForm,affectationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Count , Q
from django.template import loader
from xhtml2pdf import pisa



@login_required(login_url='login')
def homePage(request):
    establishments = Etablissement.objects.all()

    establishment_data = []
    for establishment in establishments:
        total_materials = Materiel.objects.count()
        establishment_materials = Materiel.objects.filter(
            affectation__id_emplacement__id_etablissement=establishment).count()
        if total_materials > 0:
            percentage = (establishment_materials / total_materials) * 100
        else:
            percentage = 0

        establishment_data.append({
            'establishment': establishment,
            'percentage': percentage,
        })


    bon_etat_count = Materiel.objects.filter(etat='Bon etat').count()
    hs_count = Materiel.objects.filter(etat='HS').count()
    neuve_count = Materiel.objects.filter(etat='Neuve').count()


    materiel_count = Materiel.objects.filter().count()
    emplacement_count = Emplacement.objects.filter().count()
    employees_count = Employee.objects.filter().count()

    context = {
        'bon_etat_count': bon_etat_count,
        'hs_count': hs_count,
        'neuve_count': neuve_count,
        'establishment_data': establishment_data,
        'total_materiel' : materiel_count,
        'total_emplacement': emplacement_count,
        'total_employees': employees_count,
        'navbar':'home',
    }

    return render(request, 'home.html', context)


# Statistiques

def statistique(request):
    all_etablissement = Etablissement.objects.all()
    return render(request, 'statistiques.html',{'etablissements':all_etablissement})

def show_statistiques(request):
    if request.method == 'POST':
        etablissement_id = request.POST.get('id_etablissement')
        selected_etablissement = Etablissement.objects.get(id=etablissement_id)

        total_all_materiel = Materiel.objects.count()
        total_affectations = Affectation.objects.filter(id_emplacement__id_etablissement=selected_etablissement).count()

        total_materiel = Affectation.objects.filter(id_emplacement__id_etablissement=selected_etablissement).count()
        total_employees = Employee.objects.filter(emplacement__id_etablissement=selected_etablissement).count()
        total_emplacement = Emplacement.objects.filter(id_etablissement=selected_etablissement).count()

        bon_etat_count = Affectation.objects.filter(
            id_materiel__etat='Bon etat', id_emplacement__id_etablissement=selected_etablissement
        ).count()
        hs_count = Affectation.objects.filter(
            id_materiel__etat='HS', id_emplacement__id_etablissement=selected_etablissement
        ).count()
        neuve_count = Affectation.objects.filter(
            id_materiel__etat='Neuve', id_emplacement__id_etablissement=selected_etablissement
        ).count()

        emplacement_data = Emplacement.objects.filter(id_etablissement=selected_etablissement).annotate(
        percentage=Count('affectation__id_materiel') * 100 / total_all_materiel,
        bon_etat_percentage = Count('affectation__id_materiel',filter=Q(affectation__id_materiel__etat='Bon etat')) * 100 / total_affectations,
        hs_percentage = Count('affectation__id_materiel',filter=Q(affectation__id_materiel__etat='HS')) * 100 / total_affectations,
        neuve_percentage = Count('affectation__id_materiel',filter=Q(affectation__id_materiel__etat='Neuve')) * 100 / total_affectations,
        ).values('designation', 'percentage').order_by('designation')

        return render(request, 'show_statistiques.html', {
            'total_materiel': total_materiel,
            'total_employees': total_employees,
            'total_emplacement': total_emplacement,
            'bon_etat_count': bon_etat_count,
            'hs_count': hs_count,
            'neuve_count': neuve_count,
            'emplacement_data': emplacement_data,
        'etablissements': selected_etablissement,

        })



# Materiels
@login_required(login_url='login')

def materiel(request):
    id_etablissement = request.POST.get('id_etablissement')
    id_emplacement = request.POST.get('id_emplacement')
    all_etablissement = Etablissement.objects.all()
    all_emplacement = Emplacement.objects.all()
    materiels = Materiel.objects.all()

    if id_etablissement or id_emplacement:
        if id_etablissement:
            materiels = materiels.filter(affectation__id_emplacement__id_etablissement_id=id_etablissement)
        if id_emplacement:
            materiels = materiels.filter(affectation__id_emplacement_id=id_emplacement)

    for materiel in materiels:
        affectations = Affectation.objects.filter(id_materiel=materiel)
        emplacements = [affectation.id_emplacement.designation for affectation in affectations]
        materiel.emplacements = emplacements

    context = {
        "materiels": materiels,
        "emplacements": all_emplacement,
        "etablissements": all_etablissement,
        "navbar": 'materiel',
    }

    return render(request, "materiels/index.html", context)

def load_form_materiel(request):
    form = materielForm()
    return render(request, "materiels/add.html",{'form':form,"navbar":'materiel'})
def add_materiel(request):
    form = materielForm(request.POST)
    form.save()
    return redirect('materiel')
def edit_materiel(request, id):
    materiel = Materiel.objects.get(id=id)
    return render(request,'materiels/edit.html',{'materiel':materiel,"navbar":'materiel'})
def update_materiel(request, id):
    materiel = Materiel.objects.get(id=id)
    form = materielForm(request.POST, instance=materiel)
    form.save()
    return redirect('materiel')
def delete_materiel(request, id):
    materiel = Materiel.objects.get(id=id)
    materiel.delete()
    return redirect('materiel')


# Affectation
@login_required(login_url='login')

def affectation(request):
    all_affectation = Affectation.objects.all()
    return render(request,"affectations/index.html",{"affectations": all_affectation,"navbar":'affectation'})

def load_form_affectation(request):
    all_materiel = Materiel.objects.all()
    all_emplacement = Emplacement.objects.all()
    form = affectationForm()
    return render(request, "affectations/add.html",{'form':form,"navbar":'affectation','materiels':all_materiel,'emplacements':all_emplacement})
def add_affectation(request):
    form = affectationForm(request.POST)
    form.save()
    return redirect('affectation')
def edit_affectation(request, id):
    all_materiel = Materiel.objects.all()
    all_emplacement = Emplacement.objects.all()
    affectation = Affectation.objects.get(id=id)
    form = affectationForm()
    return render(request,'affectations/edit.html',{'form':form,'affectation':affectation,"navbar":'affectation','materiels':all_materiel,'emplacements':all_emplacement})
def update_affectation(request, id):
    affectation = Affectation.objects.get(id=id)
    form = affectationForm(request.POST, instance=affectation)
    form.save()
    return redirect('affectation')
def delete_affectation(request, id):
    affectation = Affectation.objects.get(id=id)
    affectation.delete()
    return redirect('affectation')




# Employees
@login_required(login_url='login')

def employe(request):
    all_employe= Employee.objects.all()
    return render(request,"employees/index.html",{"employes": all_employe,"navbar":'employe'})


def load_form_employe(request):
    form = employeForm()
    return render(request, "employees/add.html",{'form':form,"navbar":'employe'})
def add_employe(request):
    form = employeForm(request.POST)
    form.save()
    return redirect('employe')
def edit_employe(request, id):
    employe = Employee.objects.get(id=id)
    form = employeForm()
    return render(request,'employees/edit.html',{'employe':employe,"navbar":'employe','form':form})
def update_employe(request, id):
    employe = Employee.objects.get(id=id)
    form = employeForm(request.POST, instance=employe)
    form.save()
    return redirect('employe')
def delete_employe(request, id):
    employe = Employee.objects.get(id=id)
    employe.delete()
    return redirect('employe')


# Etablissement
@login_required(login_url='login')

def etablissement(request):
    all_etablissement= Etablissement.objects.all()
    return render(request,"etablissements/index.html",{"etablissements": all_etablissement,"navbar":'etablissement'})

def load_form_etablissement(request):
    form = etablissementForm()
    return render(request, "etablissements/add.html",{'form':form,"navbar":'etablissement'})
def add_etablissement(request):
    form = etablissementForm(request.POST)
    form.save()
    return redirect('etablissement')
def edit_etablissement(request, id):
    etablissement = Etablissement.objects.get(id=id)
    return render(request,'etablissements/edit.html',{'etablissement':etablissement,"navbar":'etablissement'})
def update_etablissement(request, id):
    etablissement = Etablissement.objects.get(id=id)
    form = etablissementForm(request.POST, instance=etablissement)
    form.save()
    return redirect('etablissement')
def delete_etablissement(request, id):
    etablissement = Etablissement.objects.get(id=id)
    etablissement.delete()
    return redirect('etablissement')

def show_etablissement(request, id):
    etablissements = Etablissement.objects.get(id=id)
    emplacements = Emplacement.objects.filter(id_etablissement=etablissements)
    materiels = Affectation.objects.filter(id_emplacement__id_etablissement=etablissements).select_related('id_materiel')

    return render(request, 'etablissements/show.html', {
        'etablissements': etablissements,
        'navbar': 'etablissement',
        'emplacements': emplacements,
        'materiels': materiels,
    })

# Emplacement
@login_required(login_url='login')

def emplacement(request):
    emplacements = Emplacement.objects.all()
    all_etablisement= Etablissement.objects.all()
    id_etablissement = request.POST.get('id_etablissement')
    if id_etablissement:
            emplacements = emplacements.filter(affectation__id_emplacement__id_etablissement_id=id_etablissement)


    return render(request,"emplacements/index.html",{"emplacements": emplacements,"navbar":'emplacement',"etablissements":all_etablisement})

def load_form_emplacement(request):
    all_employe = Employee.objects.all()
    all_etablissement = Etablissement.objects.all()
    form = emplacementForm()
    return render(request, "emplacements/add.html",{'form':form,"navbar":'emplacement','employes':all_employe,'etablissements':all_etablissement})
def add_emplacement(request):
    form = emplacementForm(request.POST)
    form.save()
    return redirect('emplacement')
def edit_emplacement(request, id):
    all_employe = Employee.objects.all()
    all_etablissement = Etablissement.objects.all()
    emplacement = Emplacement.objects.get(id=id)
    form = emplacementForm()
    return render(request,'emplacements/edit.html',{'form':form,'emplacement':emplacement,"navbar":'emplacement','employes':all_employe,'etablissements':all_etablissement})
def update_emplacement(request, id):
    emplacement = Emplacement.objects.get(id=id)
    form = emplacementForm(request.POST, instance=emplacement)
    form.save()
    return redirect('emplacement')
def delete_emplacement(request, id):
    emplacement = Emplacement.objects.get(id=id)
    emplacement.delete()
    return redirect('emplacement')

def materiel_emplacment(request, id):
    emplacement = Emplacement.objects.get(id=id)
    materiels = Materiel.objects.all()
    materiels = materiels.filter(affectation__id_emplacement_id=emplacement)
    return render(request,'emplacements/materiel_emplacment.html',{'emplacement':emplacement,'materiels':materiels})



def materiel_emplacment(request, id):
    emplacement = Emplacement.objects.get(id=id)
    materiels = Materiel.objects.all()
    materiels = materiels.filter(affectation__id_emplacement_id=emplacement)
    # Supposons que vous ayez des données à passer au template
    data = {'emplacement':emplacement,'materiels':materiels}

    # Chargez le template à l'aide du moteur de template
    template = loader.get_template('emplacements/materiel_emplacment.html')

    # Rendez les données dans le template en utilisant le contexte
    rendered_template = template.render(data, request)

    # Utilisez xhtml2pdf pour générer le PDF à partir du contenu rendu
    pdf_output = pisa.CreatePDF(rendered_template)

    if not pdf_output.err:
        # Créez une réponse HttpResponse avec le contenu PDF généré
        response = HttpResponse(pdf_output.dest.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename="list_materiels.pdf"'  # Nom du fichier de téléchargement
        return response

    return HttpResponse('Erreur lors de la génération du PDF.', status=500)
