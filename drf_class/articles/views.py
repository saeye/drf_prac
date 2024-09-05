from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ArticleSerializer,
    ArticleDetailSerializer,
    CommentSerializer,
)
from .models import Article, Comment
from rest_framework.views import APIView


class ArticleListAPIView(APIView):

    permission_classes = [IsAuthenticated] 

    def get(self, request):
        print("\n\n\n 현재 유저의 유저네임:", request.user.username, "\n\n\n")
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class ArticleDetailAPIView(APIView):

    permission_classes = [IsAuthenticated] 

    def get_object(self, pk):
        return get_object_or_404(Article, pk=pk)

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleDetailSerializer(article, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, pk):
        article = self.get_object(pk)
        article.delete()
        data = {"pk": f"{pk} is deleted."}
        return Response(data, status=status.HTTP_200_OK)


class CommentListAPIView(APIView):

    permission_classes = [IsAuthenticated] 

    def get(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        comments = article.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def post(self, request, article_pk):
        article = get_object_or_404(Article, pk=article_pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class CommentDetailAPIView(APIView):

    permission_classes = [IsAuthenticated] 

    def get_object(self, comment_pk):
        return get_object_or_404(Comment, pk=comment_pk)

    def put(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    def delete(self, request, comment_pk):
        comment = self.get_object(comment_pk)
        comment.delete()
        return Response(status=status.HTTP_200_OK)
    

@api_view(["GET"])
def check_sql(request):
    from django.db import connection

    comments = Comment.objects.all().prefetch_related("article")
    for comment in comments:
        print(f"{comment.id}번 {comment.article.title}")

    return Response()
