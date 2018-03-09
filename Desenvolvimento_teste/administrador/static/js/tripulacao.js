$(function() {
        var scntDiv = $('#p_scents');
        var i = $('#p_scents p').size() + 1;
        
        $('#addScnt').live('click', function() {
                $('<div class="col-md-3" ><label>Cargo:</label>' +
				  		'<div class="form-group label-floating" >' +
		                		'<select class="form-control" name="tipo" id="p_scnt">' +
									'<option value="Escolha"> Escolha </option>' +
		                        	'<option value="Comandante"> Comandante </option>' +
		                        	'<option value="1º Imediato"> 1º Imediato </option>' +
		                        	'<option value="2º Imediato"> 2º Imediato </option>' +
		                        	'<option value="Encarregado"> Encarregado </option>' +                              
		                    	'</select>' +
		                	'</div>' +
				  '</div>' +							
				  '<div class="col-md-7"><label>Nome:</label>' +
				  	'<div class="form-group">' +
		                  '<input type="text" class="form-control" name="nome" placeholder="nome">' +
		            '</div>' +
				  '</div>' +
				  '<div class="col-md-2"><label>Sexo:</label>' +
				  	'<div class="form-group">' +
		                  '<input type="text" class="form-control" name="sexo" placeholder="sexo">' +
		            '</div>' +
				  '</div>' +
				  '<div class="col-md-4"><label>Data de nascimento:</label>' +
				  	'<input type="date" class="form-control" name="data" placeholder="data de nascimento:">' +
				  '</div>' +
				  '<div class="col-md-4"><label>Salario:</label>' +
				  	'<input type="number" class="form-control" name="data" placeholder="salario:">' +
				  '</div>' +						  
				'</div>'+
				'<br>').appendTo(scntDiv);
                i++;
                return false;
        });
        
        $('#remScnt').live('click', function() { 
                if( i > 2 ) {
                        $(this).parents('p').remove();
                        i--;
                }
                return false;
        });
});