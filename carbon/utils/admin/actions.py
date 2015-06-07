from django.utils import timezone
from django.contrib import messages

from ..data.csv import ModelToCSV

#ADMIN VIEWS 



def resave_item(modeladmin, request, queryset):	

	items_saved = 0
	save_errors = 0
	for item in queryset:
	    try:
	    	item.save()
	    	items_saved += 1
	    except:
	    	save_errors += 1

	if items_saved > 0:
	 	messages.success(request, '%s items were saved.'%(items_saved))

	if save_errors > 0:
		messages.warning(request, '%s items were not saved.'%(save_errors))
resave_item.short_description = "Re-Save"


def output_csv(modeladmin, request, queryset):
	
	try:

		verbose_name = modeladmin.model._meta.verbose_name_plural.title()
		now = timezone.now()
		now_string ="%s-%s-%s" % (now.year, str(now.month).zfill(2), str(now.day).zfill(2))
		filename = "%s_%s.csv" % (verbose_name, now_string)

		return ModelToCSV(request, queryset, modeladmin.csv_fields, filename=filename)

	except:
		messages.warning(request, 'There are no CSV fields specified for this model')
output_csv.short_description = "Output to CSV"    