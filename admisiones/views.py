from .forms import MultimediaForm
from django.utils.decorators import method_decorator
from .forms import MensajeContactoForm
from .models import MensajeContacto
from django.contrib import messages

def contacto_view(request):
    if request.method == 'POST':
        form = MensajeContactoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Tu mensaje ha sido enviado exitosamente!')
            return redirect('contacto')
    else:
        form = MensajeContactoForm()
    return render(request, 'contacto.html', {'form': form})
from django.contrib.auth.decorators import login_required

def pagos_en_linea_view(request):
    return render(request, 'pagos_en_linea.html')
from .models import Testimonio
from .forms import TestimonioForm
from .forms import ComprobantePagoForm
from .models import ComprobantePago
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
@login_required
def comprobante_pago_view(request):
    if request.method == 'POST':
        form = ComprobantePagoForm(request.POST, request.FILES)
        if form.is_valid():
            comprobante = form.save(commit=False)
            comprobante.autor = request.user
            comprobante.save()
            return redirect('comprobante_pago')
    else:
        form = ComprobantePagoForm()
    comprobantes = ComprobantePago.objects.filter(autor=request.user).order_by('-fecha_subida')
    return render(request, 'comprobante_pago.html', {'form': form, 'comprobantes': comprobantes})
@login_required
def testimonios_view(request):
    testimonios = Testimonio.objects.filter(aprobado=True).order_by('-fecha')
    if request.method == 'POST':
        form = TestimonioForm(request.POST)
        if form.is_valid():
            testimonio = form.save(commit=False)
            testimonio.autor = request.user
            testimonio.aprobado = False  # Moderación
            testimonio.save()
            return redirect('testimonios')
    else:
        form = TestimonioForm()
    return render(request, 'testimonios.html', {'testimonios': testimonios, 'form': form})
from .models import Multimedia
from django.views.generic import ListView



@method_decorator(login_required, name='dispatch')
class GaleriaMultimediaView(ListView):
    model = Multimedia
    template_name = 'galeria_multimedia.html'
    context_object_name = 'multimedia'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_staff:
            context['form'] = MultimediaForm()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect('galeria_multimedia')
        form = MultimediaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('galeria_multimedia')
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    paginate_by = 12
# Panel de administración visual (dashboard)
from django.contrib.admin.views.decorators import staff_member_required
@staff_member_required
def dashboard_panel_admin(request):
    from .models import Usuario, Hijo, Tarea, Calificacion, Evento, Noticia
    total_usuarios = Usuario.objects.count()
    total_padres = Usuario.objects.filter(rol='padre').count()
    total_profesores = Usuario.objects.filter(rol='profesor').count()
    total_hijos = Hijo.objects.count()
    total_tareas = Tarea.objects.count()
    total_calificaciones = Calificacion.objects.count()
    total_eventos = Evento.objects.count()
    total_noticias = Noticia.objects.count()
    context = {
        'total_usuarios': total_usuarios,
        'total_padres': total_padres,
        'total_profesores': total_profesores,
        'total_hijos': total_hijos,
        'total_tareas': total_tareas,
        'total_calificaciones': total_calificaciones,
        'total_eventos': total_eventos,
        'total_noticias': total_noticias,
    }
    return render(request, 'dashboard_panel_admin.html', context)
# Panel de usuario personalizado
from django.contrib.auth.decorators import login_required
@login_required
def panel_usuario(request):
    usuario = request.user
    hijos = None
    tareas = None
    calificaciones = None
    if usuario.rol == 'padre':
        from .models import Hijo, PadreHijo, Calificacion
        hijos = Hijo.objects.filter(padrehijo__padre=usuario)
        tareas = None
        calificaciones = Calificacion.objects.filter(hijo__in=hijos)
    elif usuario.rol == 'profesor':
        from .models import Tarea, Calificacion
        tareas = Tarea.objects.filter(profesor=usuario)
        calificaciones = Calificacion.objects.filter(profesor=usuario)
    context = {
        'usuario': usuario,
        'hijos': hijos,
        'tareas': tareas,
        'calificaciones': calificaciones,
    }
    return render(request, 'panel_usuario.html', context)
from .models import Usuario
from django.core.mail import send_mail
# Vista para recuperación de contraseña
from django.shortcuts import render, redirect
from django.contrib import messages
def recuperar_contrasena(request):
    from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
    from django.utils.encoding import force_bytes, force_str
    from django.contrib.auth.tokens import default_token_generator
    from django.urls import reverse
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            usuario = Usuario.objects.get(email=email)
            token = default_token_generator.make_token(usuario)
            uid = urlsafe_base64_encode(force_bytes(usuario.pk))
            reset_url = request.build_absolute_uri(
                reverse('admisiones:reset_password', kwargs={'uidb64': uid, 'token': token})
            )
            send_mail(
                'Recuperación de contraseña',
                f'Haz clic en el siguiente enlace para restablecer tu contraseña: {reset_url}',
                'no-reply@colegioninojesus.edu',
                [email],
                fail_silently=True,
            )
            messages.success(request, 'Se han enviado instrucciones a tu correo si existe una cuenta registrada.')
        except Usuario.DoesNotExist:
            messages.error(request, 'No existe una cuenta con ese correo electrónico.')
        return redirect('admisiones:recuperar_contrasena')
    return render(request, 'recuperar_contrasena.html')

# Vista para restablecer la contraseña con token seguro
def reset_password(request, uidb64, token):
    from django.contrib.auth.tokens import default_token_generator
    from django.utils.http import urlsafe_base64_decode
    from django.utils.encoding import force_str
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        usuario = Usuario.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Usuario.DoesNotExist):
        usuario = None
    if usuario is not None and default_token_generator.check_token(usuario, token):
        if request.method == 'POST':
            nueva_contrasena = request.POST.get('password')
            if nueva_contrasena and len(nueva_contrasena) >= 6:
                usuario.set_password(nueva_contrasena)
                usuario.save()
                messages.success(request, 'Tu contraseña ha sido restablecida correctamente.')
                return redirect('admisiones:login_usuario')
            else:
                messages.error(request, 'La contraseña debe tener al menos 6 caracteres.')
        return render(request, 'reset_password.html', {'validlink': True})
    else:
        return render(request, 'reset_password.html', {'validlink': False})
from django.contrib.auth.decorators import login_required
from .forms import NotificacionForm
from .models import Notificacion

# Vista para crear notificaciones internas
@login_required
def crear_notificacion(request):
    if not (request.user.rol == 'profesor' or request.user.is_staff):
        messages.error(request, 'Solo administradores y profesores pueden crear notificaciones.')
        return redirect('admisiones:inicio')
    if request.method == 'POST':
        form = NotificacionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Notificación creada y enviada correctamente.')
            return redirect('admisiones:inicio')
    else:
        form = NotificacionForm()
    return render(request, 'notificaciones/crear_notificacion.html', {'form': form})
from django.shortcuts import render
# Panel de profesor
@login_required
def panel_profesor(request):
    if hasattr(request.user, 'rol') and request.user.rol == 'profesor':
        return render(request, 'panel_profesor.html')
    else:
        messages.error(request, 'Solo los profesores pueden acceder a este panel.')
        return redirect('admisiones:inicio')
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

# Redirección para /calificaciones/
@login_required
def calificaciones_redirect(request):
    if request.user.rol == 'profesor':
        return redirect('admisiones:lista_calificaciones_profesor')
    elif request.user.rol == 'padre':
        return redirect('admisiones:calificaciones_hijos_padre')
    else:
        return redirect('admisiones:inicio')

# Redirección para /tareas/
@login_required
def tareas_redirect(request):
    if request.user.rol == 'profesor':
        return redirect('lista_tareas_profesor')
    elif request.user.rol == 'padre':
        return redirect('tareas_grado_padre')
    else:
        return redirect('inicio')
from .forms import TareaForm, CalificacionForm
from .models import Tarea, Calificacion, Hijo, PadreHijo
from django.contrib.auth.decorators import login_required

# Vista para que profesores creen tareas
@login_required
def crear_tarea(request):
    if request.user.rol != 'profesor':
        messages.error(request, 'Solo los profesores pueden crear tareas.')
        return redirect('inicio')
    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            tarea = form.save(commit=False)
            tarea.profesor = request.user
            tarea.save()
            messages.success(request, 'Tarea creada correctamente.')
            return redirect('lista_tareas_profesor')
    else:
        form = TareaForm()
    return render(request, 'tareas/crear_tarea.html', {'form': form})

# Vista para que profesores asignen calificaciones
@login_required
def asignar_calificacion(request):
    if request.user.rol != 'profesor':
        messages.error(request, 'Solo los profesores pueden asignar calificaciones.')
        return redirect('inicio')
    if request.method == 'POST':
        form = CalificacionForm(request.POST)
        if form.is_valid():
            calificacion = form.save(commit=False)
            calificacion.profesor = request.user
            calificacion.save()
            messages.success(request, 'Calificación asignada correctamente.')
            return redirect('lista_calificaciones_profesor')
    else:
        form = CalificacionForm()
    return render(request, 'tareas/asignar_calificacion.html', {'form': form})

# Vista para que profesores vean sus tareas
@login_required
def lista_tareas_profesor(request):
    if request.user.rol != 'profesor':
        messages.error(request, 'Solo los profesores pueden ver esta lista.')
        return redirect('inicio')
    tareas = Tarea.objects.filter(profesor=request.user)
    return render(request, 'tareas/lista_tareas_profesor.html', {'tareas': tareas})

# Vista para que profesores vean sus calificaciones asignadas
@login_required
def lista_calificaciones_profesor(request):
    if request.user.rol != 'profesor':
        messages.error(request, 'Solo los profesores pueden ver esta lista.')
        return redirect('inicio')
    calificaciones = Calificacion.objects.filter(profesor=request.user)
    return render(request, 'tareas/lista_calificaciones_profesor.html', {'calificaciones': calificaciones})

# Vista para que padres vean tareas de su grado
@login_required
def tareas_grado_padre(request):
    if request.user.rol != 'padre':
        messages.error(request, 'Solo los padres pueden ver tareas de grado.')
        return redirect('inicio')
    hijos = Hijo.objects.filter(padrehijo__padre=request.user)
    grados = hijos.values_list('grado', flat=True)
    tareas = Tarea.objects.filter(grado__in=grados)
    return render(request, 'tareas/tareas_grado_padre.html', {'tareas': tareas})

# Vista para que padres vean calificaciones de sus hijos
@login_required
def calificaciones_hijos_padre(request):
    if request.user.rol != 'padre':
        messages.error(request, 'Solo los padres pueden ver calificaciones de hijos.')
        return redirect('inicio')
    hijos = Hijo.objects.filter(padrehijo__padre=request.user)
    calificaciones = Calificacion.objects.filter(hijo__in=hijos)
    return render(request, 'tareas/calificaciones_hijos_padre.html', {'calificaciones': calificaciones})
from .forms import RegistroHijoForm
from .models import Hijo, PadreHijo

# Vista para registrar hijos y vincularlos al padre autenticado
from django.contrib.auth.decorators import login_required
@login_required
def registrar_hijo(request):
    if request.user.rol != 'padre':
        messages.error(request, 'Solo los padres pueden registrar hijos.')
        return redirect('inicio')
    if request.method == 'POST':
        form = RegistroHijoForm(request.POST)
        if form.is_valid():
            hijo = form.save()
            PadreHijo.objects.create(padre=request.user, hijo=hijo)
            messages.success(request, f'Hijo {hijo.nombre} registrado y vinculado correctamente.')
            return redirect('inicio')
    else:
        form = RegistroHijoForm()
    return render(request, 'registration/registrar_hijo.html', {'form': form})
from django.contrib.auth import authenticate, login
from .forms import LoginUsuarioForm

# Vista de login personalizado para padres/profesores
def login_usuario(request):
    if request.method == 'POST':
        form = LoginUsuarioForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'Bienvenido, {}!'.format(user.username))
                return redirect('inicio')
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = LoginUsuarioForm()
    return render(request, 'registration/login.html', {'form': form})
from .forms import RegistroUsuarioForm

# Vista para registro de usuario (padre/profesor)
def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            usuario = form.save(commit=False)
            usuario.set_password(form.cleaned_data['password'])
            usuario.save()
            messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
            return redirect('admisiones:login_usuario')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'registration/registro.html', {'form': form})
def padres_estudiantes(request):
    return render(request, 'padres_estudiantes.html')
def mapa(request):
    return render(request, 'mapa.html')
def recursos(request):
    return render(request, 'recursos.html')
def testimonios(request):
    return render(request, 'testimonios.html')
def calendario_escolar(request):
    return render(request, 'calendario.html')
def galeria_multimedia(request):
    return render(request, 'galeria.html')
def institucional(request):
    return render(request, 'institucional.html')
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.utils.text import slugify
from django.db import IntegrityError, transaction
from .models import Noticia, Evento, GaleriaImagen
from .forms import EventoForm

# Mixin para verificar si el usuario es administrador
class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        request = getattr(self, 'request', None)
        if request:
            return request.user.is_staff
        return False

    def handle_no_permission(self):
        request = getattr(self, 'request', None)
        if request:
            messages.error(request, 'No tienes permiso para acceder a esta página.')
        return redirect('inicio')

class InicioView(TemplateView):
    template_name = 'inicio.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['noticias_destacadas'] = Noticia.objects.filter(
            fecha_publicacion__lte=timezone.now()
        ).order_by('-fecha_publicacion')[:3]
        context['eventos_proximos'] = Evento.objects.filter(
            fecha_inicio__gte=timezone.now()
        ).order_by('fecha_inicio')[:3]
        # Notificaciones internas para el usuario autenticado
        request = self.request
        if request.user.is_authenticated:
            from .models import Notificacion
            context['notificaciones'] = Notificacion.objects.filter(destinatario=request.user).order_by('-fecha_creacion')[:5]
        else:
            context['notificaciones'] = []
        return context

class NoticiaListView(ListView):
    model = Noticia
    template_name = 'noticias/lista.html'
    context_object_name = 'noticias'
    paginate_by = 10
    
    def get_queryset(self):
        return Noticia.objects.filter(fecha_publicacion__lte=timezone.now()).order_by('-fecha_publicacion')

class NoticiaDetailView(DetailView):
    model = Noticia
    template_name = 'noticias/detalle.html'
    context_object_name = 'noticia'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_object(self, queryset=None):
        queryset = self.get_queryset()
        slug = self.kwargs.get(self.slug_url_kwarg)
        pk = self.kwargs.get('pk')
        if slug:
            return get_object_or_404(queryset, slug=slug)
        elif pk:
            return get_object_or_404(queryset, pk=pk)
        else:
            raise AttributeError('No pk or slug provided for NoticiaDetailView')

    def get_queryset(self):
        return Noticia.objects.filter(fecha_publicacion__lte=timezone.now())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = context.get('object') or self.get_object()
        if getattr(obj, 'etiquetas', None):
            context['etiquetas'] = [tag.strip() for tag in obj.etiquetas.split(',') if tag.strip()]
        return context

class NoticiaCreateView(AdminRequiredMixin, CreateView):
    model = Noticia
    fields = ['titulo', 'contenido', 'imagen_principal', 'destacada', 'etiquetas']
    template_name = 'noticias/noticia_form.html'
    
    def form_valid(self, form):
        form.instance.autor = self.request.user
        
        # Generate slug from title
        base_slug = slugify(form.instance.titulo)
        form.instance.slug = base_slug
        
        # Ensure slug is unique
        counter = 1
        while True:
            try:
                with transaction.atomic():
                    response = super().form_valid(form)
                    messages.success(self.request, 'La noticia se ha creado correctamente.')
                    return response
            except IntegrityError:
                counter += 1
                form.instance.slug = f"{base_slug}-{counter}"
    
    def get_success_url(self):
        obj = getattr(self, 'object', None) or self.get_object()
        return reverse_lazy('admisiones:noticia_detalle', kwargs={'pk': obj.pk})

class EventoListView(ListView):
    model = Evento
    template_name = 'eventos/lista.html'
    context_object_name = 'eventos'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Evento.objects.all().order_by('fecha_inicio')
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proximo_evento'] = Evento.proximo_evento()
        context['eventos_proximos'] = Evento.eventos_proximos()
        return context

class EventoDetailView(DetailView):
    model = Evento
    template_name = 'eventos/detalle.html'
    context_object_name = 'evento'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['proximo_evento'] = Evento.proximo_evento()
        return context

class EventoCreateView(AdminRequiredMixin, CreateView):
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/evento_form.html'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'El evento se ha creado correctamente.')
        return response
    
    def get_success_url(self):
        obj = getattr(self, 'object', None) or self.get_object()
        slug = getattr(obj, 'slug', None)
        if slug:
            return reverse_lazy('admisiones:evento_detalle', kwargs={'slug': slug})
        return reverse_lazy('admisiones:lista_eventos')

class EventoUpdateView(AdminRequiredMixin, UpdateView):
    model = Evento
    form_class = EventoForm
    template_name = 'eventos/evento_form.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'El evento se ha actualizado correctamente.')
        return response
    
    def get_success_url(self):
        obj = getattr(self, 'object', None) or self.get_object()
        slug = getattr(obj, 'slug', None)
        if slug:
            return reverse_lazy('admisiones:evento_detalle', kwargs={'slug': slug})
        return reverse_lazy('admisiones:lista_eventos')

class EventoDeleteView(AdminRequiredMixin, DeleteView):
    model = Evento
    template_name = 'eventos/evento_confirm_delete.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    success_url = reverse_lazy('admisiones:lista_eventos')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'El evento se ha eliminado correctamente.')
        return super().delete(request, *args, **kwargs)

