<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "cognatesets" %>


<h3>${_('Cognate set')}</h3>


<%util:table items="${ctx.reflexes}" args="item" options="${dict(bInfo=True)}">
    <%def name="head()">
        <th>Form</th>
        <th>Language</th>
        <th>Alignment</th>
    </%def>
    <td>${h.link(request, item.counterpart)}</td>
    <td>${h.link(request, item.counterpart.language)}</td>
    <td>
        <span class="alignment">${item.alignment}</span>
    </td>
</%util:table>