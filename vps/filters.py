import django_filters

from vps.models import Vps


class VpsFilter(django_filters.FilterSet):
    cpu = django_filters.NumberFilter()
    cpu_gt = django_filters.NumberFilter(field_name='cpu', lookup_expr='gt')
    cpu_lt = django_filters.NumberFilter(field_name='cpu', lookup_expr='lt')

    ram = django_filters.NumberFilter()
    ram_gt = django_filters.NumberFilter(field_name='ram', lookup_expr='gt')
    ram_lt = django_filters.NumberFilter(field_name='ram', lookup_expr='lt')

    hdd = django_filters.NumberFilter()
    hdd_gt = django_filters.NumberFilter(field_name='hdd', lookup_expr='gt')
    hdd_lt = django_filters.NumberFilter(field_name='hdd', lookup_expr='lt')

    status = django_filters.ChoiceFilter(choices=Vps.STATUSES)

    class Meta:
        model = Vps
        fields = ['cpu', 'ram', 'hdd', 'status']
