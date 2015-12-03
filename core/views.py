from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from .models import *
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.views.generic import FormView
from .forms import *

# Create your views here.
class Home(TemplateView):
  template_name = "home.html"

class QuestionCreateView(CreateView):
    model = Question
    template_name = "question/question_form.html"
    fields = ['title', 'description', 'visibility']
    success_url = reverse_lazy('question_list')

    def form_valid(self, form):
      form.instance.user = self.request.user
      return super(QuestionCreateView, self).form_valid(form)

class QuestionListView(ListView):
    model = Question
    template_name = "question/question_list.html"
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super(QuestionListView, self).get_context_data(**kwargs)
        user_votes = Question.objects.filter(vote__user=self.request.user)
        context['user_votes'] = user_votes
        return context

class QuestionDetailView(DetailView):
    model = Question
    template_name = 'question/question_detail.html'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)
        question = Question.objects.get(id=self.kwargs['pk'])
        answers = Answer.objects.filter(question=question)
        context['answers'] = answers
        user_answers = Answer.objects.filter(question=question, user=self.request.user)
        context['user_answers'] = user_answers
        user_votes = Answer.objects.filter(vote__user=self.request.user)
        context['user_votes'] = user_votes
        return context

class QuestionUpdateView(UpdateView):
    model = Question
    template_name = 'question/question_form.html'
    fields = ['title', 'description']

    def get_object(self, *args, **kwargs):
            object = super(QuestionUpdateView, self).get_object(*args, **kwargs)
            if object.user != self.request.user:
                raise PermissionDenied()
            return object

class QuestionDeleteView(DeleteView):
    model = Question
    template_name = 'question/question_confirm_delete.html'
    success_url = reverse_lazy('question_list')

    def get_object(self, *args, **kwargs):
            object = super(QuestionDeleteView, self).get_object(*args, **kwargs)
            if object.user != self.request.user:
                raise PermissionDenied()
            return object

class AnswerCreateView(CreateView):
    model = Answer
    template_name = "answer/answer_form.html"
    fields = ['text', 'visibility']

    def get_success_url(self):
        return self.object.question.get_absolute_url()

    def form_valid(self, form):
        question = Question.objects.get(id=self.kwargs['pk'])
        if Answer.objects.filter(question=question, user=self.request.user).exists():
          raise PermissionDenied()
        form.instance.user = self.request.user
        form.instance.question = Question.objects.get(id=self.kwargs['pk'])
        return super(AnswerCreateView, self).form_valid(form)

class AnswerUpdateView(UpdateView):
    model = Answer
    pk_url_kwarg = 'answer_pk'
    template_name = 'answer/answer_form.html'
    fields = ['text']

    def get_success_url(self):
        return self.object.question.get_absolute_url()

    def get_object(self, *args, **kwargs):
            object = super(AnswerUpdateView, self).get_object(*args, **kwargs)
            if object.user != self.request.user:
                raise PermissionDenied()
            return object

class AnswerDeleteView(DeleteView):
    model = Answer
    pk_url_kwarg = 'answer_pk'
    template_name = 'answer/answer_confirm_delete.html'

    def get_success_url(self):
        return self.object.question.get_absolute_url()

    def get_object(self, *args, **kwargs):
            object = super(AnswerDeleteView, self).get_object(*args, **kwargs)
            if object.user != self.request.user:
                raise PermissionDenied()
            return object

class VoteFormView(FormView):
    form_class = VoteForm

    def form_valid(self, form):
        user = self.request.user
        question = Question.objects.get(pk=form.data["question"])
        try:
            answer = Answer.objects.get(pk=form.data["answer"])
            prev_votes = Vote.objects.filter(user=user, answer=answer)
            has_voted = (prev_votes.count()>0)
            if not has_voted:
                Vote.objects.create(user=user, answer=answer)
            else:
                prev_votes[0].delete()
            return redirect(reverse('question_detail', args=[form.data["question"]]))
        except:
            prev_votes = Vote.objects.filter(user=user, question=question)
            has_voted = (prev_votes.count()>0)
            if not has_voted:
                Vote.objects.create(user=user, question=question)
            else:
                prev_votes[0].delete()
        return redirect('question_list')

class UserDetailView(DetailView):
    model = User
    slug_field = 'username'
    template_name = 'user/user_detail.html'
    context_object_name = 'user_in_view'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user_in_view = User.objects.get(username=self.kwargs['slug'])
        questions = Question.objects.filter(user=user_in_view).exclude(visibility=1)
        context['questions'] = questions
        answers = Answer.objects.filter(user=user_in_view).exclude(visibility=1)
        context['answers'] = answers
        return context

class UserUpdateView(UpdateView):
    model = User
    slug_field = "username"
    template_name = "user/user_form.html"
    fields = ['email', 'first_name', 'last_name']

    def get_success_url(self):
        return reverse('user_detail', args=[self.request.user.username])

    def get_object(self, *args, **kwargs):
        object = super(UserUpdateView, self).get_object(*args, **kwargs)
        if object != self.request.user:
            raise PermissionDenied()
        return object

class UserDeleteView(DeleteView):
    model = User
    slug_field = "username"
    template_name = 'user/user_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('logout')

    def get_object(self, *args, **kwargs):
        object = super(UserDeleteView, self).get_object(*args, **kwargs)
        if object != self.request.user:
            raise PermissionDenied()
        return object

    def delete(self, request, *args, **kwargs):
        user = super(UserDeleteView, self).get_object(*args)
        user.is_active = False
        user.save()
        return redirect(self.get_success_url())

class SearchQuestionListView(QuestionListView):
    def get_queryset(self):
        incoming_query_string = self.request.GET.get('query','')
        return Question.objects.filter(title__icontains=incoming_query_string)