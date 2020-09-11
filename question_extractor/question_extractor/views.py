"""
Request handler file to process incoming requests.

"""
from django.http import JsonResponse
from django.http import HttpResponse
from .extract import extract_qs, answer_evaluator

# Error handling
errors = {
    'ShortSentences': {
        'status': 400,
        'message': 'The sentences provided were too short.',
        'detail': 'Ensure that your sentences are of appropriate length for questions.'
    },
    'ValueError': {
        'status': 400,
        'message': 'The json provided was invalid.'
    },
    'UnansweredQuestionError': {
        'status': 400,
        'message': 'Some questions were left unanswered.'
    },
    'RequestedQuestionsError': {
        'status': 400,
        'message': 'Requested number of questions was too high for document.'
    }

}


def extract(request):
    if request.method == 'POST':
        text = request.POST['text']
        num = request.POST['num']

        # initialize Document object
        Doc = extract_qs.Document(text, int(num))

        # Extract qs
        Doc.question_extractor()

        # Answers & question dictionary
        ans_qs = Doc.answers_questions

        # If type is in then it entered a later error
        if ans_qs == 400:
            return JsonResponse(errors['ShortSentences'], safe=False)

        elif ans_qs == 444:
            return JsonResponse(errors['RequestedQuestionsError'], safe=False)

        return JsonResponse(ans_qs, safe=False)

    else:
        return HttpResponse('In the get')


def answer(request):
    if request.method == 'POST':
        user_ans = request.POST.getlist("user_ans")
        correct_ans = request.POST.getlist("correct_ans")

        if len(user_ans) != len(correct_ans):
            return JsonResponse(errors['UnansweredQuestionError'])

        i = 0
        bleu = 0.0

        while i < len(user_ans):
            # Get bleu score for each pair o answers and add to total
            bleu += answer_evaluator.get_bleu_score(correct_ans[i].split(), user_ans[i].split())
            i += 1

        # Average
        bleu = bleu / len(user_ans)

        r = {
            'score': bleu
        }
        # Return to Shan frontend
        return JsonResponse(r, safe=False)


def home(request):
    return HttpResponse("Home page for django server.")
