(function () {
  var header = document.getElementById('top');
  window.addEventListener('scroll', function () {
    header.classList.toggle('scrolled', window.scrollY > 8);
  });

  var burger = document.getElementById('burger');
  var menu = document.getElementById('menu');
  if (burger && menu) {
    burger.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { menu.classList.remove('open'); });
    });
  }

  var WA = document.body.getAttribute('data-wa');
  var form = document.getElementById('diag-form');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var f = new FormData(form);
      var v = function (k) { return (f.get(k) || '').toString().trim(); };
      var texto = 'Olá! Quero o diagnóstico gratuito da KAIRON.\n\n' +
        'Nome: ' + v('nome') + '\n' +
        'Empresa: ' + v('empresa') + '\n' +
        'Desafio: ' + v('desafio') + '\n' +
        (v('msg') ? '\n' + v('msg') : '');
      var canal = e.submitter && e.submitter.value === 'email' ? 'email' : 'wa';
      if (canal === 'email') {
        window.location.href = 'mailto:contato@kaironbr.com?subject=' +
          encodeURIComponent('Diagnóstico gratuito | ' + v('empresa')) +
          '&body=' + encodeURIComponent(texto + '\nWhatsApp: ' + v('whatsapp'));
      } else {
        window.open('https://wa.me/' + WA + '?text=' + encodeURIComponent(texto), '_blank', 'noopener');
      }
    });
  }
})();
