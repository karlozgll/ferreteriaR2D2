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
            <td>${element.precio_compra}</td>
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
  .then(data => {agregarProducto({...data, cantidad : cantidad.value , subTotal : data.precio_compra * cantidad.value}) })
  .then(data => calcularTotal())
};

const calcularTotal = () => {
  const total = productosTabla.reduce((acc , producto) => acc + producto.subTotal , 0)
  document.getElementById('total').value = total
}


const guardarCompra = () => {
  const selectedProveedor = document.getElementById("selectedProveedor").value
  const numero_comprobante = document.getElementById("numero_comprobante").value
  const total = document.getElementById("total").value
  fetch(`http://localhost/compras/cabecera/nueva`,{ 
    method : 'POST',
    mode: 'cors',
    cache: 'no-cache',
    credentials: 'same-origin',
    headers: {
      'Content-Type': 'application/json'
    },
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
    body : JSON.stringify({ selectedProveedor , numero_comprobante , total , productosTabla })
  })
}
