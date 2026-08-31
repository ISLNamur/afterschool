# This file is part of HappySchool.
#
# HappySchool is the legal property of its developers, whose names
# can be found in the AUTHORS file distributed with this source
# distribution.
#
# HappySchool is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# HappySchool is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with HappySchool.  If not, see <http://www.gnu.org/licenses/>.

import json
import xlsxwriter

from io import BytesIO

from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse

from django_filters import rest_framework as filters

from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from core.views import BaseFilters, BaseModelViewSet, get_app_settings, LargePageSizePagination
from core.utilities import get_menu
from core.email import send_email

from .models import AfterschoolSettingsModel, ActivityModel, ActivitySubscriptionModel
from .serializers import AfterschoolSettingsSerializer, ActivitySerializer, ActivitySubscriptionSerializer


def get_menu_entry(active_app, request):
    if not request.user.has_perm("afterschool.view_afterschool"):
        return {}
    return {
        "app": "afterschool",
        "display": "afterschool",
        "url": "/afterschool/",
        "active": active_app == "afterschool",
    }


def get_settings():
    return get_app_settings(AfterschoolSettingsModel)


class AfterschoolView(TemplateView):
    template_name = "afterschool/afterschool.html"
    filter_set = []

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context["menu"] = json.dumps(get_menu(self.request, "afterschool"))
        context["filters"] = json.dumps(self.filter_set)
        context["settings"] = json.dumps((AfterschoolSettingsSerializer(get_settings()).data))
        context["can_view_subscriptions"] = json.dumps(
            self.request.user.has_perm("afterschool.view_activitysubscriptionmodel")
        )

        return context


class ActivityViewSet(ReadOnlyModelViewSet):
    queryset = ActivityModel.objects.all()
    serializer_class = ActivitySerializer
    pagination_class = LargePageSizePagination


class ActivitySubscriptionViewSet(ModelViewSet):
    queryset = ActivitySubscriptionModel.objects.all()
    serializer_class = ActivitySubscriptionSerializer

    def get_permissions(self):
        if self.action == "create":
            permission_classes = []
        else:
            permission_classes = [DjangoModelPermissions]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        subscription = serializer.save()
        send_email(
            to=[subscription.resp_email],
            subject="Confirmation de la demande d'inscription à SLAS",
            email_template="afterschool/email_confirm.html",
            context={"sub": subscription}
        )


class SubscriptionExcelView(PermissionRequiredMixin, View):
    permission_required = ["afterschool.view_activitysubscriptionmodel"]

    def get(self, request, *args, **kwargs):
        subscriptions = ActivitySubscriptionModel.objects.all()
        file_name = "subscriptions.xlsx"
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet()
        worksheet.set_column(0, 2, 30)

        row = 0
        worksheet.write_row(0, 0, [
            "Nom élève",
            "Prénom élève",
            "Classe",
            "Date de naissance",
            "Autre famille",
            "Resp. nom",
            "Resp. prénom",
            "Resp. adresse",
            "Resp. courriel 1",
            "Resp. courriel 2",
            "Resp. tél. 1",
            "Resp. tél. 2",
            "Paiement",
            "Répondu",
            "Payé",
            "Activité",
        ])
        row += 1
        days = {
            0: "Lundi",
            1: "Mardi",
            2: "Mercredi",
            3: "Jeudi",
            4: "Vendredi",
        }
        for s in subscriptions:
            worksheet.write_row(row, 0, [
                s.student_lastname,
                s.student_firstname,
                s.classe,
                str(s.birth),
                s.family,
                s.resp_lastname,
                s.resp_firstname,
                s.resp_address,
                s.resp_email,
                s.resp_email_2,
                s.resp_phone,
                s.resp_phone_2,
                s.resp_payement,
                s.answered,
                s.payed,
                f"{s.activity.name} ({days[s.activity.day]} / {s.activity.timerange})",
            ])
            row += 1
        workbook.close()

        response = HttpResponse(
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = 'filename; filename="' + file_name + '"'
        response.write(output.getvalue())
        return response
