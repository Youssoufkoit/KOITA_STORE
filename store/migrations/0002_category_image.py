# store/migrations/0002_category_image.py
# Généré automatiquement - À créer avec: python manage.py makemigrations

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='categories/',
                verbose_name='Image de la catégorie',
                help_text='Image d\'illustration de la catégorie (recommandé: 400x300px)'
            ),
        ),
    ]