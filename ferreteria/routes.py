from flask import render_template, flash, url_for, redirect, request, abort, make_response, jsonify
from ferreteria import app, db
from ferreteria.forms import RegUsuarioForm, RegProveedorForm, RegClienteForm, LoginForm, RegProductoForm
from ferreteria.models import Cliente, Usuario, Proveedor, Producto, Unidad, Categoria, Compra, DetalleCompra, Venta, DetalleVenta
from flask import send_from_directory
from datetime import datetime
from sqlalchemy import or_, and_
from fpdf import FPDF
import ferreteria.clases.pdf as pdf
import os
import json

@app.route("/home", methods=["GET"])
def home():
    return render_template("home.html")


@app.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(nickname=form.nickname.data).first()
        if usuario:
            if usuario.password == form.password.data:
                flash(
                    f'Bienvenido {usuario.nickname}!, has iniciado sesión con éxito', 'success')
                return redirect(url_for('home'))
            else:
                flash(
                    f'Contraseña incorrecta para {usuario.nickname}', 'danger')
        else:
            flash(f'No existe este usuario', 'danger')
    return render_template("login.html", form=form)

#########-----------USUARIO -----------#########


@app.route("/usuarios", methods=["GET", "POST"])
def usuarios():
    usuarios = Usuario.query.all()
    return render_template('usuarios/usuarios.html', usuarios=usuarios, titulo='Usuarios')


@app.route("/regUsuario", methods=["GET", "POST"])
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


@app.route("/actUsuario/<int:id>", methods=["GET", "POST"])
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


@app.route("/clientes", methods=["GET", "POST"])
def clientes():
    clientes = Cliente.query.all()
    return render_template('clientes/clientes.html', clientes=clientes, titulo='Clientes')


@app.route("/regCliente", methods=["GET", "POST"])
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

@app.route("/actCliente/<int:id>", methods=["GET", "POST"])
def actCliente(id):
    form = RegClienteForm()
    cliente = Cliente.query.get(id)
    if form.is_submitted():
        cliente.nombre = form.nombre.data
        cliente.apellido = form.apellido.data
        cliente.direccion = form.direccion.data
        cliente.celular = form.celular.data
        cliente.email = form.email.data
        db.session.commit()
        flash(f'Se ha actualizado un cliente con éxito!!!', 'success')
        return redirect(url_for('clientes'))
    elif request.method == 'GET':
        form.nombre.data = cliente.nombre
        form.apellido.data = cliente.apellido
        form.email.data = cliente.email
        form.direccion.data = cliente.direccion
        form.celular.data = cliente.celular
    return render_template("clientes/regCliente.html", form=form, titulo='Actualizar Cliente')

#########----------- PROVEEDOR -----------#########


@app.route("/proveedores", methods=["GET", "POST"])
def proveedores():
    proveedores = Proveedor.query.all()
    return render_template('proveedores/proveedores.html', proveedores=proveedores, titulo='Proveedores')


@app.route("/regProveedor", methods=["GET", "POST"])
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

@app.route("/actProveedor/<int:id>", methods=["GET", "POST"])
def actProveedor(id):
    form = RegProveedorForm()
    proveedor = Proveedor.query.get(id)
    if form.is_submitted():
        proveedor.razon_social = form.razonSocial.data
        proveedor.direccion = form.direccion.data
        proveedor.celular = form.celular.data
        proveedor.email = form.email.data
        db.session.commit()
        flash(f'Se ha actualizado un proveedor con éxito!!!', 'success')
        return redirect(url_for('proveedores'))
    elif request.method == 'GET':
        form.razonSocial.data = proveedor.razon_social
        form.email.data = proveedor.email
        form.direccion.data = proveedor.direccion
        form.celular.data = proveedor.celular
    return render_template("proveedores/regProveedor.html", form=form, titulo='Actualizar Proveedor')

#########----------- PRODUCTOS -----------#########


@app.route("/productos", methods=["GET", "POST"])
def productos():
    productos = Producto.query.all()
    return render_template('productos/productos.html', productos=productos, titulo='Productos')


@app.route("/regProducto", methods=["GET", "POST"])
def regProducto():
    form = RegProductoForm()
    categorias = Categoria.query.all()
    unidades = Unidad.query.all()
    proveedores = Proveedor.query.all()
    form.categoria.choices = [(c.id, c.nombre) for c in categorias]
    form.unidad.choices = [(u.id, u.nombre) for u in unidades]
    form.proveedor.choices = [(p.id, p.razon_social) for p in proveedores]
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

@app.route("/actProducto/<int:id>", methods=["GET", "POST"])
def actProducto(id):
    form = RegProductoForm()
    producto = Producto.query.get(id)
    categorias = Categoria.query.all()
    unidades = Unidad.query.all()
    proveedores = Proveedor.query.all()
    
    if form.is_submitted():
        producto.categoria_id = form.categoria.data
        producto.unidad_id = form.unidad.data
        producto.proveedor_id = form.proveedor.data
        producto.nombre = form.nombre.data
        producto.precio_compra = form.precioCompra.data
        producto.precio_venta = form.precioVenta.data
        producto.cantidad = form.cantidad.data
        db.session.commit()
        flash(f'Se ha actualizado un producto con éxito!!!', 'success')
        return redirect(url_for('productos'))
    elif request.method == 'GET':
        form.categoria.choices = [(c.id, c.nombre) for c in categorias]
        form.unidad.choices = [(u.id, u.nombre) for u in unidades]
        form.proveedor.choices = [(p.id, p.razon_social) for p in proveedores]
        form.nombre.data = producto.nombre
        form.precioCompra.data = producto.precio_compra
        form.precioVenta.data = producto.precio_venta
        form.cantidad.data = producto.cantidad
    return render_template("productos/regProducto.html", form=form, titulo='Actualizar Producto')

@app.route("/producto/ajax/<int:id>", methods=['GET'])
def ajaxProducto(id):
    productoObt = Producto.query.get(id)
    return jsonify(
        id_product=productoObt.id,
        nombre=productoObt.nombre,
        precio_compra=str(productoObt.precio_compra),
        precio_venta=str(productoObt.precio_venta),
        stock=productoObt.cantidad
    )


@app.route("/ventas", methods=['GET', "POST"])
def ventas():
    ventas = Venta.query.all()
    return render_template('ventas/ventasList.html', ventas=ventas, titulo='Ventas de Productos')

@app.route("/ventas/detalle/<int:id>", methods=['GET', "POST"])
def DetalleVentas(id):
    detalleVenta1 = DetalleVenta.query.filter(DetalleVenta.venta_id == id)
    return render_template('ventas/detallesVenta.html', detalles=detalleVenta1, titulo='Detalles de la venta ')

@app.route("/nueva-venta", methods=['GET', "POST"])
def NuevaVenta():
    productos = Producto.query.all()
    clientes = Cliente.query.all()
    return render_template('ventas/ventas.html', productos=productos, clientes=clientes, titulo='Venta de Productos')


@app.route("/ventas/cabecera/nueva", methods=['POST'])
def ventaNueva():
    try:
        content = request.get_json(force=True)
        details = content["productosTabla"]
        NuevaVentaContent = Venta(descuento=content["descuento"],
                                  total=content["total"], numero_comprobante=content["numero_comprobante"], cliente_id=content["selectedCliente"])
        db.session.add(NuevaVentaContent)
        db.session.flush()
        db.session.commit()

        for detail in details:
            contentDetail = DetalleVenta(producto_id=detail["id_product"], cantidad=detail["cantidad"], 
                                        precio_unitario = detail["precio_venta"],venta_id = NuevaVentaContent.id)
            db.session.add(contentDetail)
            db.session.commit()
            productMod = Producto.query.get(detail["id_product"])
            productMod.cantidad = int(productMod.cantidad) - int(detail["cantidad"])
            db.session.commit()
        flash(f'La venta se ha guardado con éxito!!!', 'success')
        return False
    except:
        flash(f'No se pudo guardar la venta', 'error')
        return False

@app.route("/compras", methods=['GET', "POST"])
def compras():
    compras = Compra.query.all()
    return render_template('compras/comprasList.html', compras=compras, titulo='Compras de Productos')

@app.route("/compras/detalle/<int:id>", methods=['GET', "POST"])
def DetalleCompras(id):
    detalleCompra = DetalleCompra.query.filter(DetalleCompra.compra_id == id)
    return render_template('compras/detallesCompra.html', detalles=detalleCompra, titulo='Detalles de la compra ')
    
@app.route("/nueva-compra", methods=['GET', "POST"])
def NuevaCompra():
    productos = Producto.query.all()
    proveedorList = Proveedor.query.all()
    return render_template('compras/compras.html', productos=productos, proveedores=proveedorList, titulo='Compra de Productos')


@app.route("/compras/cabecera/nueva", methods=['POST'])
def compraNueva():
    try:
        content = request.get_json(force=True)
        details = content["productosTabla"]
        NuevaCompraContent = Compra(total=content["total"], numero_comprobante=content["numero_comprobante"],
                                    proveedor_id=content["selectedProveedor"])
        db.session.add(NuevaCompraContent)
        db.session.flush()
        db.session.commit()
        for detail in details:
            contentDetail = DetalleCompra(producto_id=detail["id_product"],precio_unitario = detail["precio_compra"],
                                          cantidad=detail["cantidad"], compra_id=NuevaCompraContent.id)
            db.session.add(contentDetail)
            db.session.commit()
            productMod = Producto.query.get(detail["id_product"])
            productMod.cantidad = int(productMod.cantidad) + int(detail["cantidad"])
            db.session.commit()
        return False
    except:
        flash(f'No se pudo guardar la compra', 'error')
        return False

@app.route('/reportarVentas', methods=['GET', 'POST'])
def reportarVentas():
    ventas = db.session.query(Venta).all()
    respuesta = pdf.pdfVentas(ventas)
    return respuesta

@app.route('/reportarCompras', methods=['GET', 'POST'])
def reportarCompras():
    compras = db.session.query(Compra).all()
    respuesta = pdf.pdfCompras(compras)
    return respuesta