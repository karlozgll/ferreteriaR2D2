from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField, TextAreaField, FloatField, IntegerField, SelectField
from wtforms_html5 import DateField, DateRange
from wtforms_html5 import Length
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange
from ferreteria.models import Usuario, Cliente, Proveedor, Producto, Unidad, Categoria, Compra, DetalleCompra, Venta, DetalleVenta
from sqlalchemy import or_, and_
from datetime import date

class LoginForm(FlaskForm):
    nickname = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar Sesión')

class RegUsuarioForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    nickname = StringField('Nombre de Usuario', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Contraseña')
    submit = SubmitField('Guardar')

    def validate_nickname(self, nickname): #VALIDACION DE USUARIO EXISTENTE
        usuario=Usuario.query.filter_by(nickname=nickname.data).first()
        if usuario:
            raise ValidationError(f'El nombre de usuario "{nickname.data}" ya está en uso')

    def validate_email(self, email): #VALIDACION DE USUARIO EXISTENTE
        usuario=Usuario.query.filter_by(email=email.data).first()
        if usuario:
            raise ValidationError('Este correo ya está en uso')

class RegClienteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(min=2, max=50)])
    direccion = StringField('Direccion', validators=[DataRequired(), Length(min=2, max=80)])
    celular = IntegerField('Celular', validators=[DataRequired()])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    submit = SubmitField('Guardar')

    def validate_email(self, email): #VALIDACION DE USUARIO EXISTENTE
        cliente=Cliente.query.filter_by(email=email.data).first()
        if cliente:
            raise ValidationError('Este correo ya está en uso')

class RegProveedorForm(FlaskForm):
    razonSocial = StringField('Razón Social', validators=[DataRequired(), Length(min=2, max=80)])
    direccion = StringField('Direccion', validators=[DataRequired(), Length(min=2, max=80)])
    celular = IntegerField('Celular', validators=[DataRequired()])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    submit = SubmitField('Guardar')

    def validate_email(self, email): #VALIDACION DE USUARIO EXISTENTE
        proveedor=Proveedor.query.filter_by(email=email.data).first()
        if proveedor:
            raise ValidationError('Este correo ya está en uso')

    def validate_razonSocial(self, razonSocial): #VALIDACION DE USUARIO EXISTENTE
        proveedor=Proveedor.query.filter_by(razon_social=razonSocial.data).first()
        if proveedor:
            raise ValidationError(f'Ya existe un proveedor con el nombre de "{razonSocial.data}"')
    
class RegProductoForm(FlaskForm):
    categoria = SelectField('Seleccione la categoría', validate_choice=False)
    unidad = SelectField('Seleccione la unidad', validate_choice=False)
    proveedor = SelectField('Seleccione proveedor', validate_choice=False)
    nombre = StringField('Direccion', validators=[DataRequired(), Length(min=2, max=50)])
    precioCompra = FloatField('Precio de Compra', validators=[DataRequired()])
    precioVenta = FloatField('Precio de Venta', validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired()])
    submit = SubmitField('Guardar')