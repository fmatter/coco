<%namespace name="util" file="../util.mako"/>
<% from coco.models import Cognateset, FormCognate, MorphCognate, StemCognate %>

<div class="tabbable">

    <ul class="nav nav-tabs">
        <li class="active"><a href="#cognatesets" data-toggle="tab"> Cognate sets </a></li>
        <li><a href="#cognates" data-toggle="tab"> Cognates </a></li>
    </ul>

    <div class="tab-content" style="overflow: visible;">

        <div id="cognatesets" class="tab-pane active">
            ${request.get_datatable('cognatesets', Cognateset,contribution=ctx).render()}
        </div>

        <div id="cognates" class="tab-pane">
            Morphs:
            ${request.get_datatable('morphcognates', MorphCognate,contribution=ctx).render()}
            Forms:
            ${request.get_datatable('formcognates', FormCognate,contribution=ctx).render()}
            Stems:
            ${request.get_datatable('stemcognates', StemCognate,contribution=ctx).render()}
        </div>

    </div>

</div>