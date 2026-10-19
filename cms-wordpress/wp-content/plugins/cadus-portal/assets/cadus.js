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

    // 3. Noticias: filtro por categoría y botones del carrusel. Sin JS la lista sigue siendo un scroll horizontal con todo visible.
    var caja = document.querySelector('[data-cadus-carrusel]');
    if (caja) {
      var pista = caja.querySelector('.cadus-carrusel__pista');
      var mandos = caja.querySelector('[data-cadus-mandos]');
      var filtros = document.querySelector('[data-cadus-filtros]');
      var tarjetas = Array.prototype.slice.call(caja.querySelectorAll('.cadus-noticia'));
      var ant = caja.querySelector('.cadus-carrusel__ant');
      var sig = caja.querySelector('.cadus-carrusel__sig');
      var suave = function () { return movimiento.matches ? 'auto' : 'smooth'; };
      var estadoMandos = function () {
        if (!ant || !sig) { return; }
        var max = pista.scrollWidth - pista.clientWidth - 2;
        var sinAnt = pista.scrollLeft <= 2;
        var sinSig = pista.scrollLeft >= max;
        var teniaFoco = document.activeElement;
        ant.disabled = sinAnt;
        sig.disabled = sinSig;
        // si el botón que tenía el foco se acaba de deshabilitar, el foco pasa al otro para no perderlo
        if (teniaFoco === ant && sinAnt && !sinSig) { sig.focus(); }
        if (teniaFoco === sig && sinSig && !sinAnt) { ant.focus(); }
        if (mandos) { mandos.hidden = max <= 0; }
      };
      if (mandos) { mandos.hidden = false; }
      if (ant && sig) {
        ant.addEventListener('click', function () { pista.scrollBy({ left: -pista.clientWidth * 0.9, behavior: suave() }); });
        sig.addEventListener('click', function () { pista.scrollBy({ left: pista.clientWidth * 0.9, behavior: suave() }); });
        pista.addEventListener('scroll', function () { window.requestAnimationFrame(estadoMandos); }, { passive: true });
        window.addEventListener('resize', estadoMandos);
        estadoMandos();
      }
      if (filtros) {
        filtros.hidden = false;
        // región viva: anuncia cuántas noticias quedan al filtrar (los chips no cambian el foco)
        var aviso = document.createElement('p');
        aviso.className = 'screen-reader-text';
        aviso.setAttribute('role', 'status');
        filtros.insertAdjacentElement('afterend', aviso);
        var botones = Array.prototype.slice.call(filtros.querySelectorAll('[data-cadus-filtro]'));
        botones.forEach(function (b) {
          b.addEventListener('click', function () {
            var cat = b.getAttribute('data-cadus-filtro');
            botones.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
            tarjetas.forEach(function (t) {
              var cats = (t.getAttribute('data-cadus-categorias') || '').split(/\s+/);
              var ver = cat === 'todo' || cats.indexOf(cat) !== -1;
              t.hidden = !ver;
              if (ver) { t.classList.add('is-visible'); }
            });
            var visibles = tarjetas.filter(function (t) { return !t.hidden; }).length;
            aviso.textContent = visibles + (visibles === 1 ? ' noticia' : ' noticias') + (cat === 'todo' ? '' : ' en ' + b.textContent.trim());
            pista.scrollTo({ left: 0, behavior: 'auto' });
            estadoMandos();
          });
        });
      }
    }
  } catch (e) {
    raiz.classList.remove('cadus-js'); // ante cualquier error, el contenido se muestra sin animación
  }
})();
