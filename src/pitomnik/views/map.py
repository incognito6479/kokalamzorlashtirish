from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from config.settings.base import LOGIN_URL
from django.shortcuts import get_object_or_404
from regionroad.models import District, Region, RoadDistrict, Road
from django.core.paginator import Paginator
from ..forms import RoadAddForm

road_type = {
    "Маҳаллий": Road.RoadType.LOCAL,
    "Давлат": Road.RoadType.GOVERNMENT,
    "Халқаро": Road.RoadType.INTERNATIONAL,
}


@login_required(login_url=LOGIN_URL)
def index(request):
    context = {
        "section": "map",
        "organization": request.user.organization
    }
    return render(request, "index.html", context)


@login_required(login_url=LOGIN_URL)
def road_add(request):
    try:
        region = Region.objects.get(id=request.user.organization_id)
        obj = RoadDistrict.objects.get_planted_plants(region)
        if request.GET.get('search_input'):
            obj = RoadDistrict.objects.filter(road__title__contains=request.GET['search_input'], district_id__region_id=request.user.organization_id)
        paginator = Paginator(obj, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'organization': request.user.organization,
            'page_obj': page_obj,

        }
        return render(request, 'road_district/road_add.html', context)
    except:
        obj = RoadDistrict.objects.all()
        if request.GET.get('search_input'):
            obj = RoadDistrict.objects.filter(road__title__contains=request.GET['search_input'])
        paginator = Paginator(obj, 25)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {
            'organization': request.user.organization,
            'page_obj': page_obj,

        }
        return render(request, 'road_district/road_add.html', context)


@login_required(login_url=LOGIN_URL)
def road_add_form(request):
    f = RoadAddForm()
    if request.method == 'POST':
        try:
            district = District.objects.get(
                name=request.POST['district'],
            )
            road_slice = request.POST['road_slice'].split("-")
            road_from = road_slice[0].split(",")[0]
            road_to = road_slice[1]
            if district:
                road, create = Road.objects.get_or_create(
                    code=request.POST['road_code'],
                    title=request.POST['road'],
                    road_type=road_type[request.POST['road_type']],
                )
                road.save()
                RoadDistrict.objects.get_or_create(
                    road=road,
                    district=district,
                    defaults={
                        "road_from": road_from,
                        "road_to": road_to,
                        "requirement": round(
                            float(road_to) - float(road_from), 2
                        ),
                    },
                )
        except District.DoesNotExist:
            print(request.POST['district'])
            return redirect('pitomnik:road_add_form')
        return redirect('pitomnik:road_add')
    context = {
        'form': f
    }
    return render(request, 'road_district/road_add_form.html', context)


@login_required(login_url=LOGIN_URL)
def road_delete(request, pk):
    try:
        road_del = RoadDistrict.objects.get(id=pk)
        road_del.delete()
        return redirect('pitomnik:road_add')
    except:
        print('ERROR')
        return redirect('pitomnik:road_add')


@login_required(login_url=LOGIN_URL)
def road_change(request, pk):
    roaddistrict = RoadDistrict.objects.get(id=pk)
    road_info = Road.objects.get(id=roaddistrict.road_id)
    district_info = District.objects.get(id=roaddistrict.district_id)
    road_slice = str(roaddistrict.road_from) + '-' + str(roaddistrict.road_to)
    district_name_choices = District.objects.values_list('name', flat=True)
    if request.method == 'POST':
        road_slice = request.POST['road_slice'].split("-")
        road_from = road_slice[0].split(",")[0]
        road_to = road_slice[1]
        road_info.code = request.POST['road_code']
        road_info.title = request.POST['road']
        road_info.road_type = road_type[request.POST['road_type']]
        road_info.save()
        district_info.name = request.POST['district']
        district_info.save()
        roaddistrict.road_to = road_to
        roaddistrict.road_from = road_from
        roaddistrict.save()
        return redirect('pitomnik:road_add')
    context = {
        'pk': pk,
        'road_info': road_info,
        'district_info': district_info,
        'road_slice': road_slice,
        'district_name_choices': district_name_choices,
    }
    return render(request, 'road_district/road_add_change.html', context)
