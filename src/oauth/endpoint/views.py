from rest_framework import viewsets, parsers, permissions

from .. import serializer, models
from ...base.permissions import IsAuthor


class UserView(viewsets.ModelViewSet):
    """ User CRUD """
    parser_classes = (parsers.MultiPartParser,)
    serializer_class = serializer.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.request.user

    def get_object(self):
        return self.get_queryset()


class AuthorView(viewsets.ReadOnlyModelViewSet):
    """ The list of Authors """
    queryset = models.AuthUser.objects.all().prefetch_related('social_links')
    serializer_class = serializer.AuthorSerializer


class SocialLinkView(viewsets.ModelViewSet):
    """ The CRUD for SocialLinks """
    queryset = models.SocialLink.objects.all()
    serializer_class = serializer.SocialLinkSerializer
    permission_classes = [IsAuthor]

    # def get_queryset(self):
    #     return self.request.user.social_links.all()
    #
    # def perform_create(self, serializer):
    #     serializer.save(user=self.request.user)