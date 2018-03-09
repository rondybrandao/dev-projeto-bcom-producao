$(function() {
        var scntDiv = $('#p_scents');
        var i = $('#p_scents p').size() + 1;
        
        $('#addScnt').live('click', function() {
                $('<div class="col-md-4"><label>Tipo:</label>' +			  	
				  		' <div class="form-group label-floating" id="p_scents">' +
                        		'<select class="form-control" name="tipo" id="p_scnt">' +
									'<option value="Escolha"> Escolha </option>' +
                                	'<option value="Pintura"> Pintura </option>' +
                                	'<option value="Oleo"> Oleo </option>' +
                                	'<option value="Principal"> Maquina Principal </option>'+
                                	'<option value="Bomba"> Bomba Dagua </option>'+
                                	'<option value="Casco"> Casco </option>'+
                                	'<option value="Eletrico"> Eletrico </option>'+
                                	'<option value="Eletronico"> Eletronico </option>'+
                                	'<option value="Estrutural"> Estrutural </option>'+                          
                            	'</select>'+
                        	'</div>'+
				  '</div>'+			
				  '<div class="col-md-4"><label>Descricao:</label>'+				  	
				  	'<div class="form-group">'+
                          '<textarea class="form-control" name="descricao" placeholder="descricao" rows="6"></textarea>'+
                    '</div>'+
				  '</div>'+
				  '<div class="col-md-4"><label>valor:</label>'+
				  	'<input type="number" class="form-control" name="valor" id="valor" placeholder="R$:" value="">'+
				  '</div>'+ 
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