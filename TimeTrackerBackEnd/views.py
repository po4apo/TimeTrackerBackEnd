import string

from django.contrib.auth import logout
from django.db.models import Sum, F
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, exceptions
from rest_framework import views, generics
from rest_framework import viewsets, mixins, status
from rest_framework.response import Response
from rest_framework.views import APIView

from TimeTrackerBackEnd import serializers, custom_permissions
from TimeTrackerBackEnd.models import ProjectModel, TaskModel, FrameModel

DETAIL = 'detail'


# Reg and Auth
class UserRegistrationView(APIView):
    serializer_class = serializers.UserRegisterSerializer
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        # simply delete the token to force a login
        logout(request)
        return Response(status=status.HTTP_200_OK)


class ProfileView(generics.RetrieveAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = ProjectModel.objects.all()
    serializer_class = serializers.ProjectSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,
                          custom_permissions.TaskPermissions)
    queryset = TaskModel.objects.all()
    serializer_class = serializers.TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project']
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(project__user=self.request.user)

    def perform_create(self, serializer):
        # return super().perform_create(serializer)
        got_project_id = self.request.data['project']
        user_projects = [project.pk for project in
                         ProjectModel.objects.filter(user=self.request.user)]
        if got_project_id not in user_projects:
            raise exceptions.ValidationError(
                {"project": [f"Invalid pk \"{got_project_id}\" - object does not exist."]})
        return super().perform_create(serializer)


class MangeTimeView(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    serializer_class = serializers.FrameSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = FrameModel.objects.all()
    http_method_names = ['get', 'post', 'patch']

    TASK_NOT_FOUND = string.Template('The project with pk=$pk does not exist')

    def last_frame(self, user):
        qs = self.queryset.filter(task__project__user=user)
        return qs.last()

    def status(self, request, *args, **kwargs):
        instance = self.last_frame(request.user)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def start(self, request, *args, **kwargs):
        """
        Start tracking time for current task.
        This view create frame with start_at. It means that time tracker is started.
        There can be only one active project.
        """

        task = TaskModel.objects.get(pk=request.data['task'])
        if task.project.user == request.user:
            last_frame = self.last_frame(request.user)
            if last_frame is None or last_frame.stop is not None:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                self.perform_create(serializer)
                headers = self.get_success_headers(serializer.data)
                return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
            else:
                msg = {
                    DETAIL: f'{last_frame.task.name} in {last_frame.task.project.name} already started'}
                headers = self.get_authenticate_header(msg)
                return Response(msg, status=status.HTTP_400_BAD_REQUEST, headers=headers)
        headers = self.get_authenticate_header({DETAIL: 'task'})
        return Response({DETAIL: 'task'}, status=status.HTTP_204_NO_CONTENT, headers=headers)

    def stop(self, request, *args, **kwargs):
        """
        Stop tracking time for active project.
        """
        last_item = self.last_frame(request.user)

        if last_item is not None and last_item.stop is None:
            request.data['start'] = last_item.start
            request.data['task'] = last_item.task.pk

            serializer = self.get_serializer(last_item, data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            msg = {DETAIL: f'There is no running project'}
            headers = self.get_authenticate_header(msg)
            return Response(msg, status.HTTP_400_BAD_REQUEST, headers=headers)


class StatisticView(viewsets.GenericViewSet):
    # Seems this class is not secure.
    # In general, hiding the data of one user from another looks unreliable in the project
    permission_classes = (permissions.IsAuthenticated,)
    queryset = FrameModel.objects.all()
    serializer_class = serializers.FrameSerializer

    @swagger_auto_schema(responses={200: "{time_spent: str}"})
    def task_time_spent(self, request, *args, **kwargs):
        queryset = FrameModel.objects.filter(
            task__project__user=request.user).filter(task=self.kwargs['pk'])
        time_spent = queryset.aggregate(time_spent=Sum(F("stop") - F('start')))
        return Response(time_spent, status=status.HTTP_200_OK)
