from django import forms
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import (
    HTML,
    TEMPLATE_PACK,
    ButtonHolder,
    Div,
    Field,
    Fieldset,
    Layout,
    LayoutObject,
    Submit,
)

from regionroad.models import District, Region, RoadDistrict

from .models import (
    Irrigation,
    IrrigationImage,
    LandScapeJob,
    LandScapeJobImage,
    NewIrrigation,
    NewIrrigationImage,
    Pitomnik,
    PitomnikImage,
    PitomnikPlantImage,
    PitomnikPlants,
    PitomnikSavingJob,
    PitomnikSavingJobImage,
    Plant,
    PlantedPlantImage,
    PlantedPlants,
    SavingJob,
    SavingjobImage,
)


class BaseFormSet(forms.ModelForm):
    region = forms.ModelChoiceField(queryset=Region.objects.all())
    district = forms.ModelChoiceField(queryset=District.objects.none())
    road_district = forms.ModelChoiceField(
        queryset=RoadDistrict.objects.none()
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["region"].label = "Вилоят"
        self.fields["district"].label = "Туманлар"
        self.fields["road_district"].label = "Йул номи"
        self._set_district()
        self._set_road()

    def _set_district(self):
        region_id = None
        if "region" in self.data:
            try:
                region_id = int(self.data.get("region"))
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            region_id = self.instance.road_district.district.region_id
        if region_id:
            self.fields["district"].queryset = District.objects.filter(
                region_id=region_id
            )

    def _set_road(self):
        district_id = None
        if "district" in self.data:
            try:
                district_id = int(self.data.get("district"))
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            district_id = self.instance.road_district.district_id
        if district_id:
            self.fields[
                "road_district"
            ].queryset = RoadDistrict.objects.filter_by_district(district_id)


class UpdateBaseFormSet(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["region"].initial = Region.objects.get(
            id=self.instance.road_district.district.region_id
        )
        self.fields["district"].initial = District.objects.get(
            id=self.instance.road_district.district_id
        )


class Formset(LayoutObject):
    template = "pitomnik/images/formset.html"

    def __init__(self, formset_name_in_context, template=None):
        self.formset_name_in_context = formset_name_in_context
        self.fields = []
        if template:
            self.template = template

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK):
        formset = context[self.formset_name_in_context]
        return render_to_string(self.template, {"formset": formset})


class PitomnikForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_helper()

    def _set_helper(self):
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3 create-label"
        self.helper.field_class = "col-md-9"
        self.helper.attrs = {"enctype": "multipart/form-data"}
        self.helper.layout = Layout(
            Div(
                Field("name"),
                Field("address"),
                Field("area"),
                Field("kontr"),
                Fieldset(
                    "Расм юклаш", Formset("images"), css_class="form-row"
                ),
                HTML("<br>"),
                Div(
                    ButtonHolder(Submit("submit", "Сақлаш")),
                    css_class="float-right",
                ),
                HTML(
                    f"<a href='{reverse_lazy('pitomnik:pitomnik:list')}' "
                    f"class='btn btn-secondary float-right mr-2'>Орқага</a>"
                ),
            )
        )

    class Meta:
        model = Pitomnik
        fields = ["name", "address", "area", "kontr"]
        labels = {
            "name": _("Номи"),
            "address": _("Манзил"),
            "area": _("Майдон"),
            "kontr": _("Контр"),
        }


class ImageForm(forms.ModelForm):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "inputfile"}),
    )


class PitomnikImageForm(ImageForm):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "inputfile"}),
    )

    class Meta:
        model = PitomnikImage
        exclude = ()


PitomnikImageFormSet = inlineformset_factory(
    Pitomnik,
    PitomnikImage,
    form=PitomnikImageForm,
    fields=("image",),
    min_num=1,
    max_num=20,
    extra=0,
    can_delete=True,
)


class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ("name", "type")
        labels = {
            "name": _("Номи"),
            "type": _("Ўсимлик тури"),
        }


class PitomnikPlantForm(forms.ModelForm):
    pitomnik = forms.ModelChoiceField(queryset=None, label=_("Питомник"))
    readiness_date = forms.DateField(
        required=True,
        label=_("Тахминий тайёр бўлиш санаси"),
    )

    class Meta:
        model = PitomnikPlants
        fields = (
            "pitomnik",
            "plant",
            "quantity",
            "plant_type",
            "plant_field",
            "planted_date",
            "readiness_date",
        )
        labels = {
            "plant": _("Ўсимлик"),
            "quantity": _("Миқдори"),
            "plant_type": _("Ўсимлик тури"),
            "plant_field": _("Майдон"),
            "planted_date": _("Экилган санаси"),
        }

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_form_helper()
        self.fields[
            "pitomnik"
        ].queryset = Pitomnik.objects.filter_by_organization_or_all(user)
        self.added_by = user

    def clean(self):
        self.instance.action_type = PitomnikPlants.ActionTYPE.IMPORT
        return self.cleaned_data

    def _set_form_helper(self):
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3 create-label"
        self.helper.field_class = "col-md-9"
        self.helper.attrs = {"enctype": "multipart/form-data"}
        self.helper.layout = Layout(
            Div(
                Field("pitomnik"),
                Field("plant"),
                Field("quantity"),
                Field("plant_type"),
                Field("plant_field"),
                Field("planted_date"),
                Field("readiness_date"),
                Fieldset(
                    "Add images", Formset("images"), css_class="form-row"
                ),
                HTML("<br>"),
                Div(
                    ButtonHolder(Submit("submit", "Сақлаш")),
                    css_class="float-right",
                ),
                HTML(
                    f"<a href='{reverse_lazy('pitomnik:pitomnikplants:list')}'"
                    f"class='btn btn-secondary float-right mr-2'>Орқага</a>"
                ),
            )
        )


class PitomnikPlantImageForm(ImageForm):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "inputfile"}),
    )

    class Meta:
        model = PitomnikPlantImage
        exclude = ()


PitomnikPlantImageFormSet = inlineformset_factory(
    PitomnikPlants,
    PitomnikPlantImage,
    form=PitomnikPlantImageForm,
    fields=("image",),
    min_num=1,
    max_num=20,
    extra=0,
    can_delete=True,
)


class PlantedPlantForm(BaseFormSet):
    error_messages = {
        "quantity_exceeded": _("Танланган ўсимликдан йетарлича йўқ"),
    }
    pitomnik = forms.ModelChoiceField(
        queryset=None,
        required=False,
        widget=forms.Select(attrs={"style": "width: 100%"}),
    )
    plant = forms.ModelChoiceField(queryset=Plant.objects.none())

    class Meta:
        model = PlantedPlants
        fields = (
            "plant_source",
            "quantity",
            "road_district",
            "road_from",
            "road_to",
            "metr",
            "planting_side",
            "planted_date",
        )

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        self.fields["region"].initial = Region.objects.get(
            id=self.user.organization.region_id
        )
        self._set_labels()
        self.fields[
            "pitomnik"
        ].queryset = Pitomnik.objects.filter_by_organization(user.organization)
        if "plant" in self.data:
            self.fields["plant"].queryset = Plant.objects.filter(
                id=self.data.get("plant")
            )

        self._set_form_helper()

    def _set_labels(self):
        self.fields["plant_source"].label = "Манба"
        self.fields["pitomnik"].label = "Питомник"
        self.fields["plant"].label = "Ўсимлик"
        self.fields["quantity"].label = "Экилди (дона)"
        self.fields["road_from"].label = "Км дан"
        self.fields["road_to"].label = "Км гача"
        self.fields["metr"].label = "Экилган Майдони"
        self.fields["planting_side"].label = "Йўл тарафи"
        self.fields["planted_date"].label = "Экилган санаси"
        self.fields["metr"].label = "Экилган Масофаси (metr)"

    def _set_form_helper(self):
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3 create-label"
        self.helper.field_class = "col-md-9"
        self.helper.attrs = {"enctype": "multipart/form-data"}
        self.helper.layout = Layout(
            Div(
                Field("plant_source"),
                Field("pitomnik"),
                Field("plant"),
                Field("quantity"),
                Field("region"),
                Field("district"),
                Field("road_district"),
                Field("road_from"),
                Field("road_to"),
                Field("metr"),
                Field("planting_side"),
                Field("planted_date"),
                Fieldset(
                    "Add images", Formset("images"), css_class="form-row"
                ),
                HTML("<br>"),
                Div(
                    ButtonHolder(Submit("submit", "Сақлаш")),
                    css_class="float-right",
                ),
                HTML(
                    f"<a href='{reverse_lazy('pitomnik:plantedplants:list')}' "
                    f"class='btn btn-secondary float-right mr-2'>Орқага</a>"
                ),
            )
        )

    def _validate_quantity(self):
        quantity = self.cleaned_data["quantity"]
        pitomnik = self.cleaned_data['pitomnik']
        if self.cleaned_data["pitomnik"]:
            pitomnik_plant = PitomnikPlants.objects.get_plant_total_quantity(
                pitomnik=self.cleaned_data["pitomnik"],
                plant=self.cleaned_data["plant"],
            )

            if quantity > pitomnik_plant.get("total_quantity"):
                raise ValidationError(
                    self.error_messages["quantity_exceeded"],
                    code="quantity_exceed",
                )
            # PitomnikPlants.objects.create_export(
            #     pitomnik=self.cleaned_data["pitomnik"],
            #     plant=self.cleaned_data["plant"],
            #     quantity=self.cleaned_data["quantity"],
            #     user=self.user,
            # )
            if not self.data['images-0-planted_plant']:
                PitomnikPlants.objects.create_export(
                    pitomnik=self.cleaned_data["pitomnik"],
                    plant=self.cleaned_data["plant"],
                    quantity=self.cleaned_data["quantity"],
                    user=self.user,
                )
            else:
                x = PlantedPlants.objects.get(id=int(self.data['images-0-planted_plant']))
                PitomnikPlants.objects.create_import(
                    pitomnik=self.cleaned_data["pitomnik"],
                    plant=self.cleaned_data["plant"],
                    quantity=(x.quantity - quantity),
                    user=self.user,
                )
        return quantity

    def clean(self):
        self._validate_quantity()
        self.instance.pitomnik = self.cleaned_data["pitomnik"]
        self.instance.plant = self.cleaned_data["plant"]
        return self.cleaned_data




class PlantedPlantImageForm(ImageForm):
    class Meta:
        model = PlantedPlantImage
        exclude = ()


PlantedPlantImageFormSet = inlineformset_factory(
    PlantedPlants,
    PlantedPlantImage,
    form=PlantedPlantImageForm,
    fields=("image",),
    min_num=1,
    max_num=20,
    extra=0,
    can_delete=True,
)


class CreateIrrigationForm(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_helper()

    def _set_helper(self):
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3 create-label"
        self.helper.field_class = "col-md-9"
        self.helper.attrs = {"enctype": "multipart/form-data"}
        self.helper.layout = Layout(
            Div(
                Field("region"),
                Field("district"),
                Field("road_district"),
                Field("irrigation_type"),
                Field("road_slice"),
                Field("tree_quantity"),
                Field("length"),
                Fieldset(
                    "Расм юклаш", Formset("images"), css_class="form-row"
                ),
                HTML("<br>"),
                Div(
                    ButtonHolder(Submit("submit", "Сақлаш")),
                    css_class="float-right",
                ),
                HTML(
                    f"<a href='{reverse_lazy('pitomnik:irrigation:list')}' "
                    f"class='btn btn-secondary float-right mr-2'>Орқага</a>"
                ),
            )
        )

    class Meta:
        model = Irrigation
        fields = [
            "region",
            "district",
            "road_district",
            "irrigation_type",
            "road_slice",
            "tree_quantity",
            "length",
        ]
        labels = {
            "irrigation_type": _("Суғориш тури"),
            "road_slice": _("Манзили"),
            "tree_quantity": _("Дарахтлар (дона)"),
            "length": _("Узунлиги (км)"),
        }


class IrrigationImageForm(ImageForm):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "inputfile"}),
    )

    class Meta:
        model = Irrigation
        exclude = ()


IrrigationImageFormSet = inlineformset_factory(
    Irrigation,
    IrrigationImage,
    form=IrrigationImageForm,
    fields=("image",),
    min_num=1,
    max_num=20,
    extra=0,
    can_delete=True,
)


class UpdateIrrigationForm(CreateIrrigationForm, UpdateBaseFormSet):
    pass


class CreateSavingJobForm(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_helper()

    def _set_helper(self):
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3 create-label"
        self.helper.field_class = "col-md-9"
        self.helper.attrs = {"enctype": "multipart/form-data"}
        self.helper.layout = Layout(
            Div(
                Field("region"),
                Field("district"),
                Field("road_district"),
                Field("road_from"),
                Field("road_to"),
                Field("dig_quantity"),
                Field("dig_len"),
                Field("organic_quantity"),
                Field("organic_len"),
                Field("workers_quantity"),
                Field("technique_quantity"),
                Fieldset(
                    "Расм юклаш", Formset("images"), css_class="form-row"
                ),
                HTML("<br>"),
                Div(
                    ButtonHolder(Submit("submit", "Сақлаш")),
                    css_class="float-right",
                ),
                HTML(
                    f"<a href='{reverse_lazy('pitomnik:savingjob:list')}' "
                    f"class='btn btn-secondary float-right mr-2'>Орқага</a>"
                ),
            )
        )

    class Meta:
        model = SavingJob
        fields = [
            "region",
            "district",
            "road_district",
            "road_from",
            "road_to",
            "dig_quantity",
            "dig_len",
            "organic_quantity",
            "organic_len",
            "workers_quantity",
            "technique_quantity",
        ]
        labels = {
            "road_from": _("Км дан"),
            "road_to": _("Км гача"),
            "dig_quantity": _("Дарахтлар (чопик) сони"),
            "dig_len": _("Дарахтлар (чопик) узунлиги км"),
            "length": _("Узунлиги"),
            "organic_quantity": _("Агрокимёвий ишлар(дона)"),
            "organic_len": _("Агрокимёвий ишлар(км)"),
            "workers_quantity": _("Ишчилар сони"),
            "technique_quantity": _("Техника сони"),
        }


class SavingJobImageForm(ImageForm):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "inputfile"}),
    )

    class Meta:
        model = SavingJob
        exclude = ()


SavingJobImageFormSet = inlineformset_factory(
    SavingJob,
    SavingjobImage,
    form=SavingJobImageForm,
    fields=("image",),
    min_num=1,
    max_num=20,
    extra=0,
    can_delete=True,
)


class UpdateSavingJobForm(CreateSavingJobForm, UpdateBaseFormSet):
    pass


class CreateLandScapeJobForm(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_helper()

    def _set_helper(self):
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3 create-label"
        self.helper.field_class = "col-md-9"
        self.helper.attrs = {"enctype": "multipart/form-data"}
        self.helper.layout = Layout(
            Div(
                Field("region"),
                Field("district"),
                Field("road_district"),
                Field("road_slice"),
                Field("round_quantity"),
                Field("round_area"),
                Field("cross_quantity"),
                Field("cross_area"),
                Field("panno_quantity"),
                Field("road_side_length"),
                Fieldset(
                    "Расм юклаш", Formset("images"), css_class="form-row"
                ),
                HTML("<br>"),
                Div(
                    ButtonHolder(Submit("submit", "Сақлаш")),
                    css_class="float-right",
                ),
                HTML(
                    f"<a href='{reverse_lazy('pitomnik:landscapejob:list')}' "
                    f"class='btn btn-secondary float-right mr-2'>Орқага</a>"
                ),
            )
        )

    class Meta:
        model = LandScapeJob
        fields = [
            "region",
            "district",
            "road_district",
            "road_slice",
            "round_quantity",
            "round_area",
            "cross_quantity",
            "cross_area",
            "panno_quantity",
            "road_side_length",
        ]
        labels = {
            "road_slice": _("Йўл узунлиги (км)"),
            "round_quantity": _("Айлана (дона)"),
            "round_area": _("Айлана юзаси (м2)"),
            "cross_quantity": _("Йул ўтказгич ва чорраха (дона)"),
            "cross_area": _("Йул ўтказгич ва чорраха (м2)"),
            "panno_quantity": _("Панно ва степло (дона)"),
            "road_side_length": _("Йўл ёкалари (км)"),
        }


class LandScapeJobImageForm(ImageForm):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "inputfile"}),
    )

    class Meta:
        model = LandScapeJob
        exclude = ()


LandScapeJobImageFormSet = inlineformset_factory(
    LandScapeJob,
    LandScapeJobImage,
    form=LandScapeJobImageForm,
    fields=("image",),
    min_num=1,
    max_num=20,
    extra=0,
    can_delete=True,
)


class UpdateLandScapeJobForm(CreateLandScapeJobForm, UpdateBaseFormSet):
    pass


class CreateNewIrrigationForm(BaseFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_helper()

    def _set_helper(self):
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3 create-label"
        self.helper.field_class = "col-md-9"
        self.helper.attrs = {"enctype": "multipart/form-data"}
        self.helper.layout = Layout(
            Div(
                Field("region"),
                Field("district"),
                Field("road_district"),
                Field("road_from"),
                Field("road_to"),
                Field("artesian_well"),
                Field("drop"),
                Field("rain"),
                Fieldset(
                    "Расм юклаш", Formset("images"), css_class="form-row"
                ),
                HTML("<br>"),
                Div(
                    ButtonHolder(Submit("submit", "Сақлаш")),
                    css_class="float-right",
                ),
                HTML(
                    f"<a href='{reverse_lazy('pitomnik:newirrigation:list')}' "
                    f"class='btn btn-secondary float-right mr-2'>Орқага</a>"
                ),
            )
        )

    class Meta:
        model = NewIrrigation
        fields = [
            "region",
            "district",
            "road_district",
            "road_from",
            "road_to",
            "artesian_well",
            "drop",
            "rain",
        ]
        labels = {
            "road_from": _("Км дан"),
            "road_to": _("Км гача"),
            "artesian_well": _("Артезиан қудуқ дона"),
            "drop": _("Томчилатиб км"),
            "rain": _("Ёмғирлатиб км"),
        }


class NewIrrigationImageForm(ImageForm):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "inputfile"}),
    )

    class Meta:
        model = NewIrrigation
        exclude = ()


NewIrrigationImageFormSet = inlineformset_factory(
    NewIrrigation,
    NewIrrigationImage,
    form=NewIrrigationImageForm,
    fields=("image",),
    min_num=1,
    max_num=20,
    extra=0,
    can_delete=True,
)


class UpdateNewIrrigationForm(CreateNewIrrigationForm, UpdateBaseFormSet):
    pass


class PitomnikSavingJobForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            "pitomnik"
        ].queryset = Pitomnik.objects.filter_by_organization(user.organization)
        self.added_by = user
        self._set_helper()

    def _set_helper(self):
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = "form-horizontal"
        self.helper.label_class = "col-md-3 create-label"
        self.helper.field_class = "col-md-9"
        self.helper.attrs = {"enctype": "multipart/form-data"}
        self.helper.layout = Layout(
            Div(
                Field("pitomnik"),
                Field("plants"),
                Field("total_plants"),
                Field("planted_area"),
                Field("agrotechnical_measures"),
                Field("mineral"),
                Field("organic"),
                Field("workers"),
                Field("technique"),
                Fieldset(
                    "Расм юклаш", Formset("images"), css_class="form-row"
                ),
                HTML("<br>"),
                Div(
                    ButtonHolder(Submit("submit", "Сақлаш")),
                    css_class="float-right",
                ),
                HTML(
                    f"<a href="
                    f"'{reverse_lazy('pitomnik:pitomniksavingjob:list')}' "
                    f"class='btn btn-secondary float-right mr-2'>Орқага</a>"
                ),
            )
        )

    class Meta:
        model = PitomnikSavingJob
        fields = "__all__"
        labels = {
            "pitomnik": _("Питомник"),
            "plants": _("Ўсимликлар"),
            "total_plants": _("Жами кўчатлар сони"),
            "planted_area": _("Экилган майдон"),
            "agrotechnical_measures": _("Агротехник тадбирлар"),
            "mineral": _("Минерал"),
            "organic": _("Органик"),
            "workers": _("Ишчилар"),
            "technique": _("Техника"),
        }


class PitomnikSavingJobImageForm(ImageForm):
    image = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "inputfile"}),
    )

    class Meta:
        model = PitomnikSavingJobImage
        exclude = ()


PitomnikSavingJobImageFormSet = inlineformset_factory(
    PitomnikSavingJob,
    PitomnikSavingJobImage,
    form=PitomnikSavingJobImageForm,
    fields=("image",),
    min_num=1,
    max_num=20,
    extra=0,
    can_delete=True,
)

road_type_choice = (
    ("Халқаро", _('Халқаро')),
    ("Давлат", _('Давлат')),
    ("Маҳаллий", _('Маҳаллий'))
)


class RoadAddForm(forms.Form):
    road_code = forms.CharField(
        max_length=500,
        label="Йўл коди",
        widget=forms.TextInput(attrs={'placeholder': '4P-A2 25'}))
    road = forms.CharField(
        max_length=1000,
        label="Йўл номи",
        widget=forms.TextInput(attrs={'placeholder': 'Oqtepa 35'}))
    road_slice = forms.CharField(
        max_length=200,
        label="Йўл қисми",
        widget=forms.TextInput(attrs={'placeholder': '0-25'}))
    road_type = forms.ChoiceField(
        choices=road_type_choice,
        label="Йўл тури", initial='',
        widget=forms.Select(), required=True)
    district = forms.ModelChoiceField(
        queryset=District.objects.values_list('name', flat=True),
        label="Туман/Шаҳар номи")

