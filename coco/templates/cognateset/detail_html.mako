<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>

<%! from coco.util import build_tree %>
<%! active_menu_item = "cognatesets" %>

<%def name="sidebar()">
    <%util:well title="${_('Overview')}">

        % if request.map:
    ${request.map.render()}
% endif

    </%util:well>
</%def>


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
        <tr>
            <td> Overview:</td>
            <td>${ build_tree(request, ctx)|n}</td>
        </tr>
   </tbody>
</table>

<h4>${_('Aligned cognates')}</h3>

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

<script src="${req.static_url('coco:static/alignment.js')}"></script>
<link rel="stylesheet" href="${req.static_url('coco:static/alignment.css')}" type="text/css"/>
<script>
    $( document ).ready(function() {
        var alignments = document.getElementsByClassName("alignment");
        for (var i=0,alignment; alignment=alignments[i]; i++) {
            alignment.innerHTML = plotWord(alignment.innerHTML, 'span');
        }
    });
</script>

## <div style="position: absolute; width: 100%; left: 0;">


## </div>