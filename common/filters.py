from rest_framework.filters import BaseFilterBackend

class DoctorFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        specialty = request.query_params.get('specialty')
        print("FILTER HIT", request.query_params)
        if specialty:
            queryset = queryset.filter(specialty__iexact = specialty)
        return queryset
    
from rest_framework.filters import BaseFilterBackend

