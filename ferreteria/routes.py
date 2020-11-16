from flask import render_template, flash, url_for, redirect, request, abort, make_response , jsonify
from ferreteria import app, db
from ferreteria.forms import RegUsuarioForm, RegProveedorForm, RegClienteForm, LoginForm, RegProductoForm
from ferreteria.models import Cliente, Usuario, Proveedor, Producto, Unidad, Categoria, Compra, DetalleCompra, Venta, DetalleVenta
from flask import send_from_directory
from datetime import datetime
from sqlalchemy import or_, and_
from fpdf import FPDF
import os
import json

@app.route("/home", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/", methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(nickname=form.nickname.data).first()
        if usuario:
            if usuario.password == form.password.data:
                flash(f'Bienvenido {usuario.nickname}!, has iniciado sesión con éxito', 'success')
                return redirect(url_for('home'))
            else:
                flash(f'Contraseña incorrecta para {usuario.nickname}', 'danger')
        else:
            flash(f'No existe este usuario', 'danger')
    return render_template("login.html", form=form)

#########-----------USUARIO -----------#########

@app.route("/usuarios", methods=["GET","POST"])
def usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios/usuarios.html', usuarios=usuarios, titulo='Usuarios')

@app.route("/regUsuario", methods=["GET","POST"])
def regUsuario():
    form = RegUsuarioForm()
    if form.validate_on_submit():
        usuario = Usuario(nombre=form.nombre.data, apellido=form.apellido.data,
                        email=form.email.data, nickname=form.nickname.data, password=form.password.data)
        db.session.add(usuario)
        db.session.commit()
        flash(f'El usuario se ha registrado con éxito!!!', 'success')
        return redirect(url_for('usuarios'))
    return render_template('usuarios/regUsuario.html', form=form, titulo='Usuarios')

@app.route("/actUsuario/<int:id>", methods=["GET","POST"])
def actUsuario(id):
    form = RegUsuarioForm()
    usuario = Usuario.query.get(id)
    if form.is_submitted():
        usuario.nombre = form.nombre.data
        usuario.apellido = form.apellido.data
        usuario.email = form.email.data
        usuario.nickname = form.nickname.data
        db.session.commit()
        flash(f'Se ha actualizado un usuario con éxito!!!', 'success')
        return redirect(url_for('usuarios'))
    elif request.method == 'GET':
        form.nombre.data = usuario.nombre
        form.apellido.data = usuario.apellido
        form.email.data = usuario.email
        form.nickname.data = usuario.nickname
        form.password.data = usuario.password
    return render_template("usuarios/regUsuario.html", form=form, titulo='Actualizar Usuario')

@app.route("/elimUsuario/<int:id>", methods=['GET', 'POST'])
def elimUsuario(id):
    usuario = Usuario.query.get(id)
    db.session.delete(usuario)
    db.session.commit()
    flash(f'El usuario se ha eliminado con éxito!!!', 'success')
    return redirect(url_for('usuarios'))

#########----------- CLIENTE -----------#########

@app.route("/clientes", methods=["GET","POST"])
def clientes():
    clientes = Cliente.query.all()
    return render_template('clientes/clientes.html', clientes=clientes, titulo='Clientes')

@app.route("/regCliente", methods=["GET","POST"])
def regCliente():
    form = RegClienteForm()
    if form.validate_on_submit():
        cliente = Cliente(nombre=form.nombre.data, apellido=form.apellido.data,
                        direccion=form.direccion.data, celular=form.celular.data, email=form.email.data)
        db.session.add(cliente)
        db.session.commit()
        flash(f'El cliente se ha registrado con éxito!!!', 'success')
        return redirect(url_for('clientes'))
    return render_template('clientes/regCliente.html', form=form, titulo='Clientes')

@app.route("/elimCliente/<int:id>", methods=['GET', 'POST'])
def elimCliente(id):
    cliente = Cliente.query.get(id)
    db.session.delete(cliente)
    db.session.commit()
    flash(f'El cliente se ha eliminado con éxito!!!', 'success')
    return redirect(url_for('clientes'))

#########----------- PROVEEDOR -----------#########

@app.route("/proveedores", methods=["GET","POST"])
def proveedores():
    proveedores = Proveedor.query.all()
    return render_template('proveedores/proveedores.html', proveedores=proveedores, titulo='Proveedores')

@app.route("/regProveedor", methods=["GET","POST"])
def regProveedor():
    form = RegProveedorForm()
    if form.validate_on_submit():
        proveedor = Proveedor(razon_social=form.razonSocial.data, direccion=form.direccion.data, 
                            celular=form.celular.data, email=form.email.data)
        db.session.add(proveedor)
        db.session.commit()
        flash(f'El proveedor se ha registrado con éxito!!!', 'success')
        return redirect(url_for('proveedores'))
    return render_template('proveedores/regProveedor.html', form=form, titulo='Proveedores')

@app.route("/elimProveedor/<int:id>", methods=['GET', 'POST'])
def elimProveedor(id):
    proveedor = Proveedor.query.get(id)
    db.session.delete(proveedor)
    db.session.commit()
    flash(f'El proveedor se ha eliminado con éxito!!!', 'success')
    return redirect(url_for('proveedores'))

#########----------- PRODUCTOS -----------#########

@app.route("/productos", methods=["GET","POST"])
def productos():
    productos = Producto.query.all()
    return render_template('productos/productos.html', productos=productos, titulo='Productos')

@app.route("/regProducto", methods=["GET","POST"])
def regProducto():
    form = RegProductoForm()
    categorias = Categoria.query.all()
    unidades = Unidad.query.all()
    proveedores = Proveedor.query.all()
    form.categoria.choices = [(c.id,c.nombre) for c in categorias]
    form.unidad.choices = [(u.id,u.nombre) for u in unidades]
    form.proveedor.choices =  [(p.id,p.razon_social) for p in proveedores]
    if form.validate_on_submit():
        producto = Producto(categoria_id=form.categoria.data, unidad_id=form.unidad.data,
                            proveedor_id=form.proveedor.data, nombre=form.nombre.data,
                            precio_compra=form.precioCompra.data, precio_venta=form.precioVenta.data,
                            cantidad=form.cantidad.data)
        db.session.add(producto)
        db.session.commit()
        flash(f'El producto se ha registrado con éxito!!!', 'success')
        return redirect(url_for('productos'))
    return render_template('productos/regProducto.html', form=form, titulo='Productos')

@app.route("/elimProducto/<int:id>", methods=['GET', 'POST'])
def elimProducto(id):
    producto = Producto.query.get(id)
    db.session.delete(producto)
    db.session.commit()
    flash(f'El producto se ha eliminado con éxito!!!', 'success')
    return redirect(url_for('productos'))

@app.route("/ventas",methods = ['GET',"POST"])
def ventas():
    ventas = Venta.query.all()
    return render_template('ventas/ventasList.html',ventas=ventas, titulo='Ventas de Productos')

@app.route("/nueva-venta",methods = ['GET',"POST"])
def NuevaVenta():
    productos = Producto.query.all()
    clientes = Cliente.query.all()
    return render_template('ventas/ventas.html',productos=productos, clientes=clientes, titulo='Venta de Productos')

@app.route("/producto/ajax/<int:id>",methods = ['GET'])
def ajaxProducto(id):
    productoObt = Producto.query.get(id)
    return jsonify(
        id_product = productoObt.id,
        nombre = productoObt.nombre,
        precio_compra = str(productoObt.precio_compra),
        precio_venta = str(productoObt.precio_venta),
        stock = productoObt.cantidad
    )

@app.route("/ventas/cabecera/nueva" , methods = ['POST'])
def ventaNueva():
    content = request.get_json(force = True)
    details = content["productosTabla"]
    NuevaVentaContent = Venta(descuento = content["descuento"] , 
    total = content["total"] , numero_comprobante = content["numero_comprobante"] , cliente_id = content["selectedCliente"])
    db.session.add(NuevaVentaContent)
    db.session.flush()
    db.session.commit()

    for detail in details:
        contentDetail = DetalleVenta(producto_id = detail["id_product"] ,
        cantidad = detail["cantidad"] , compra_id = NuevaVentaContent.id)
        db.session.add(contentDetail)
        db.session.commit()
    
    return jsonify(
        id_venta = "20"
    )