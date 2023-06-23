<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "cognatesets" %>


<h3>${_('Cognate set')} ${ctx.description}</h3>

<table class="table table-nonfluid">
    <tbody>
        % if ctx.contribution:
            <tr>
                <td>Contribution:</td>
                <td>${h.link(request, ctx.contribution)}</td>
            </tr>
        % endif
        % if ctx.source:
            <tr>
                <td> Source:</td>
                <td>${h.link(request, ctx.source)}</td>
            </tr>
        % endif
        ## % if ctx.description:
        ##     <tr>
        ##         <td> Description:</td>
        ##         <td>${ctx.description}</td>
        ##     </tr>
        ## % endif
   </tbody>
</table>

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

<script src="http://127.0.0.1:6543/static/alignment.js"></script>
<link rel="stylesheet" href="http://127.0.0.1:6543/static/alignment.css" type="text/css"/>
<script>
    $( document ).ready(function() {
        var alignments = document.getElementsByClassName("alignment");
        for (var i=0,alignment; alignment=alignments[i]; i++) {
            alignment.innerHTML = plotWord(alignment.innerHTML, 'span');
        }
    });
</script>

% if request.map:
    ${request.map.render()}
% endif