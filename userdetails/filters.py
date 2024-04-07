from django.db.models import Q
from userdetails.models import UserDetails
import django_filters


class UserDetailsListSearchFilter(django_filters.rest_framework.FilterSet):
    search = django_filters.CharFilter(method="my_search_filter", label="Search")

    referral_code = django_filters.CharFilter(method="my_referral_code_filter", label="Referral Code")

    def my_search_filter(self, queryset, name, value):
        return queryset.filter(display_name__icontains=value, is_active=True)

    def my_referral_code_filter(self, queryset, name, value):
        return queryset.filter(referral_code=value, is_active=True)


    class Meta:
        model = UserDetails
        fields = {}