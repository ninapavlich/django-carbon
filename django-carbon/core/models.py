from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now

from ..models import *

class Tag(Versionable, Addressible, Publishable, Accessible):

    class Meta:
        abstract = True

class TagItemOrder(models.Model):
    def get_tag_model():
        return settings.TAG_MODEL

    tag = models.ForeignKey(get_tag_model(), related_name='%(class)s_tag')
    order = models.IntegerField(default=0)

    # Related item
    content_type = models.ForeignKey(ContentType,
             verbose_name=_('content type'),
            related_name="content_type_set_for_%(class)s")
    object_pk = models.TextField(_('object ID'))
    content_object = generic.GenericForeignKey(ct_field="content_type", 
        fk_field="object_pk")

    unique_together = ((tag,content_object))

    class Meta:
        abstract = True
        ordering = ['tag','order']


    @staticmethod
    def get_items(tag):
        return TagItemOrder.objects.filter(tag=tag).order_by('order')


class Article(Versionable, Addressible, Publishable, Accessible, Categorizable, Content):
    class Meta:
        abstract = True

class Comment(Versionable, Addressible, Publishable, Accessible, Content, UserInput):
    class Meta:
        abstract = True


class Location(models.Model):
    help = {
        'latitude': "",
        'longitude': "",
    }

    latitude = models.CharField(_('Latitude'), max_length=255, 
        blank=True, null=True, help_text=help['latitude'])
    longitude = models.CharField(_('Longitude'), max_length=255, 
        blank=True, null=True, help_text=help['longitude'])

    class Meta:
        abstract = True

    @staticmethod
    def create_from_request(request):
        #TODO -- integrate with an ip-location lookup
        location = Location(
            latitude='0',
            longitude='0'
        )
        location.save()
        return location

    @staticmethod
    def create_from_address(address, type=None):
        #TODO -- integrate with an address-location lookup
        location = Location(
            latitude='0',
            longitude='0'
        )
        location.save()
        return location



class Tracking(Versionable):

    help = {
        'tracking_type': "",
        'tracking_ip_address': "",
        'tracking_session_key': "",
        'tracking_location':"",
        'tracking_user':""
    }

    
    tracking_type = models.CharField(_('Tracking Type'), max_length=255, 
        blank=True, null=True, help_text=help['tracking_type'])

    tracking_ip_address = models.CharField(_('Tracking IP Address'), max_length=255, 
        blank=True, null=True, help_text=help['tracking_ip_address'])

    tracking_session_key = models.CharField(_('Tracking Session Key'), max_length=255, 
        blank=True, null=True, help_text=help['tracking_session_key'])

    tracking_location = models.ForeignKey('Location',
        blank=True, null=True, help_text=help['tracking_location'])

    tracking_user = models.ForeignKey(settings.AUTH_USER_MODEL,
        blank=True, null=True, help_text=help['tracking_user'])

    # Related item
    content_type = models.ForeignKey(ContentType,
             verbose_name=_('content type'),
            related_name="content_type_set_for_%(app_label)s_%(class)s")
    object_pk = models.TextField(_('object ID'))
    content_object = generic.GenericForeignKey(ct_field="content_type", 
        fk_field="object_pk")

    class Meta:
        abstract = True

    @staticmethod
    def track_item(item, request, tracking_type=None):
        ipaddress = request.META.get("REMOTE_ADDR", None)
        tracking_location = settings.LOCATION_MODEL.create_from_request(request)
        tracking_user = request.user
        track = Tracking(
            content_object=item,
            tracking_type=tracking_type,
            tracking_ip_address = ipaddress,
            tracking_session_key = request.session.session_key,
            tracking_location = tracking_location,
            tracking_user = request.user,            
        )
        track.save()
        return track



def media_file_name( instance, filename ):
    """Generate Document File Name"""

    file, extension = os.path.splitext( filename )
    use_title = instance.title if instance.title else file
    short_title = slugify(use_title[:50])
    
    filename        = "%s-%s%s" % ( short_title, str( time.time() )[0:10], extension )
    filename        = filename.lower()
    return '/'.join( [ 'media',filename ] )

class Media( Versionable ):

    image = models.CharField(_("image"), max_length=255, blank=True)#models.ImageField(upload_to=media_file_name)
    
    title = models.CharField(_("title"), max_length=255, blank=True)
    credit = models.CharField(_("Credit"), max_length=255, blank=True)
    caption = models.TextField(_("Caption"), blank = True )

    class Meta:
        abstract = True
    
    @staticmethod
    def autocomplete_search_fields():
        return ("id__iexact", "title__icontains", "credit__icontains","caption__icontains",'admin_note__icontains')

    def get_admin_thumbnail(self):
        #OVERRIDE
        return self.image

    def get_image_variant(self, size):
        return self.image

    def __unicode__(self):
        if self.title:
            return ("%s")%(self.title)
        elif self.caption:
            return ("%s %s")%(self.caption, self.credit)
        else:
            return ("Image %s")%(self.pk)

        
class Image( Media ):

    class Meta:
        abstract = True
    

class Document( Media ):

    document = models.FileField(upload_to=media_file_name, blank=True)
    
    class Meta:
        abstract = True