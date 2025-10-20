# store/migrations/0005_add_redeem_code.py
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_accountproduct_rechargeproduct_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='redeem_code',
            field=models.CharField(
                max_length=50,
                blank=True,
                verbose_name='Code REDEEM',
                help_text='Code unique à fournir après achat (pour produits REDEEM uniquement)'
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='is_redeem_product',
            field=models.BooleanField(
                default=False,
                verbose_name='Produit REDEEM',
                help_text='Cocher si ce produit nécessite un code REDEEM'
            ),
        ),
        migrations.AddField(
            model_name='product',
            name='redeem_code_used',
            field=models.BooleanField(
                default=False,
                verbose_name='Code REDEEM utilisé',
                help_text='Indique si le code a déjà été vendu'
            ),
        ),
    ]