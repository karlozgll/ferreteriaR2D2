const productosTabla = [];
const agregarProducto = (producto) => {
  const find = productosTabla.filter((el) => el.nombre === producto.nombre);
  if (find.length > 0) {
    console.log("este elemento ya existe en la tabla");
  } else {
    productosTabla.push(producto);
    llenarTabla();
  }
};

const llenarTabla = () => {
  const datatable = document.getElementById("datatable");
  datatable.innerHTML = "";
  let inner = "";
  productosTabla.forEach((element, idx) => {
    inner += `<tr>
            <th scope="row">${idx + 1}</th>
            <td>${element.nombre}</td>
            <td>${element.precio_venta}</td>
            <td>${element.cantidad}</td>
            <td>${element.subTotal}</td>
        </tr>`;
  });
  datatable.innerHTML = inner;
};

const cargarData = () => {
  const selectedProducto = document.getElementById("selectedProducto");
  const cantidad = document.getElementById("cantidad");
  fetch(`http://localhost/producto/ajax/${selectedProducto.value}`)
    .then((response) => response.json())
    .then((data) => {
      if (data.stock > cantidad.value && cantidad.value > 0) {
        console.log(data)
        agregarProducto({
          ...data,
          cantidad: cantidad.value,
          subTotal: data.precio_venta * cantidad.value,
        });
      } else {
        alert("No se puede añadir por falta de stock");
      }
    })
    .then((data) => calcularTotal());
};

const calcularTotal = () => {
  const total = productosTabla.reduce(
    (acc, producto) => acc + producto.subTotal,
    0
  );
  document.getElementById("total").value = total;
  aplicarDescuento(total);
};

const aplicarDescuento = (total) => {
  const descuento = document.getElementById("descuento");
  if (descuento.value < total && descuento.value > 0) {
    const totalValue = document.getElementById("total");
    totalValue.value = total - descuento.value;
  } else {
    descuento.value = 0;
    alert("No se puede aplicar el descuento");
  }
};

const guardarVenta = () => {
  const selectedCliente = document.getElementById("selectedCliente").value;
  const numero_comprobante = document.getElementById("numero_comprobante")
    .value;
  const descuento = document.getElementById("descuento").value;
  const total = document.getElementById("total").value;
  if (
    numero_comprobante &&
    numero_comprobante !== "" &&
    numero_comprobante > 0
  ) {
    fetch(`http://localhost/ventas/cabecera/nueva`, {
      method: "POST",
      mode: "no-cors",
      cache: "no-cache",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
      },
      redirect: "follow",
      referrerPolicy: "no-referrer",
      body: JSON.stringify({
        selectedCliente,
        numero_comprobante,
        descuento,
        total,
        productosTabla,
      }),
    }).then(() => (window.location.href = "http://localhost/ventas"));
  } else {
    alert("Por favor ingrese el numero de comprobante");
  }
};
