const productosTabla = [];
const agregarProducto = (producto) => {
  productosTabla.push(producto);
  llenarTabla();
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
  .then(response => response.json())
  .then(data => {agregarProducto({...data, cantidad : cantidad.value , subTotal : data.precio_venta * cantidad.value}) })
  .then(data => calcularTotal())
};

const calcularTotal = () => {
  const total = productosTabla.reduce((acc , producto) => acc + producto.subTotal , 0)
  document.getElementById('total').value = total
  aplicarDescuento(total)
}

const aplicarDescuento = (total) => {
  const descuento = document.getElementById("descuento") 
  const totalValue = document.getElementById('total')
  totalValue.value = total - descuento.value
}

const guardarVenta = () => {
  const selectedCliente = document.getElementById("selectedCliente").value
  const numero_comprobante = document.getElementById("numero_comprobante").value
  const descuento = document.getElementById("descuento").value
  const total = document.getElementById("total").value
  fetch(`http://localhost/ventas/cabecera/nueva`,{ 
    method : 'POST',
    mode: 'cors',
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json'
    },
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
    body : JSON.stringify({ selectedCliente , numero_comprobante , descuento , total , productosTabla })
  })
  .then(response => response.json())
  .then(data => console.log(data))
}