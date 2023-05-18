# Generated by Django 4.2.1 on 2023-05-17 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('preview_text', models.TextField()),
                ('article_url', models.URLField()),
                ('html_content', models.TextField()),
                ('plain_text_content', models.TextField()),
                ('published_date', models.DateField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-published_date'],
            },
        ),
    ]