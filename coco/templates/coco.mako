<%inherit file="app.mako"/>
<link rel="stylesheet" href="${req.static_url('clld_document_plugin:static/clld-document.css')}"/>

##
## define app-level blocks:
##
<%block name="header">
    ##<a href="${request.route_url('dataset')}">
    ##    <img src="${request.static_url('coco:static/header.gif')}"/>
    ##</a>
</%block>

${next.body()}

<script src="${req.static_url('clld_document_plugin:static/clld-document.js')}"></script>
<script>
number_examples()
</script>