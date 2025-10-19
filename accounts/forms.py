from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


# ============================================
# FORMULAIRES D'AUTHENTIFICATION (EXISTANTS)
# ============================================

class SignUpForm(UserCreationForm):
    """Formulaire d'inscription"""
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom d\'utilisateur'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirmer le mot de passe'
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé.")
        return email


class LoginForm(forms.Form):
    """Formulaire de connexion"""
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nom d\'utilisateur'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Mot de passe'
        })
    )


# ============================================
# FORMULAIRES DE PROFIL (NOUVEAUX)
# ============================================

class UserUpdateForm(forms.ModelForm):
    """Formulaire de mise à jour des informations utilisateur"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom d\'utilisateur'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Prénom'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nom'
            }),
        }
        labels = {
            'username': 'Nom d\'utilisateur',
            'email': 'Email',
            'first_name': 'Prénom',
            'last_name': 'Nom',
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Vérifier si l'email existe déjà (sauf pour l'utilisateur actuel)
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé par un autre compte.")
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Vérifier si le username existe déjà (sauf pour l'utilisateur actuel)
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError("Ce nom d'utilisateur est déjà pris.")
        return username


class ProfileUpdateForm(forms.ModelForm):
    """Formulaire de mise à jour du profil utilisateur"""
    
    class Meta:
        model = Profile
        fields = ['phone', 'address']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+221 XX XXX XX XX',
                'maxlength': '20'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Votre adresse complète',
                'rows': 3
            }),
        }
        labels = {
            'phone': 'Numéro de téléphone',
            'address': 'Adresse',
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Validation basique du numéro de téléphone
        if phone:
            # Retirer les espaces et caractères spéciaux
            phone_digits = ''.join(filter(str.isdigit, phone))
            if len(phone_digits) < 9:
                raise forms.ValidationError("Le numéro de téléphone doit contenir au moins 9 chiffres.")
        return phone


class AvatarUpdateForm(forms.ModelForm):
    """Formulaire de mise à jour de l'avatar"""
    
    class Meta:
        model = Profile
        fields = ['avatar']
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        labels = {
            'avatar': 'Photo de profil',
        }

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        
        if avatar:
            # Vérifier la taille du fichier (max 5MB)
            if avatar.size > 5 * 1024 * 1024:
                raise forms.ValidationError("L'image ne doit pas dépasser 5 MB.")
            
            # Vérifier le type de fichier
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
            if avatar.content_type not in allowed_types:
                raise forms.ValidationError("Seuls les fichiers JPG, PNG et GIF sont acceptés.")
        
        return avatar


# ============================================
# FORMULAIRES SUPPLÉMENTAIRES (OPTIONNELS)
# ============================================

class ContactForm(forms.Form):
    """Formulaire de contact"""
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre nom'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre email'
        })
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sujet'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Votre message',
            'rows': 5
        })
    )


class PasswordResetRequestForm(forms.Form):
    """Formulaire de demande de réinitialisation de mot de passe"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Votre email'
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("Aucun compte n'est associé à cet email.")
        return email


class ProfileSettingsForm(forms.ModelForm):
    """Formulaire complet pour tous les paramètres du profil"""
    
    class Meta:
        model = Profile
        fields = [
            'phone', 
            'address', 
            'email_notifications', 
            'order_notifications', 
            'dark_mode'
        ]
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+221 XX XXX XX XX'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),
            'email_notifications': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'order_notifications': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'dark_mode': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }
        labels = {
            'phone': 'Téléphone',
            'address': 'Adresse',
            'email_notifications': 'Recevoir les notifications par email',
            'order_notifications': 'Recevoir les confirmations de commande',
            'dark_mode': 'Mode sombre',
        }