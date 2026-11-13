/* CADUS Portal: accesibilidad del teclado (HU-15a). Sin dependencias. */
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
