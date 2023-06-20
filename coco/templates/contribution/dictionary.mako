<%namespace name="util" file="../util.mako"/>
<% from clld_morphology_plugin import models %>
<% from clld.db.models import common %>

<div class="tabbable">

    <ul class="nav nav-tabs">
        <li class="active"><a href="#forms" data-toggle="tab"> Forms </a></li>
        <li><a href="#sentences" data-toggle="tab"> Sentences </a></li>
    </ul>

    <div class="tab-content" style="overflow: visible;">

        <div id="forms" class="tab-pane active">
            ${request.get_datatable('forms', models.Form,contribution=ctx).render()}
        </div>

        <div id="sentences" class="tab-pane">
            ${request.get_datatable('sentences', common.Sentence,contribution=ctx).render()}
        </div>

    </div>

</div>