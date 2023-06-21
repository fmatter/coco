<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>

<%! active_menu_item = "contributions" %>
<%block name="title">${_('Contribution')} '${ctx.name}'</%block>

<h2>${_('Contribution')} '${ctx.name}'</h2>

By <ul class="taglist">
% for ctb in ctx.contributor_assocs:
    <li>${h.link(request, ctb.contributor)}</li>
% endfor
</ul>


% if ctx.id in ["yab-fm"]:
<%include file="rich.mako"/>
% elif ctx.id in ["tau-fm", "aka-fm"]:
<%include file="dictionary.mako"/>
% elif "cog" in ctx.id:
<%include file="comparative.mako"/>
% else:
<%include file="box.mako"/>
%endif
