$(document).ready(function() {
    $(".alert").fadeTo(2000, 500).slideUp(500, function(){
        $(".alert").slideUp(500);
    });

});

function confirmar(e){
    const confirmacion = confirm('¿Estás seguro que deseas eliminar?')
    if (!confirmacion) {
        e.preventDefault()
    }
}
