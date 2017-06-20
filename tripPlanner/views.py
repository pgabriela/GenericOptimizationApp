from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import logout
from .models import GroupUser, ProjectGroup, ProjectHost, ProjectInvitee
from .forms import InviteFriendForm
from django.contrib.auth.models import User


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
        return render(request, 'tripPlanner/createGroup.html', {})
    else:
        return redirect('loginPage')


def createGroup2(request):
    if(request.user.is_authenticated):
        """todo"""
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
                        already = ProjectInvitee.\
                            objects.\
                            filter(invitee=invitee,
                                   host=ProjectHost.objects.
                                   filter(forProject=projectDB,
                                          host=request.user))
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
                            hostDB = hostDBalready
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
    else:
        text = "You have invited %s to %s" % (username,
                                              ProjectGroup.objects.
                                              get(pk=projpk))
    return render(request, 'tripPlanner/inviteResultFalse.html',
                  {
                      'projpk': projpk,
                      'text': text,
                  })
