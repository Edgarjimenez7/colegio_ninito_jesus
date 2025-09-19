from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('admisiones', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Multimedia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descripcion', models.TextField(blank=True)),
                ('archivo', models.FileField(upload_to='galeria/')),
                ('tipo', models.CharField(max_length=10, choices=[('imagen', 'Imagen'), ('video', 'Video')])),
                ('fecha_subida', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]