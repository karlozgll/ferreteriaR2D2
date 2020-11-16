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
            <th scope="row">${element.id_product}</th>
            <td>${element.nombre}</td>
            <td>${element.cantidad}</td>
        </tr>`;
  });
  datatable.innerHTML = inner;
};

const cargarData = () => {
  const selectedProducto = document.getElementById("selectedProducto");
  const cantidad = document.getElementById("cantidad");
  
  fetch('http://localhost/producto/ajax/2')
  .then(response => response.json())
  .then(data => {agregarProducto({...data, cantidad : cantidad.value}) ; calcularTotal()});
  
};

const calcularTotal = () => {
  const total = productosTabla.reduce((acc , producto) => acc + producto , 0)
  document.getElementById('total').value = total
}
// llenarOptionProducts();
