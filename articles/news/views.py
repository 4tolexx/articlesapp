from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.views.generic.edit import FormMixin
from .forms import CommentForm
from .models import Post, Comment, Profile


class ProfileDetailView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = "news/profile_detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(created_by__username=self.kwargs['username'])
        return context

    def get_object(self):
        return get_object_or_404(self.model, username=self.kwargs['username'])


class ProfileEditView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ["bio", "full_name", "image",]
    template_name = "news/profile_edit.html"

    def get_object(self, queryset=None):
        return self.model.objects.get(user__username=self.request.user)

    def get_success_url(self):
        return reverse("news:profile-detail", args=(self.object.user.username,))


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "description",]
    template_name = "news/news_form.html"

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)



class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "description",]
    template_name = "news/news_form.html"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.created_by:
            return True
        return False


    # def get_context_data(self, **kwargs):
    #     context = super(PostEditView, self).get_context_data(**kwargs)
    #     context['button_delete_show'] = True
    #     return context

    # def get_absolute_url(self):
    #     return reverse("news:article-detail", kwargs={"pk": self.pk})




class PostListView(ListView):
    model = Post
    context_object_name = "post_list"
    template_name = "news/news_list.html"
    paginate_by = 15
    ordering = "-publication_date"



class PostDetailView(FormMixin, DetailView):
    model = Post
    context_object_name = "post"
    template_name = "news/news_detail.html"
    form_class = CommentForm

    def get_success_url(self):
        return reverse("news:article-detail", kwargs={"pk":self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CommentForm(initial={"post":self.object})
        return context 

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.user_comment = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.save()
        return super(PostDetailView, self).form_valid(form)



# Article comment section 
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ["comment_body",]
    template_name = "news/comment_form.html"

    def form_valid(self, form):
        form.instance.user_comment = self.request.user
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        return super().form_valid(form)






