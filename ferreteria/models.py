from ferreteria import db
from datetime import datetime
from sqlalchemy import func

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=False, nullable=False)
    apellido = db.Column(db.String(50), unique=False, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)
    nickname = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)

class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=False, nullable=False)
    apellido = db.Column(db.String(50), unique=False, nullable=False)
    direccion = db.Column(db.String(80), unique=False, nullable=False)
    celular = db.Column(db.Integer, unique=False, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)

class Proveedor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    razon_social = db.Column(db.String(80), unique=False, nullable=False)
    direccion = db.Column(db.String(80), unique=False, nullable=False)
    celular = db.Column(db.Integer, unique=False, nullable=False)
    email = db.Column(db.String(40), unique=True, nullable=False)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    unidad_id = db.Column(db.Integer, db.ForeignKey('unidad.id'), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)
    nombre = db.Column(db.String(50), unique=False, nullable=False)
    precio_compra = db.Column(db.Numeric(12,2), unique=False, nullable=False)
    precio_venta = db.Column(db.Numeric(12,2), unique=False, nullable=False)
    cantidad = db.Column(db.Integer, unique=False, nullable=False)
    fecha = db.Column(db.DateTime, default=func.now())

class Unidad(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=False, nullable=False)

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), unique=False, nullable=False)

class Compra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=func.now())
    total = db.Column(db.Numeric(12,2), unique=False, nullable=True)
    numero_comprobante = db.Column(db.Integer, unique=False, nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedor.id'), nullable=False)
    detalles = db.relationship('DetalleCompra',backref='compras',lazy=True)

class DetalleCompra(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, unique=False, nullable=False)
    precio_unitario = db.Column(db.Numeric(12,2), unique=False, nullable=False)
    compra_id = db.Column(db.Integer, db.ForeignKey('compra.id'), nullable=False)

class Venta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, default=func.now())
    descuento = db.Column(db.Numeric(12,2), unique=False, nullable=True)
    total = db.Column(db.Numeric(12,2), unique=False, nullable=True)
    numero_comprobante = db.Column(db.Integer, unique=False, nullable=False)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'), nullable=False)
    detalles = db.relationship('DetalleVenta',backref='ventas',lazy=True)

class DetalleVenta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)
    cantidad = db.Column(db.Integer, unique=False, nullable=False)
    precio_unitario = db.Column(db.Numeric(12,2), unique=False, nullable=False)
    venta_id = db.Column(db.Integer, db.ForeignKey('venta.id'), nullable=False)
