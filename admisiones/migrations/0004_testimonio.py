from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('admisiones', '0003_multimedia'),
    ]

    operations = [
        migrations.CreateModel(
            name='Testimonio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contenido', models.TextField(max_length=500)),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('aprobado', models.BooleanField(default=False)),
                ('autor', models.ForeignKey('admisiones.Usuario', on_delete=models.CASCADE)),
            ],
        ),
    ]