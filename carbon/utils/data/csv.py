import csv

from django.http import HttpResponse

def get_repr(value): 
    if callable(value):
        return '%s' % value()
    return value

def get_field(instance, field):
    field_path = field.split('.')
    attr = instance
    for elem in field_path:
        try:
            attr = getattr(attr, elem)
        except AttributeError:
            return None
    return attr


def ModelToCSV(request, queryset, fields, filename="output.csv"):
	MANY_RELATED_MANAGER = "ManyRelatedManager"

	capitalized_fields = [w.replace("_", " ").replace("-", " ").replace("  ", " ").title() for w in fields]
	csv_data = []
	csv_data.append(capitalized_fields)

	
	# -- Rows
	for item in queryset:
		row = []
		for field in fields:

			if '__' in field:

				pieces = field.split('__')
				current_item = item


				for piece in pieces:
					if current_item:
						current_item = getattr(current_item, piece)

				row.append(unicode(current_item).encode("ascii", "ignore"))

			else:

				try:
					attr = get_repr(get_field(item, field))
					field_type = attr.__class__.__name__
					#row.append(unicode("CN: "+field_type).encode("utf-8"))			
					print "field_type: %s %s"%(field_type, field)

					if field_type == MANY_RELATED_MANAGER:
						ms = []
						for m in attr.all():
							ms.append(unicode(m).encode('ascii', 'ignore'))

						row.append(u'; '.join(ms).encode('ascii', 'ignore'))
					elif field_type == 'property':

						row.append(unicode(attr).encode("ascii", "ignore"))

					elif field_type == 'instancemethod':
						
						attr = getattr(item, field)()

						row.append(unicode(attr).encode("ascii", "ignore"))

					else:

						row.append(unicode(attr).encode("ascii", "ignore"))
					
				except:
					row.append(u"Not found")

		csv_data.append(row)

	return CSVResponse(request, csv_data, filename)


def ArrayToCSV(request, data, filename="output.csv"):	

	csv_data = []
	
	# -- Rows
	for fields in data:
		row = []
		for field in fields:
			try:
				row.append(unicode(field).encode("ascii", "ignore"))
			except:
				row.append(u"Not found")

		csv_data.append(row)

	return CSVResponse(request, csv_data, filename)

def CSVResponse(request, data, filename="output.csv"):
	# Create the HttpResponse object with the appropriate CSV header.

	#response = HttpResponse(content_type="text/plain")

	response = HttpResponse(content_type="text/csv")
	response['Content-Disposition'] = 'attachment; filename="'+filename+'"'
   

	writer = csv.writer(response)

	for line in data:
		writer.writerow(line)

	return response
