 //$("input[submit]") asi puedo selecionar todos los campos imput que tengan un atributo submit
 $(document).ready(function(){     // cuando el documento este cargado va  a ejecutar las funciones que esten dentro
   
  $("button.toggle-mostrar-verbo").click(function () {
      $("span.ocultar-verbo").toggle();
      $("span.mostrar-verbo").toggle();
      $("#toggle-mostrar-verbo").slideToggle(200);
});
  
  $("button.toggle-mostrar-sustantivo").click(function () {
      $("span.ocultar-sustantivo").toggle();
      $("span.mostrar-sustantivo").toggle();
      $("#toggle-mostrar-sustantivo").slideToggle(200);
});
  
 $("a.img").click(function () {
      $("#imagen-sustantivo").slideToggle(100);
      $(".ocultar-tip").toggle();
      $(".mostrar-tip").toggle();
});
 
$("a.img2").click(function () {
      $(".conjugacion").slideToggle(100);
      $("#ocultar-tip2").toggle();
      $("#mostrar-tip2").toggle();
});
  
$('.tip').tooltip('hide');

$('#buscar_ejemplos').modal('toggle');

$("button.toggle-mostrar-actualizar").click(function () {
      $("span.ocultar-actualizar").toggle();
      $("span.mostrar-actualizar").toggle();
      $("#mostrar-admin").slideToggle(200);
});

$("button.toggle-mostrar-ejemplo").click(function () {
      $("span.ocultar-ejemplo").toggle();
      $("span.mostrar-ejemplo").toggle();
      $("#mostrar-ejemplo").slideToggle(200);
});
	
$(".glosa").click(function () {
      $(".glosarios").slideToggle(100);
      $("#ocultar-glosario").toggle();
      $("#mostrar-glosario").toggle();
});

$("a.img3").click(function () {
      $(".conjugacion").slideToggle(100);
      $("#ocultar-tip3").toggle();
      $("#mostrar-tip3").toggle();
});

$("#mostrar-gramatica").click(function () {
      $("#container-fluid-negro").slideToggle(300);
     // $("#ocultar-tip3").toggle();
    //  $("#mostrar-tip3").toggle();
});

jQuery('.oculto').hide();
        jQuery('#palabras_sustantivo').change(function(){
             if(jQuery('#palabras_sustantivo').attr('checked'))
                 jQuery('.oculto').show();
             else jQuery('.oculto').hide();
          });
	
jQuery('.oculto3').hide();
        jQuery('#palabras_anadir_glosario').change(function(){
             if(jQuery('#palabras_anadir_glosario').attr('checked'))
                 jQuery('.oculto3').show();
             else jQuery('.oculto3').hide();
          });
	
jQuery('.oculto2').hide();
        jQuery('#palabras_verbo').change(function(){
             if(jQuery('#palabras_verbo').attr('checked'))
                 jQuery('.oculto2').show();
             else jQuery('.oculto2').hide();
          });

 }); // final de la carga del documento
 
 
  

 