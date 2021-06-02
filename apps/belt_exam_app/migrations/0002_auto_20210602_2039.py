# Generated by Django 2.2.4 on 2021-06-02 20:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('belt_exam_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Thought',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thought_text', models.TextField(max_length=1000, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('thoughted_by', models.CharField(max_length=255, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thoughts_posted', to='belt_exam_app.User')),
                ('favouriting_users', models.ManyToManyField(related_name='favourite_thoughts', to='belt_exam_app.User')),
            ],
        ),
        migrations.DeleteModel(
            name='Quote',
        ),
    ]
