queryset_list = Post.objects.active()  # .order_by("-timestamp")
if request.user.studente.is_rappr_istituto or request.user.is_superuser:
	queryset_list = Post.objects.all()

query = request.GET.get("q")
if query:
	queryset_list = queryset_list.filter(
		Q(title__icontains = query) |
		Q(content__icontains = query) |
		Q(user__first_name__icontains = query) |
		Q(user__last_name__icontains = query)
	).distinct()
paginator = Paginator(queryset_list, 8)  # Show 25 contacts per page
page_request_var = "page"
page = request.GET.get(page_request_var)
try:
	queryset = paginator.page(page)
except PageNotAnInteger:
	# If page is not an integer, deliver first page.
	queryset = paginator.page(1)
except EmptyPage:
	# If page is out of range (e.g. 9999), deliver last page of results.
	queryset = paginator.page(paginator.num_pages)