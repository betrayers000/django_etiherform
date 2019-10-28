from django.shortcuts import render, redirect, get_object_or_404
from .forms import QuestionsForm, ChoiceForm
from .models import Question, Choice
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    questions = Question.objects.all()
    return render(request, 'questions/index.html', {'questions': questions})

def detail(request, id):
    question = get_object_or_404(Question, id=id)
    choice_form = ChoiceForm()
    # choice_1 = len(Choice.objects.filter(question=question, pick=1))
    # choice_2 = len(Choice.objects.filter(question=question, pick=2))
    # total = choice_1 + choice_2
    # per1 = round(choice_1/total)
    # per2 = round(choice_2/total)
    choices = question.choice_set.all()
    choice_1 = choices.filter(pick=1).count()
    choice_2 = len(choices.filter(pick=2))

    total = choices.count()

    per_1, per_2 = 50, 50
    if total != 0:
        per_1 = choice_1/total * 100
        per_2 = choice_2/total * 100

    context = {
        'question':question,
        'choice_form':choice_form,
        'num1': choice_1,
        'num2': choice_2,
        'per_1': per_1,
        'per_2': per_2, 
    }
    return render(request, 'questions/detail.html', context)

def update(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method == "POST":
        form = QuestionsForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            return redirect('questions:detail', id)
    else:
        form = QuestionsForm(instance=question)
    context = {
        'form': form
    }
    return render(request, 'questions/form.html', context)

def delete(request, id):
    question = get_object_or_404(Question, id=id)
    question.delete()
    return redirect('questions:index')

@login_required
def create(request):
    # 1. 글쓰기 클릭 > GET요청
    # 6. 사용자가 올바르지않은 데이터를 입력하고 제출 클릭 > POST요청
    # 12. 사용자가 올바른 데이터를 입력하고 제출 클릭 > POST요청

    # 7. POST요청이기 때문에 if문 실행
    # 13. POST요청이기 때문에 if문 실행
    if request.method == "POST":
        # 8. 들어온 요청에 대한 form을 생성
        # 14. 들어온 요청에 대한 form을 생성
        form = QuestionsForm(request.POST)
        # 9. 생성된 form의 데이터가 올바른지 검증
        # 15. 생성된 form의 데이터가 올바른지 검증
        if form.is_valid():
            # 16. 데이터가 올바르기 때문에 저장
            form.save()
            # 17. 데이터 저장 후 메인페이지로 이동
            return redirect('questions:index')
    # 2. GET요청이기때문에 else문 실행
    else:
        # 3. 입력을 위한 form을 생성 (GET으로 요청받았을때)
        form = QuestionsForm()
    # 4. form을 context에 넣기
    # 10. form의 데이터가 검증을 통과 못했을 시
    #     올바르게 입력된 데이터는 남기고 다시 form 보여주기
    context = {
        'form': form
    }
    # 5. form.html 보여주기 (빈 form)
    # 11. form.html 보여주기 (올바른 데이터는 들어있음)
    return render(request, 'questions/form.html', context)

def choice_create(request, id):
    question = get_object_or_404(Question, id=id)
    if request.method == "POST":
        # form = ChoiceForm(request.POST, instance=question)
        # if form.is_valid():
        #     choice = Choice()
        #     pick = request.POST.get('pick')
        #     comment = request.POST.get('comment')
        #     choice.question = question
        #     choice.pick = pick
        #     choice.comment = comment
        #     choice.save()
        choice_form = ChoiceForm(request.POST)
        if choice_form.is_valid():
            choice = choice_form.save(commit=False)
            choice.question = question
            choice.save()
            return redirect('questions:detail', id)
    else:
        pass

@require_POST
def choice_delete(request, question_id, choice_id):
    choice = get_object_or_404(Choice, id=choice_id)
    if request.method == "POST":
        choice.delete()
    return redirect('questions:detail', question_id)