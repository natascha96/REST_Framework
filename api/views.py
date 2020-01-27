from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.views import APIView
from vocabulary_trainer.models import ListAccess, Vokabel, VokabelList
from .serializers import VokabelListSerializer, VokabelSerializer



class VocabularyListAPIView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        list_ids = ListAccess.objects.values_list('list').filter(user=request.user)
        lists = VokabelList.objects.filter(id__in=list_ids).values()
        return Response({"lists": lists})

    def post(self, request):
        name = request.data.get('name', None)
        description = request.data.get('description', '')

        if not name:
            return Response(status=400)

        new_list = VokabelList.objects.create(
            name=name,
            description=description
        )
        new_list.save()

        ListAccess.objects.create(
            user=request.user,
            list=new_list,
            role='owner'
        )

        return Response({
            'id': new_list.id,
            'name': new_list.name,
            'description': new_list.description
        }, status=201)


class VocabularyDetailListAPIView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        saved_vokabellist = get_object_or_404(VokabelList.objects.all(), pk=pk)
        data = request.data.get('vokabellist')
        serializer = VokabelListSerializer(instance=saved_vokabellist, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            vokabellist_saved = serializer.save()
        return Response({"success": "Vokabellist '{}' updated successfully".format(vokabellist_saved.name)})

    def delete(self, request, pk):
        # Hole die Vokabelliste mit diesem Primärschlüssel
        vokabellist = get_object_or_404(VokabelList.objects.all(), pk=pk)
        vokabellist.delete()
        return Response({"message": "Vokbellist with id `{}` has been deleted.".format(pk)}, status=204)



class VocabularyAPIView(APIView):

    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):

        resp_dict = {
            'status': None,
            'message': None,
            'data': None
        }

        try:
            list_id = request.query_params.get("list_id", None)

            # checken ob die list id angegben wurde
            if list_id is None or list_id == '':
                raise ValueError("Bitte eine Listen ID angeben")

            # die Vokabeln holen
            try:
                vokabel_list_obj = VokabelList.objects.get(id=list_id)
            except ObjectDoesNotExist:
                raise ValueError("Die Listen ID ist ungültig")

            # überpürfen ob der Nutzer diese Liste einsehen darf
            try:
                list_perm_qs = ListAccess.objects.get(user=request.user, list=vokabel_list_obj)
            except ObjectDoesNotExist:
                raise PermissionError("Diese Liste gehört nicht zu deinem User Account")

            # Vokabeln holen
            vokabeln = Vokabel.objects.filter(list=vokabel_list_obj).values()

            resp_dict['status'] = "success"
            resp_dict['message'] = "Fetched tasks successfully"
            resp_dict['data'] = vokabeln
            resp = Response(resp_dict)
            resp.status_code = 200

        except PermissionError as pe:
            resp_dict['status'] = "failed"
            resp_dict['message'] = pe.__str__()
            resp_dict['data'] = None
            resp = Response(resp_dict)
            resp.status_code = 403
        except ValueError as ve:
            resp_dict['status'] = "failed"
            resp_dict['message'] = ve.__str__()
            resp_dict['data'] = None
            resp = Response(resp_dict)
            resp.status_code = 400
        except Exception as e:
            resp_dict['status'] = "failed"
            resp_dict['message'] = "Something went wrong, Error: " + e.__str__()
            resp_dict['data'] = None
            resp = Response(resp_dict)
            resp.status_code = 500

        return resp


    def post(self, request):
        list_id = request.data.get("list_id")
        name1 = request.data.get("name1")
        name2 = request.data.get('name2')

        vokabel_list = VokabelList.objects.get(id=list_id)

        new_vokabel = Vokabel(
            list=vokabel_list,
            name1=name1,
            name2=name2
        )
        new_vokabel.save()

        return Response({
            'id': new_vokabel.pk,
            'list': new_vokabel.list,
            'name1': new_vokabel.name1,
            'name2': new_vokabel.name2,
            'done': new_vokabel.done
        }, status=201)


class VocabularyDetailAPIView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        saved_vokabel = get_object_or_404(VokabelList.objects.all(), pk=pk)
        data = request.data.get('vokabellist')
        serializer = VokabelSerializer(instance=saved_vokabel, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            vokabel_saved = serializer.save()
        return Response({"success": "Vokabel '{}' updated successfully".format(vokabel_saved.name1)})

    def delete(self, request, pk):
        # Hole die Vokabel mit diesem Primärschlüssel
        vokabel = get_object_or_404(Vokabel.objects.all(), pk=pk)
        vokabel.delete()
        return Response({"message": "Vokbel with id `{}` has been deleted.".format(pk)}, status=204)


class VocabularyStatusAPIView(APIView):
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        vokabel_id = request.data.get("vokabel_id")
        new_status = request.data.get("status")
        new_status = True if new_status.lower() == 'true' else False

        vokabel_obj = Vokabel.objects.get(id=vokabel_id)
        user_perm = ListAccess.objects.get(user=request.user, list=vokabel_obj.list)
        vokabel_obj.done = new_status
        vokabel_obj.save()

        return Response({
            'vokabel_id': vokabel_obj,
            'status': new_status,
        }, status=201)
