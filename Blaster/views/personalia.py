# Third-party imports
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

# Local imports
from Blaster.models.BlastJob import BlastJob
from Blaster.models.BlastBuddies import BlastBuddies
from Blaster.models.SharedJobs import SharedJobs


@login_required()
def personalia_page(request: WSGIRequest) \
    -> HttpResponse | HttpResponseRedirect:
    """Renders the personalia page

    Renders the personalia page. With obtaining multiple statistics of the 
    user. The view also call the password change when request method is post.

    When the user is not logged in the user will be redirected to the login 
    page with the next page being personalia.
    The 403 page will thus not be rendered, as it redirects to the login page.

    If this view is loaded the only way for the request method to be post 
    would be if the change password was used on the page, for this reason the 
    if statement checking for post works to change the password.
    If a new post request possiblity would be added this also needs to change.

    The Shared_Jobs need to be retrieved or created because a new user 
    does not yet have the shared_jobs table. This will ensure that the table 
    exists for the user when accaccessing asing the page. 
    It would be better to move the code that creates the Shared_Jobs table to 
    the signup views, so all new users have the table after signing up.

    :param request: Django request object
    :type request: WSGIRequest
    :return : personalia page with the user information or redirects 
    back to personalia page after passwword change
    :rtype: Union[HttpResponse, redirect]
    """

    # Render 403 if user isn't logged in is not rendered here, 
    # this code is not used.
    if not request.user.is_authenticated:
        return render(request, '403.html')

    # Change password and refresh page on POST
    if request.method == 'POST':
        change_password(request)
        return redirect(personalia_page)

    # Calculate stats and shared jobs
    jobs_done, days_on_masterblast, total_query_len, avg_hits_job, \
        longest_query = obtain_stats(request)
    
    user = request.user
    # IMPORTANT OR IT BREAKS, is needed for new users that dont have the table
    shared_jobs, created = SharedJobs.objects.get_or_create(user = user)
    shared_jobs = SharedJobs.objects.get(user=request.user)\
        .shared_job.all().annotate(hit_count=Count('blasthit'))

    context = {
        'jobs_done': jobs_done,
        'days_on_master_blast': days_on_masterblast,
        'tot_query_len': total_query_len,
        'avg_hits_job': avg_hits_job,
        'Longes_query': longest_query,
        'shared_jobs': shared_jobs
    }
    return render(request, 'pages/personalia.html', context)


@login_required(login_url = "login")
def change_password(request: WSGIRequest) -> None:
    """Changes the user password

    Handles changing the password if the given old password is correct
    and the new password was filled in correctly twice. User stays
    logged in upon changing password.

    :param request: Django request object
    :type request: WSGIRequest
    :return: there is no return as the password change doesnt return
    :rtype: None
    """

    old_password = request.POST.get('Old_Password')
    new_password = request.POST.get('New_Password')
    new_password2 = request.POST.get('New_Password2')
    user = request.user

    if user.check_password(old_password):
        if new_password == new_password2:
            user.set_password(new_password)
            user.save()
            # Keeps user logged in after change
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password has been \
                            successfully changed.')
        else:
            messages.error(request, 'New passwords do not match.')
    else:
        messages.error(request, 'Incorrect old password.')


def obtain_stats(request: WSGIRequest) -> tuple[int, int, int, float, int]:
    """Obtains user statistics

    Obtains/calculates the statistics shown on the perosnalia page:
    total jobs done, total days on masterblast, total length of
    queries, the average amount of hits per job  rounded to 2 decimels,
    the length of the longest query submitted by the user.

    :param WSGIRequest request: Django request object
    :type request: WSGIRequest
    :return: all the user stats in order jobs_done, days_on_master_blast, 
    tot_query_len, avg_hits_job and Longes_query
    :rtype: tuple[int, int, int, float, int]
    """
    user = request.user

    jobs_done = 0
    days_on_master_blast = 0
    tot_query_len = 0
    tot_hits = 0
    tot_jobs = 0
    longest_query = 0

    jobs_done = BlastJob.objects.filter(user = request.user).count()

    current_date = timezone.now()
    register_date = timezone.localtime(user.date_joined)
    days_on_master_blast = (current_date - register_date).days

    blast_jobs = BlastJob.objects.filter(user = request.user)
    if blast_jobs.exists():
        for blast_job in blast_jobs:
            len_seq = len(blast_job.sequence)
            tot_query_len += len_seq
            tot_hits += blast_job.blasthit_set.count()
            tot_jobs += 1
            if len_seq >= longest_query:
                longest_query = len_seq

    if tot_jobs != 0:
        avg_hits_job = tot_hits / tot_jobs
        avg_hits_job = round(avg_hits_job, 2)
    else:
        avg_hits_job = 0
    return jobs_done, days_on_master_blast, tot_query_len, avg_hits_job, longest_query


def remove_buddie(
        request: WSGIRequest,
        user_username: str,
        buddie_username: str
        ) -> HttpResponseRedirect:
    """Removes buddie from a user's BlastBuddies

    Removes a buddie from a users buddie list. Then redirects to the
    same page to reload the blast buddie list now excluding the new
    buddie.

    :param request: Django request object
    :type request: WSGIRequest
    :param user_username: the username of the user logged in
    :type user_username: str
    :param buddie_username: the username of the user needed to be 
    removed from the buddie list of the logged in user
    :type buddie_username: str
    :return: redirects back to personalia page after removing buddie
    :rtype: redirect
    """
    user = get_object_or_404(User, username = user_username)
    buddie = get_object_or_404(User, username = buddie_username)
    if hasattr(user, 'blastbuddies_as_user'):
        user.blastbuddies_as_user.buddie.remove(buddie)
    return redirect("/personalia")


def search_user(request: WSGIRequest) -> JsonResponse:
    """Gives the searched user if it exist

    Used to get the account you search for in blast buddie club. Then 
    returns this username if it exists. If the username doesn't exist,
    returns an empty list.

    :param request: Django request object
    :type request: WSGIRequest
    :return: a JsonResponse with a list with the found user 
             or an empty list if the user didn't exist.
    :rtype: JsonResponse
    """
    username = request.GET['name']
    # user name needs to specificly be the same
    users = User.objects.filter(username = username)
    user_list = [{'username': user.username, 'email': user.email}
                for user in users]
    return JsonResponse({'users': user_list})


def add_buddie(request: WSGIRequest, buddie_username: str) -> HttpResponseRedirect:
    """Adds buddie as buddie

    Adds a buddie from a users buddie list. Then redirects to the same 
    page to reload the blast buddie list now including the new buddie.

    :param request: Django request object
    :type request: WSGIRequest
    :param buddie_username: the username of the user needed to be 
    added from the buddie list of the logged in user
    :type buddie_username: str
    :return: redirects back to personalia page after adding buddie
    :rtype: redirect
    """
    user = None
    if request.user.is_authenticated:
        user = request.user

    if user is not None:
        buddie = get_object_or_404(User, username = buddie_username)
        blast_buddies_instance, created = \
            BlastBuddies.objects.get_or_create(user = user)
        blast_buddies_instance.buddie.add(buddie)

    return redirect("/personalia")
