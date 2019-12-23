# Generated by Django 2.2.4 on 2019-09-02 15:49

from django.db import migrations


def set_upload_status(apps, schema_editor):
    Document = apps.get_model('document', 'Document')
    Task = apps.get_model('task', 'Task')

    documents = Document.objects.all()

    pending_files = Task.objects.filter(name='Load Documents',
        status__in=['PENDING']).values('metadata__file_name', 'upload_session_id')
    for file_data in pending_files:
        if 'file_name' in file_data and 'upload_session_id' in file_data:
            documents = documents.exclude(name=file_data['file_name'],
                                          upload_session_id=file_data['upload_session_id'])
    chunk_size = 100
    for n in range(0, documents.count(), chunk_size):
        documents_chunk = documents[n:n + chunk_size]
        for d in documents_chunk:
            d.metadata['upload_status'] = 'DONE'
        Document.objects.bulk_update(documents_chunk, ['metadata'])


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0151_move_document_table'),
        ('task', '0031_auto_20180725_1416')
    ]

    operations = [
        migrations.RunPython(set_upload_status, reverse_code=migrations.RunPython.noop),
    ]