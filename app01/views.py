from django.shortcuts import render
from app01 import models

class Foo(object):
    def __init__(self,data):
        self.data = data

    def __iter__(self):
        for item in self.data:
            yield item

def test(request):
    user_list = [
        {'id':1,'name':'alex','age':19},
        {'id':2,'name':'eric','age':18},
    ]
    obj = Foo(user_list)
    return render(request,'test.html',{'user_list':obj})

from django.forms import ModelForm

class QuestionModelForm(ModelForm):
    class Meta:
        model = models.Question
        fields = ['caption','tp']


class OptionModelForm(ModelForm):
    class Meta:
        model = models.Option
        fields = ['name','score']

def question(request,pid):
    """
    问题
    :param request:
    :param pid: 问卷ID
    :return:
    """
    # 获取当前问卷中的所有问题
    """
    que_list = models.Question.objects.filter(naire_id=pid) # [Question,Question,Question]
    if not que_list:
        # 新创建的问卷，其中还么有创建问题
        form_list = []
        form = QuestionModelForm()
        form_list.append(form)
    else:
        form_list = []
        # 含问题的问卷
        for que in que_list:
            form = QuestionModelForm(instance=que)
            form_list.append(form)

    return render(request,'que_list.html',{'form_list':form_list})
    """

    # def inner():
    #     que_list = models.Question.objects.filter(naire_id=pid)  # [Question,Question,Question]
    #     if not que_list:
    #         # 新创建的问卷，其中还么有创建问题
    #         form = QuestionModelForm()
    #         yield {'form':form,'obj':None,'option_class':'hide','options':None}
    #     else:
    #         # 含问题的问卷
    #         for que in que_list:
    #             form = QuestionModelForm(instance=que)
    #             temp =  {'form':form, 'obj':que, 'option_class':'hide','options':None}
    #             if que.tp == 2:
    #                 temp['option_class'] = ''
    #                 # 获取当前问题的所有选项？que
    #                 option_model_list = []
    #                 option_list = models.Option.objects.filter(qs=que)
    #                 for v in option_list:
    #                     vm = OptionModelForm(instance=v)
    #                     option_model_list.append(vm)
    #                 temp['options'] =option_model_list
    #             yield temp
    #
    # return render(request, 'que_list.html', {'form_list': inner()})


    def inner():
        que_list = models.Question.objects.filter(naire_id=pid)  # [Question,Question,Question]
        if not que_list:
            # 新创建的问卷，其中还么有创建问题
            form = QuestionModelForm()
            yield {'form': form, 'obj': None, 'option_class': 'hide', 'options': None}
        else:
            # 含问题的问卷
            for que in que_list:
                form = QuestionModelForm(instance=que)
                temp = {'form': form, 'obj': que, 'option_class': 'hide', 'options': None}
                if que.tp == 2:
                    temp['option_class'] = ''
                    # 获取当前问题的所有选项？que
                    def inner_loop(quee):
                        option_list = models.Option.objects.filter(qs=quee)
                        for v in option_list:
                            yield {'form':OptionModelForm(instance=v), 'obj':v}
                    # temp['options'] = inner_loop(que)
                    temp['options'] = inner_loop(que)
                yield temp

    return render(request, 'que_list.html', {'form_list': inner()})





