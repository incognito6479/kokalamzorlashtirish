from django.contrib.auth.models import ContentType, Group, Permission


def get_add_permission(perm, group):
    perm = Permission.objects.get(codename=perm)
    group.permissions.add(perm)


def create_permission_for_content(app_label):
    content_type_admin = ContentType.objects.filter(app_label=app_label)
    for content in content_type_admin:
        perm, exists = Permission.objects.get_or_create(
            name=f"View {content.model} for Admin",
            content_type=content,
            codename=f"view_{content.model}_admin",
        )
        perm.save()


group_names = {
    "PITOMNIK": "Манзарали ўсимликлар питомникларини "
    "мувофиқлаштириш бошқармаси",
    "VEHICLE": "Моддий-техник таъминот ва шартномалар бўлими",
    "PRODUCTION": "Ишлаб-чиқариш техник бўлими",
    "ACCOUNTING": "Бухгалтерия хисоби ва хисоботи бўлими",
    "FINANCE": "Молия",
    "SAVING_JOB": "Ўсимликларни ҳимоя қилиш ҳамда ободонлаштириш"
    " ва яшил хўжаликлар объектларини сақлаш бошқармаси",
    "LOCAL_ADMIN": "Маҳаллий админ",
    "MAIN_ADMIN": "Бош Aдмин",
}

group_app_names = {
    "PITOMNIK": [
        "pitomnik",
        "pitomnikplants",
        "pitomniksavingjob",
        "plant",
        "pitomnikimage",
        "pitomnikplantimage",
    ],
    "VEHICLE": ["vehicle"],
    "PRODUCTION": [
        "plantingproduction",
        "savingjobproduction",
        "irrigationproduction",
        "landscapejobproduction",
    ],
    "ACCOUNTING": ["debitcredit", "salary"],
    "FINANCE": [],
    "SAVING_JOB": [
        "irrigation",
        "irrigationimage",
        "newirrigation",
        "landscapejob",
        "landscapejobimage",
        "savingjob",
        "plantedplants",
        "pitomnik",
        "pitomnikplants",
        "plantedplantimage",
    ],
    "LOCAL_ADMIN": [
        "user",
        "pitomnik",
        "pitomnikplants",
        "pitomniksavingjob",
        "plant",
        "pitomnikimage",
        "plantingproduction",
        "savingjobproduction",
        "irrigationproduction",
        "landscapejobproduction",
        "debitcredit",
        "salary",
        "irrigation",
        "newirrigation",
        "landscapejob",
        "savingjob",
        "plantedplants",
        "pitomnik",
        "pitomnikplants",
        "plantedplantimage",
        "pitomnikplantimage",
        "vehicle",
    ],
    "MAIN_ADMIN": [],
}
base_permissions = ["add", "view", "change"]
admin_permissions = ["add", "view", "change", "delete"]


def add_permissions(group, permissions, app_names):
    for app_name in app_names:
        for permission in permissions:
            get_add_permission(f"{permission}_{app_name}", group)


def add_main_admin_permissions_by_app_name(app_name, admin_group):
    content_type = ContentType.objects.filter(app_label=app_name).exclude(
        model__contains="image"
    )
    for content in content_type:
        perm = Permission.objects.get(
            name=f"View {content.model} for Admin",
            codename=f"view_{content.model}_admin",
        )
        admin_group.permissions.add(perm)


def set_main_admin_permissions():
    app_names = ["pitomnik", "vehicles", "accounting", "account"]
    for app_name in app_names:
        create_permission_for_content(app_label=app_name)

    head_admin_group = Group.objects.get(name=group_names["MAIN_ADMIN"])

    for app_name in app_names:
        add_main_admin_permissions_by_app_name(app_name, head_admin_group)

    additional_code_names = [
        "view_pitomnikimage",
        "view_plantedplantimage",
        "view_pitomniksavingjobimage",
        "view_newirrigationimage",
        "view_landscapejobimage",
        "view_irrigationimage",
        "view_savingjobimage",
        "view_pitomnikplantimage",
        "view_monthlyproductionplan",
        "add_monthlyproductionplan",
        "change_monthlyproductionplan",
        "delete_monthlyproductionplan",
        "view_yearlyproductionplan",
        "change_yearlyproductionplan",
        "add_yearlyproductionplan",
        "delete_yearlyproductionplan",
        "view_saving",
    ]

    for code_name in additional_code_names:
        head_admin_group.permissions.add(
            Permission.objects.get(codename=code_name)
        )


def add_local_admin_permissions():
    group = Group.objects.get(name=group_names["LOCAL_ADMIN"])
    add_permissions(group, admin_permissions, group_app_names["LOCAL_ADMIN"])


def run():
    key_list = list(group_names.keys())
    val_list = list(group_names.values())
    for key in group_names:
        group, _ = Group.objects.get_or_create(name=group_names[key])
        if group.name in group_names.values() and group.name not in [
            "LOCAL_ADMIN",
            "MAIN_ADMIN",
        ]:
            position = val_list.index(group.name)
            key = key_list[position]
            add_permissions(group, base_permissions, group_app_names[key])

    add_local_admin_permissions()
    set_main_admin_permissions()
