import xlrd, csv, pandas, pprint as pp

from django.shortcuts import render,render_to_response
from django.template import RequestContext
from django.db import IntegrityError
from django.contrib import messages
from django.views import generic
from django.core.urlresolvers import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse
from datapoints.mixins import PermissionRequiredMixin


from pandas.io.excel import read_excel

from source_data.forms import *
from source_data.models import *
from source_data.etl_tasks.ingest_document import DocIngest
from source_data.etl_tasks.pre_process_document import pre_process_xls


def file_upload(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            newdoc = Document(docfile = request.FILES['docfile'])
            newdoc.created_by = request.user
            newdoc.save()
            document_id = newdoc.id

            file_path = newdoc.docfile.url

            if file_path.endswith('xls') or file_path.endswith('xlsx'):

                ## FIND MAPPINGS ##
                df, mappings = pre_process_xls(file_path,newdoc.id)

                ## MOVE XLS INTO DATAPOINTS TABLE ##
                current_user_id = request.user.id
                d = DocIngest(document_id,mappings,df,current_user_id)
                # process_sheet_df(df,document_id,mappings)

                return document_review(request,newdoc.id,mappings)

            # if file is csv...

            else:
                messages.add_message(request, messages.INFO, 'Please\
                    upload either .CSV, .XLS or .XLSX file format')

    else:
        form = DocumentForm()

    return render_to_response(
        'upload/file_upload.html',
        {'form': form},
        context_instance=RequestContext(request)
    )



def document_review(request,document_id,mappings):

    doc_data = []

    r =  {'problem':'Indicators to Map','recs':len(mappings['indicators']),'model':'indicator'}
    r2 = {'problem':'Campaigns to Map','recs':len(mappings['campaigns']),'model':'campaign'}
    r3 = {'problem':'Regions To Map','recs':len(mappings['regions']),'model':'region'}

    doc_data.append(r)
    doc_data.append(r2)
    doc_data.append(r3)


    return render_to_response(
        'upload/document_review.html',
        {'doc_data': doc_data},
        context_instance=RequestContext(request),
    )


######### META MAPPING ##########


class CreateMap(PermissionRequiredMixin, generic.CreateView):

    template_name='map/map.html'
    success_url=reverse_lazy('datapoints:datapoint_index')
    # permission_required = 'datapoints.add_datapoint'

    def form_valid(self, form):
    # this inserts into the changed_by field with  the user who made the insert
        obj = form.save(commit=False)
        obj.mapped_by = self.request.user
        # obj.source_id = Source.objects.get(source_name='data entry').id
        obj.save()
        return HttpResponseRedirect(self.success_url)


class IndicatorMapCreateView(CreateMap):

    model=IndicatorMap
    form_class = IndicatorMapForm
    context_object_name = 'indicator_to_map'
    template_name = 'map/map.html'
    success_url=reverse_lazy('source_data:to_map')



    def get_initial(self):
        return { 'source_indicator': self.kwargs['pk'] }



class RegionMapCreateView(CreateMap):

    model=RegionMap
    form_class = RegionMapForm


class CampaignMapCreateView(CreateMap):

    model=CampaignMap
    form_class = CampaignMapForm


class ToMap(generic.ListView):

    model = SourceIndicator
    template_name = 'map/to_map.html'
    context_object_name = 'items'

    def get_queryset(self):

        return SourceIndicator.objects.filter(indicatormap__isnull=True)



class ShowSourceIndicator(generic.DetailView):

    context_object_name = "source_indicator"
    template_name = 'map/source_indicator.html'
    model = SourceIndicator
