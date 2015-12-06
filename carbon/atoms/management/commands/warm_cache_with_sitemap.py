import lxml.etree
import requests
import datetime

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):

        from datetime import datetime
        startTime = datetime.now()
        current_site = Site.objects.get_current()
        protocol = 'http' if not settings.USE_SSL else 'https'
        url = '%s://%s'%(protocol, current_site.domain)
        sitemap_urls = get_sitemap_urls(url)

        print "Found %s URLs to load from %s"%(len(sitemap_urls), url)
        counter = 0
        for url in sitemap_urls:
            retrieve_content(url)
            counter += 1
            print "Loaded %s of %s (%s)"%(counter, len(sitemap_urls), url)

        print "Finished loading %s sitemap URLs in %s"%(len(sitemap_urls), datetime.now() - startTime)

    
    
def get_sitemap_urls(domain):
    sitemaps = read_robots(domain)
    urls = []   
    for sitemap_url in sitemaps:
        urls += process_sitemap(sitemap_url)

    return urls


def read_robots(domain):
    
    robots_url = '%s/robots.txt'%(domain.strip("/"))
    robots_content = retrieve_content(robots_url)
    sitemaps = []


    if robots_content:
        for line in robots_content.split('\n'):
            line = line.strip()

            if line.lower().startswith('sitemap:'):
                sitemaps.append(line[len('Sitemap:'):].strip())

    return sitemaps


    
def process_sitemap(sitemap_link):    
    
    namespaces = [
        ('sm', 'http://www.sitemaps.org/schemas/sitemap/0.9'),
    ]
    
    sitemap_content = retrieve_content(sitemap_link)
    if not sitemap_content:
        return []

    urls = []
    xml = sitemap_content.encode('utf-8')
    parser = lxml.etree.XMLParser(ns_clean=True, recover=True, encoding='utf-8')
    tree = lxml.etree.fromstring(xml, parser=parser)
    
    for sitemap in tree.xpath('//sm:sitemap | //sitemap', namespaces=namespaces):
        for loc in sitemap.xpath('sm:loc | loc', namespaces=namespaces):
            child_sitemap_url = loc.text.strip()
            child_sitemap_link = self.set.get_or_create_link_object(child_sitemap_url, sitemap_link)                
            self.sitemaps.append(child_sitemap_url)
    
    for sitemap in tree.xpath('//sm:url | //url', namespaces=namespaces):
        # TODO: add last update date, rank and update frequency
        for loc in sitemap.xpath('sm:loc | loc', namespaces=namespaces):
            url = loc.text.strip()
            urls.append(url)

    return urls


def retrieve_content(url):
    r = requests.get(url)
    return r.text