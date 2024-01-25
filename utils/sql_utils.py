from pprint import pprint

from django.db import connection
from django.utils.deprecation import MiddlewareMixin

from vps_manager_django_api import settings


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


class PrintSqlQuery(MiddlewareMixin):
    def process_response(self, request, response):
        if settings.DEBUG and settings.LOCAL and len(connection.queries) > 0:
            from pygments import highlight
            from pygments.formatters.terminal import TerminalFormatter
            from pygments.lexers.sql import SqlLexer
            from pygments_pprint_sql import SqlFilter

            queries = connection.queries
            lexer = SqlLexer()
            lexer.add_filter(SqlFilter())

            totsecs = 0.0
            print(f"Client IP: {get_client_ip(request)}")
            request_no_auth = {
                x: request.headers[x]
                for x in request.headers
                if x not in ["Authorization", "Cookie"]
            }
            pprint(f"Request headers: \n{request_no_auth}")
            for query in queries:
                print(query["time"], "used on:")
                totsecs += float(query["time"])
                print(highlight(query["sql"], lexer, TerminalFormatter()))

            print("Number of queries:", len(queries))
            print("Total time:", totsecs)
        return response
