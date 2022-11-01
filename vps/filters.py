import django_filters

from vps.models import Vps


class VpsFilter(django_filters.FilterSet):
    cpu = django_filters.NumberFilter(help_text="For finding vps with specific cpu value")
    cpu_gt = django_filters.NumberFilter(
        field_name="cpu",
        lookup_expr="gt",
        help_text="For finding vps with cpu value bigger then cpu_gt"
    )
    cpu_lt = django_filters.NumberFilter(
        field_name="cpu",
        lookup_expr="lt",
        help_text="For finding vps with cpu value bigger then cpu_gt"
    )

    ram = django_filters.NumberFilter(help_text="For finding vps with specific ram value")
    ram_gt = django_filters.NumberFilter(
        field_name="ram",
        lookup_expr="gt",
        help_text="For finding vps with cpu value bigger then ram_gt"
    )
    ram_lt = django_filters.NumberFilter(
        field_name="ram",
        lookup_expr="lt",
        help_text="For finding vps with cpu value bigger then ram_lt"
    )

    hdd = django_filters.NumberFilter(help_text="For finding vps with specific hdd value")
    hdd_gt = django_filters.NumberFilter(
        field_name="hdd",
        lookup_expr="gt",
        help_text="For finding vps with cpu value bigger then hdd_gt"
    )
    hdd_lt = django_filters.NumberFilter(
        field_name="hdd",
        lookup_expr="lt",
        help_text="For finding vps with cpu value bigger then hdd_lt"

    )
    status = django_filters.ChoiceFilter(
        choices=Vps.STATUSES,
        help_text="Display all vps with selected status"
    )

    class Meta:
        model = Vps
        fields = ["cpu", "ram", "hdd", "status"]
