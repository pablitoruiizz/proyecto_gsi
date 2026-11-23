/* CADUS Portal: accesibilidad del teclado (HU-15a) y errores de los formularios (HU-15, H15-3). Sin dependencias. */
(function () {
  'use strict';
  try {
    // «Saltar al contenido»: además de desplazar la página, mueve el foco al <main>. Sin esto, algunos navegadores dejan el
    // foco en el enlace y la siguiente pulsación del tabulador vuelve a recorrer la cabecera.
    var enlace = document.querySelector('.skip-link');
    if (!enlace) { return; }
    enlace.addEventListener('click', function () {
      var id = (enlace.getAttribute('href') || '').replace('#', '');
      var destino = id ? document.getElementById(id) : null;
      if (!destino) { return; }
      if (!destino.hasAttribute('tabindex')) {
        destino.setAttribute('tabindex', '-1');
        destino.addEventListener('blur', function () { destino.removeAttribute('tabindex'); }, { once: true });
      }
      destino.focus();
    });
  } catch (e) { /* el enlace sigue funcionando como ancla normal */ }
})();

/* CADUS Portal: errores accesibles en los formularios de Fluent Forms (buzón y mediación) (HU-15, H15-3).
   Fluent Forms pinta cada error como <div class="error" role="alert"> junto al campo y marca el campo con aria-invalid,
   pero no los enlaza ni mueve el foco. Aquí: cada error se enlaza a su campo con aria-describedby (el lector lo lee al
   llegar al campo) y, tras un intento de envío, el foco va al primer campo con error. */
(function () {
  'use strict';
  try {
    var formularios = document.querySelectorAll('form.frm-fluent-form');
    if (!formularios.length || !window.MutationObserver) { return; }
    var contador = 0;

    function campoDe(error) {
      var grupo = error.closest('.ff-el-group');
      return grupo ? grupo.querySelector('input:not([type=hidden]), select, textarea') : null;
    }

    function quitarId(campo, id) {
      var ids = (campo.getAttribute('aria-describedby') || '').split(/\s+/).filter(function (x) { return x && x !== id; });
      if (ids.length) { campo.setAttribute('aria-describedby', ids.join(' ')); } else { campo.removeAttribute('aria-describedby'); }
    }

    function enlazar(form) {
      form.querySelectorAll('.ff-el-group .error').forEach(function (error) {
        var campo = campoDe(error);
        if (!campo) { return; }
        if (!error.id) { error.id = 'cadus-error-' + (++contador); }
        var ids = (campo.getAttribute('aria-describedby') || '').split(/\s+/).filter(Boolean);
        if (ids.indexOf(error.id) === -1) { ids.push(error.id); campo.setAttribute('aria-describedby', ids.join(' ')); }
      });
      // Errores que ya no están: se quita su id del campo para que el lector no anuncie un mensaje inexistente.
      form.querySelectorAll('[aria-describedby*="cadus-error-"]').forEach(function (campo) {
        (campo.getAttribute('aria-describedby') || '').split(/\s+/).forEach(function (id) {
          if (id.indexOf('cadus-error-') === 0 && !document.getElementById(id)) { quitarId(campo, id); }
        });
      });
    }

    formularios.forEach(function (form) {
      var intento = 0;
      var pendiente = null;
      // Fase de captura: se registra antes de que Fluent Forms valide y pinte los errores.
      form.addEventListener('submit', function () { intento = Date.now(); }, true);
      new MutationObserver(function () {
        clearTimeout(pendiente);
        pendiente = setTimeout(function () {
          enlazar(form);
          if (intento && Date.now() - intento < 5000) {
            var primero = form.querySelector('[aria-invalid="true"]');
            if (primero) { intento = 0; primero.focus(); }
          }
        }, 60);
      }).observe(form, { childList: true, subtree: true });
    });
  } catch (e) { /* sin esto los errores siguen visibles y con role=alert */ }
})();
