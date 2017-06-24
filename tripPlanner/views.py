from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from .models import GroupUser, ProjectGroup, ProjectHost, ProjectInvitee,\
    Answer, Preference
from .forms import InviteFriendForm, MakeGroupForm, MakePrefsForm
from django.contrib.auth.models import User
from django import forms


def home(request):
    if(request.user.is_authenticated):
        groups = GroupUser.objects.filter(groupUsername=request.user)
        hostingProjects = ProjectHost.objects.filter(host=request.user)
        invitedInProjects = ProjectInvitee.objects.filter(invitee=request.user)
        return render(request, 'tripPlanner/home.html',
                      {
                          'groups': groups,
                          'hostingProjects': hostingProjects,
                          'invitedInProjects': invitedInProjects,
                      })
    else:
        return redirect('loginPage')


def logoutPage(request):
    logout(request)
    return redirect('loginPage')


def createGroup(request):
    if(request.user.is_authenticated):
        if(request.method == "POST"):
            form = MakeGroupForm(request.POST)
            if(form.is_valid()):
                projectGroup = form.save()
                groupUser = GroupUser(groupUsername=request.user,
                                      ingroup=projectGroup)
                groupUser.save()
                return redirect('tripPlanner:makingPreferences',
                                projpk=projectGroup.pk)
            else:
                form = MakeGroupForm()
                return render(request, 'tripPlanner/createGroup.html',
                              {
                                  'form': form,
                              })
        else:
            form = MakeGroupForm()
            return render(request, 'tripPlanner/createGroup.html',
                          {
                              'form': form,
                          })
    else:
        return redirect('loginPage')


def makingPreferences(request, projpk):
    if(request.user.is_authenticated):
        if(request.method == "POST"):
            form = MakePrefsForm(request.POST)
            if(form.is_valid()):
                counter = 1
                for x in range(len(request.POST.dict())):
                    theVar = request.POST.dict().get('question_%s' %
                                                     counter)
                    if(theVar):
                        ans = Answer.objects.get(pk=theVar)
                        counter += 1
                    else:
                        continue
                    groupUser = GroupUser.objects.\
                        get(groupUsername=request.user,
                            ingroup=ProjectGroup.objects.get(pk=projpk))
                    Preference(answer=ans, groupUser=groupUser).save()
                return redirect('tripPlanner:groupDetail', pk=projpk)
            else:
                return redirect('/')
        else:
            theGroup = get_object_or_404(ProjectGroup, pk=projpk)
            groupUserAlready =\
                GroupUser.objects.filter(groupUsername=request.user,
                                         ingroup=theGroup)
            if(not groupUserAlready):
                groupUser = GroupUser(groupUsername=request.user,
                                      ingroup=theGroup)
                groupUser.save()
            questions = {}
            answers = []
            theTopic = theGroup.inTopic
            i = 1
            for question in theTopic.question_set.all():
                for answer in question.answer_set.all():
                    answers.append((str(answer.pk), answer.text))
                questions['question_%s' % i] =\
                    forms.\
                    ChoiceField(choices=answers,
                                label=question.text)
                answers = []
                i += 1
            form = MakePrefsForm()
            for x in range(len(questions)):
                form.__dict__['fields']['question_%s' % str(x+1)] =\
                    questions['question_%s' % str(x+1)]
            return render(request, 'tripPlanner/makingPreferences.html',
                          {
                              'form': form,
                              'projpk': projpk,
                          })
    else:
        return redirect('loginPage')


def groupDetail(request, pk):
    if(request.user.is_authenticated):
        group = get_object_or_404(ProjectGroup, pk=pk)
        groupmembers = group.groupuser_set.all()
        return render(request, 'tripPlanner/groupDetail.html',
                      {
                          'groupmembers': groupmembers,
                          'group': group,
                      })
    else:
        return redirect('loginPage')


def inviteFriend(request, projpk):
    if(request.user.is_authenticated):
        if(request.method == "POST"):
            form = InviteFriendForm(request.POST)
            if(form.is_valid()):
                form = form.clean()
                try:
                    invitee = User.objects.get(username=form['username'])
                except User.DoesNotExist:
                    invitee = None
                if(invitee):
                    if(invitee != request.user):
                        """invite"""
                        projectDB = get_object_or_404(ProjectGroup, pk=projpk)
                        alreadyInProj = GroupUser.objects.\
                            filter(groupUsername=invitee,
                                   ingroup=projectDB)
                        if(alreadyInProj):
                            return redirect('tripPlanner:inviteResultFalse',
                                            projpk=projpk,
                                            errNo=3,
                                            username=form['username'])
                        already = ProjectInvitee.\
                            objects.\
                            filter(invitee=invitee,
                                   host=ProjectHost.objects.
                                   filter(forProject=projectDB))
                        if(already):
                            return redirect('tripPlanner:inviteResultFalse',
                                            projpk=projpk,
                                            username=form['username'],
                                            errNo=2)
                        hostDBalready = ProjectHost.objects.\
                            filter(forProject=projectDB,
                                   host=request.user)
                        if(not hostDBalready):
                            hostDB = ProjectHost(forProject=projectDB,
                                                 host=request.user)
                            hostDB.save()
                        else:
                            hostDB = hostDBalready[0]
                        inviteeDB = ProjectInvitee(host=hostDB,
                                                   invitee=invitee)
                        inviteeDB.save()
                        return redirect('tripPlanner:inviteResultTrue',
                                        projpk=projpk,
                                        username=form['username'])
                    else:
                        return redirect('tripPlanner:inviteResultFalse',
                                        projpk=projpk,
                                        username=form['username'],
                                        errNo=0)
                else:
                    """no such username"""
                    return redirect('tripPlanner:inviteResultFalse',
                                    projpk=projpk, username=form['username'],
                                    errNo=1)
            else:
                return redirect('/')
        else:
            form = InviteFriendForm()
            return render(request, 'tripPlanner/inviteFriend.html',
                          {
                              'projpk': projpk,
                              'form': form,
                          })
    else:
        return redirect('loginPage')


def inviteResultTrue(request, projpk, username):
    text = "You have successfully invited %s" % (username)
    return render(request, 'tripPlanner/inviteResultTrue.html',
                  {
                      'projpk': projpk,
                      'text': text,
                  })


def inviteResultFalse(request, projpk, username, errNo):
    if(int(errNo) == 1):
        text = "There is no user with username: %s" % (username)
    elif(int(errNo) == 0):
        text = "You cannot invite yourself!"
    elif(int(errNo) == 2):
        text = "%s have been invited to %s" % (username,
                                               ProjectGroup.objects.
                                               get(pk=projpk))
    else:
        text = "%s is already in this group" % username
    return render(request, 'tripPlanner/inviteResultFalse.html',
                  {
                      'projpk': projpk,
                      'text': text,
                  })


def declineInvitation(request, ipk):
    if(request.user.is_authenticated):
        ProjectInvitee.objects.get(pk=ipk).delete()
        return redirect('/')
    else:
        return redirect('/')


def acceptInvitation(request, projpk, ipk):
    if(request.user.is_authenticated):
        ProjectInvitee.objects.get(pk=ipk).delete()
        return redirect('tripPlanner:makingPreferences', projpk=projpk)
    else:
        return redirect('/')
