<%namespace name="util" file="../util.mako"/>
<% from clld_morphology_plugin import models %>
<% from clld.db.models import common %>

<div class="tabbable">

    <ul class="nav nav-tabs">
        <li class="active"><a href="#morphs" data-toggle="tab"> Morphs </a></li>
        <li><a href="#wordforms" data-toggle="tab"> Wordforms </a></li>
        <li><a href="#forms" data-toggle="tab"> Forms </a></li>
        <li><a href="#lexemes" data-toggle="tab"> Lexemes </a></li>
        <li ><a href="#stems" data-toggle="tab"> Stems </a></li>
        <li><a href="#sentences" data-toggle="tab"> Sentences </a></li>
    </ul>

    <div class="tab-content" style="overflow: visible;">

        <div id="morphs" class="tab-pane active">
            ${request.get_datatable('morphs', models.Morph,contribution=ctx).render()}
        </div>

        <div id="wordforms" class="tab-pane">
            ${request.get_datatable('wordforms', models.Wordform,contribution=ctx).render()}
        </div>

        <div id="forms" class="tab-pane">
            ${request.get_datatable('forms', models.Form,contribution=ctx).render()}
        </div>

        <div id="lexemes" class="tab-pane">
            ${request.get_datatable('lexemes', models.Lexeme,contribution=ctx).render()}
        </div>

        <div id="stems" class="tab-pane">
            ${request.get_datatable('stems', models.Stem,contribution=ctx).render()}
        </div>

        <div id="sentences" class="tab-pane">
            ${request.get_datatable('sentences', common.Sentence,contribution=ctx).render()}
        </div>

    </div>

</div>