# -*- coding:utf-8 -*-
from plone import api
from plone.api.exc import InvalidParameterError
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.interfaces import ISocialLikeSettings
from sc.social.like.utils import get_language
from urllib import urlencode
from zope.component import getMultiAdapter


class PluginView(BrowserView):

    gp_enabled = True
    language = 'en'

    plugin = ViewPageTemplateFile('templates/plugin.pt')
    link = ViewPageTemplateFile('templates/link.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.setup()

    def setup(self):
        portal_state = getMultiAdapter(
            (self.context, self.request), name=u'plone_portal_state')
        self.portal = portal_state.portal()
        self.site_url = portal_state.portal_url()
        self.portal_title = portal_state.portal_title()
        self.url = self.context.absolute_url()
        self.language = get_language(self.context)

    @property
    def typebutton(self):
        record = ISocialLikeSettings.__identifier__ + '.typebutton'
        try:
            typebutton = api.portal.get_registry_record(record)
        except InvalidParameterError:
            typebutton = ''

        if typebutton == 'horizontal':
            typebutton = 'medium'
        else:
            typebutton = 'tall'
        return typebutton

    def share_link(self):
        # Does we need any special language handler?
        # See https://developers.google.com/+/web/share/?hl=it#available-languages
        params = dict(
            url=self.context.absolute_url(),
            hl=self.language,
        )
        url = 'https://plus.google.com/share?' + urlencode(params)
        return url
