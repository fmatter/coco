<%inherit file="app.mako"/>

##
## define app-level blocks:
##
<%block name="header">
    ##<a href="${request.route_url('dataset')}">
    ##    <img src="${request.static_url('coco:static/header.gif')}"/>
    ##</a>
</%block>

${next.body()}

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