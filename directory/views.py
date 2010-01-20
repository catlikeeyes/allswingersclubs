from django.shortcuts import render_to_response
from django.http import HttpResponsePermanentRedirect
from allswingersclubs.directory.templatetags.my_slugify import my_slugify
from django.core.urlresolvers import reverse
from allswingersclubs.directory.models import *
from django.contrib.flatpages.models import FlatPage
from django.template import RequestContext

def index(request):
	all_states_list = State.objects.all()
	flatpages = FlatPage.objects.all()
	return render_to_response(
		'directory/index.html',
		{
			'all_states_list': all_states_list,
			'flatpages': flatpages,
		},
		context_instance=RequestContext(request),
	)
	
def state(request, state_usps_name):
	current_state = State.objects.filter(usps_name__exact=state_usps_name).get()
	all_clubs_for_state = Club.objects.select_related('state','city').filter(state__usps_name__exact=state_usps_name).order_by('name')
	empty_cities = City.objects.filter(state__usps_name__exact=state_usps_name,club__name__isnull=True)
	
	all_states_list = State.objects.all()
	return render_to_response(
		'directory/state.html',
		{
			'state': current_state,
			'clubs_list': all_clubs_for_state,
			'empty_cities': empty_cities,
			'all_states_list': all_states_list,
		},
		context_instance=RequestContext(request),
	)

	
def club(request, club_id, club_urlsafe_title):
	current_club = Club.objects.select_related('state','city').filter(id__exact=club_id).get()
	real_club_urlsafe_title=my_slugify(current_club.name)
	if(club_urlsafe_title != real_club_urlsafe_title):
		return HttpResponsePermanentRedirect(
			current_club.get_absolute_url()
		)
	else:
		current_club.photos = current_club.photo_set.all()
		all_clubs_for_state = Club.objects.filter(state__usps_name__exact=current_club.state.usps_name)
		return render_to_response(
			'directory/club.html',
			{
				'club': current_club,
				'clubs_list': all_clubs_for_state,
			},
			context_instance=RequestContext(request),
		)
