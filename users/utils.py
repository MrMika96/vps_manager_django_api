from django.db.models import Count, Case, When, Value, CharField


def return_users_annotated_fields():
    return {
            'vps_count': Count("vps"),
            'workload': Case(
                When(vps_count__range=[1, 3], then=Value("EASY", output_field=CharField())),
                When(vps_count__range=[3, 8], then=Value("MEDIUM", output_field=CharField())),
                When(vps_count__gte=9, then=Value("HARD", output_field=CharField())),
                default=Value("VERY_EASY", output_field=CharField())
            ),
            'applications_deployed': Count("application", distinct=True)
        }