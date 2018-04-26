
$('#myModal').on('shown.bs.modal', function() {
  var nomeUsuario = $("#myInput").val();
  $('#nomeModal').text(nomeUsuario);
});

