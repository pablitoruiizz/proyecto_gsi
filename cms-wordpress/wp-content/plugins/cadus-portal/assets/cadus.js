/* CADUS Portal: revelado al bajar y paralaje suave del hero. Sin dependencias. */
(function () {
  'use strict';
  var raiz = document.documentElement;
  var movimiento = window.matchMedia('(prefers-reduced-motion: reduce)');
  var puntero = window.matchMedia('(hover: hover) and (pointer: fine)');

  try {
    // 1. Revelado: [data-reveal] solo se oculta (clase cadus-js) cuando este script ya está en marcha; si falla, todo queda visible.
    var items = Array.prototype.slice.call(document.querySelectorAll('[data-reveal]'));
    if (items.length && 'IntersectionObserver' in window && !movimiento.matches) {
      raiz.classList.add('cadus-js');
      var io = new IntersectionObserver(function (entradas) {
        entradas.forEach(function (e) {
          if (e.isIntersecting) {
            e.target.classList.add('is-visible');
            io.unobserve(e.target);
          }
        });
      }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
      items.forEach(function (e) { io.observe(e); });
    }

    // 2. Paralaje del hero: decorativo, solo con puntero fino y sin preferencia de movimiento reducido (se consulta en cada evento).
    var hero = document.querySelector('[data-cadus-hero]');
    if (hero) {
      var formas = Array.prototype.slice.call(hero.querySelectorAll('.cadus-hero__forma'));
      var factor = [18, 30, 46];
      var cola = 0;
      var ult = null;
      var soltar = function () {
        if (cola) { cancelAnimationFrame(cola); cola = 0; }
        ult = null;
        formas.forEach(function (f) { f.style.translate = ''; });
      };
      hero.addEventListener('pointermove', function (ev) {
        if (!puntero.matches || movimiento.matches) { return; }
        ult = { x: ev.clientX, y: ev.clientY };
        if (cola) { return; }
        cola = requestAnimationFrame(function () {
          cola = 0;
          if (!ult) { return; }
          var r = hero.getBoundingClientRect();
          var x = (ult.x - r.left) / r.width - 0.5;
          var y = (ult.y - r.top) / r.height - 0.5;
          formas.forEach(function (f, i) {
            f.style.translate = (-x * factor[i]).toFixed(1) + 'px ' + (-y * factor[i]).toFixed(1) + 'px';
          });
        });
      });
      hero.addEventListener('pointerleave', soltar);
    }
  } catch (e) {
    raiz.classList.remove('cadus-js'); // ante cualquier error, el contenido se muestra sin animación
  }
})();
