(() => {
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const buzz = (ms = 8) => { try { if (navigator.vibrate && (!navigator.userActivation || navigator.userActivation.hasBeenActive)) navigator.vibrate(ms); } catch (e) {} };

  /* ---------- Hero room switcher ---------- */
  const hero = $('.hero'), word = $('#heroWord'), cap = $('#heroCap');
  const caps = { kitchen: 'Recent kitchen + open plan · Nov 2025', bath: 'Recent primary bath · Aug 2026', home: 'Recent whole-home remodel · Feb 2026' };
  const roomBtns = $$('.rooms [role=radio]');
  let roomTouched = false;
  function setRoom(btn) {
    const room = btn.dataset.room;
    roomBtns.forEach((b) => b.setAttribute('aria-checked', b === btn));
    $$('.hero__pic').forEach((p) => p.classList.toggle('is-on', p.dataset.for === room));
    hero.dataset.room = room;
    word.classList.add('is-swap');
    setTimeout(() => { word.textContent = btn.dataset.word; word.classList.remove('is-swap'); }, reduce ? 0 : 220);
    cap.textContent = caps[room];
  }
  roomBtns.forEach((b, i) => {
    b.addEventListener('click', () => { roomTouched = true; buzz(); setRoom(b); });
    b.addEventListener('keydown', (e) => {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      const j = (i + (e.key === 'ArrowRight' ? 1 : -1) + roomBtns.length) % roomBtns.length;
      roomTouched = true; setRoom(roomBtns[j]); roomBtns[j].focus();
    });
  });
  // gently cycle rooms until the visitor picks one
  if (!reduce) {
    let k = 0;
    const cyc = setInterval(() => {
      if (roomTouched || scrollY > innerHeight) { if (roomTouched) clearInterval(cyc); return; }
      k = (k + 1) % roomBtns.length; setRoom(roomBtns[k]);
    }, 5200);
  }

  /* ---------- Count-up (final value is already in the markup) ---------- */
  function countUp(el) {
    if (reduce) return;
    const end = parseFloat(el.dataset.count), dec = +(el.dataset.dec || 0);
    if (end < 2) return;
    const t0 = performance.now(), dur = 1200;
    const step = (t) => {
      const k = Math.max(0, Math.min(1, (t - t0) / dur)), e = 1 - Math.pow(1 - k, 3);
      el.textContent = (end * e).toFixed(dec);
      if (k < 1) requestAnimationFrame(step); else el.textContent = end.toFixed(dec);
    };
    requestAnimationFrame(step);
  }

  /* ---------- Reveal on scroll ---------- */
  const io = new IntersectionObserver((entries) => {
    entries.forEach((en) => {
      if (!en.isIntersecting) return;
      en.target.classList.add('in');
      $$('[data-count]', en.target).forEach(countUp);
      if (en.target.matches('[data-count]')) countUp(en.target);
      io.unobserve(en.target);
    });
  }, { threshold: 0.18, rootMargin: '0px 0px -6% 0px' });
  $$('[data-reveal], .steps li').forEach((el) => io.observe(el));
  // phone chat plays when it is well in view
  const phone = $('.phone');
  new IntersectionObserver((en, o) => { if (en[0].isIntersecting) { phone.classList.add('in'); o.disconnect(); } }, { threshold: 0.45 }).observe(phone);

  /* ---------- Services tiles pre-fill the quiz ---------- */
  $$('[data-pick]').forEach((t) => t.addEventListener('click', () => {
    const r = $(`#quiz [name=project][value="${t.dataset.pick}"]`);
    if (r) { r.checked = true; setTimeout(() => stepN === 1 && go(2), 500); }
  }));

  /* ---------- Reveal studio (before/after + roof scrub) ---------- */
  const ba = $('#ba'), baR = $('#baRange'), baB = $('#baBefore'), baA = $('#baAfter'), note = $('#baNote');
  const scrub = $('#scrub'), scR = $('#scrubRange'), scImgs = $$('img', scrub), scLis = $$('.scrub__stages li', scrub);
  const sets = {
    kitchen: { b: 'images/ba26-kitchen-before.jpg', a: 'images/ba26-kitchen-after.jpg', bAlt: 'Before: the same galley kitchen with white cabinets and tile floor', aAlt: 'After: galley kitchen with navy and light-blue shaker cabinets', comp: false,
      note: 'White laminate and tile floors out; navy and soft-blue shaker cabinets, a farmhouse sink, brass hardware and new plank flooring in.' },
    bath: { b: 'images/ba26-bath-before.jpg', a: 'images/ba26-bath-after.jpg', bAlt: 'Before: primary bath with a tiled tub deck and yellow walls', aAlt: 'After: freestanding tub, floating wood vanity with lit mirrors', comp: false,
      note: 'The built-in tub deck and brass-framed shower came out; a freestanding tub, floating wood vanity with backlit mirrors and a fluted walk-in shower went in.' },
    gut: { b: 'images/ba26-gut-before.jpg', a: 'images/ba26-gut-after.jpg', bAlt: 'Before: the house gutted down to bare studs and subfloor', aAlt: 'After: finished open kitchen with a large island', comp: false,
      note: 'Taken down to the studs, then rebuilt: framing, plumbing, electric, drywall, cabinetry and a big island, all managed by one team.' },
    roof: { note: 'A full tear-off on a waterfront home in Oceanport, shot by drone: the old roof, stripped to the deck, and finished.' }
  };
  const setP = (v) => ba.style.setProperty('--p', v + '%');
  baR.addEventListener('input', () => setP(baR.value));
  function setScrub(v) {
    const s = v / 100; // 0..2
    scrub.style.setProperty('--s', s);
    scImgs[1].style.opacity = Math.min(1, Math.max(0, s));
    scImgs[2].style.opacity = Math.min(1, Math.max(0, s - 1));
    const st = Math.round(s);
    scLis.forEach((l, i) => l.classList.toggle('on', i === st));
  }
  scR.addEventListener('input', () => setScrub(+scR.value));
  setScrub(0);

  let swept = false;
  function sweep(fromV, toV, set, dur = 1400) {
    if (reduce) { set(toV); return; }
    const t0 = performance.now(), id = {};
    sweep.cur = id; // a newer sweep cancels this one
    const f = (t) => {
      if (sweep.cur !== id) return;
      const k = Math.max(0, Math.min(1, (t - t0) / dur)), e = k < .5 ? 2 * k * k : 1 - Math.pow(-2 * k + 2, 2) / 2;
      set(fromV + (toV - fromV) * e);
      if (k < 1) requestAnimationFrame(f);
    };
    requestAnimationFrame(f);
    // if frames never run (background tab), still land on the final state
    setTimeout(() => { if (sweep.cur === id) set(toV); }, dur + 120);
  }
  const ptabs = $$('.ptabs [role=tab]');
  function pick(i) {
    ptabs.forEach((b, j) => { b.setAttribute('aria-selected', i === j); b.tabIndex = i === j ? 0 : -1; });
    const key = ptabs[i].dataset.ba, s = sets[key];
    note.textContent = s.note;
    const isRoof = key === 'roof';
    ba.hidden = isRoof; scrub.hidden = !isRoof;
    if (isRoof) { scR.value = 0; setScrub(0); sweep(0, 200, (v) => { scR.value = v; setScrub(v); }, 2200); }
    else {
      baB.src = s.b; baA.src = s.a; baB.alt = s.bAlt; baA.alt = s.aAlt;
      ba.classList.toggle('is-comp', s.comp);
      sweep(15, 55, (v) => { baR.value = v; setP(v); }, 900);
    }
    buzz(6);
  }
  ptabs.forEach((b, i) => {
    b.addEventListener('click', () => pick(i));
    b.addEventListener('keydown', (e) => {
      if (e.key !== 'ArrowRight' && e.key !== 'ArrowLeft') return;
      const j = (i + (e.key === 'ArrowRight' ? 1 : -1) + ptabs.length) % ptabs.length;
      pick(j); ptabs[j].focus();
    });
  });
  // one demo sweep the first time it is really in view, so people learn to drag
  new IntersectionObserver((en, o) => {
    if (!en[0].isIntersecting || swept) return;
    swept = true; o.disconnect();
    sweep(50, 12, (v) => { baR.value = v; setP(v); }, 700);
    setTimeout(() => sweep(12, 88, (v) => { baR.value = v; setP(v); }, 1300), 750);
    setTimeout(() => sweep(88, 50, (v) => { baR.value = v; setP(v); }, 700), 2100);
  }, { threshold: 0.6 }).observe(ba);

  /* ---------- Reels: tap to play, one at a time ---------- */
  const reels = $$('.reel');
  reels.forEach((r) => {
    const v = $('video', r), b = $('.reel__play', r);
    const toggle = () => {
      if (v.paused) {
        reels.forEach((o) => { if (o !== r) { $('video', o).pause(); o.classList.remove('is-playing'); } });
        v.play().then(() => r.classList.add('is-playing')).catch(() => {});
      } else { v.pause(); r.classList.remove('is-playing'); }
    };
    b.addEventListener('click', toggle);
    v.addEventListener('click', toggle);
  });
  // pause a reel that scrolls out of view
  const rio = new IntersectionObserver((en) => en.forEach((e) => { if (!e.isIntersecting) { $('video', e.target).pause(); e.target.classList.remove('is-playing'); } }), { threshold: 0.2 });
  reels.forEach((r) => rio.observe(r));

  /* ---------- Snap row dots ---------- */
  $$('[data-dots-for]').forEach((dots) => {
    const track = document.getElementById(dots.dataset.dotsFor);
    if (!track) return;
    const items = [...track.children];
    items.forEach(() => dots.appendChild(document.createElement('b')));
    const mark = () => {
      const w = items[0].getBoundingClientRect().width + 14;
      const i = Math.min(items.length - 1, Math.round(track.scrollLeft / w));
      [...dots.children].forEach((d, j) => d.classList.toggle('on', j === i));
    };
    track.addEventListener('scroll', () => requestAnimationFrame(mark), { passive: true });
    mark();
  });

  /* ---------- Process timeline fill ---------- */
  const steps = $('#steps');
  const fill = () => {
    const r = steps.getBoundingClientRect(), mid = innerHeight * 0.6;
    steps.style.setProperty('--p', Math.max(0, Math.min(1, (mid - r.top) / r.height)).toFixed(3));
  };

  /* ---------- Gallery filter + lightbox ---------- */
  const gs = $$('.g');
  $$('.chip').forEach((c) => c.addEventListener('click', () => {
    $$('.chip').forEach((o) => { const on = o === c; o.classList.toggle('is-on', on); o.setAttribute('aria-pressed', on); });
    gs.forEach((g) => g.classList.toggle('is-out', c.dataset.filter !== 'all' && g.dataset.kind !== c.dataset.filter));
    buzz(6);
  }));
  const lb = $('#lb'), lbImg = $('#lbImg'), lbCount = $('#lbCount');
  let cur = 0, list = [];
  const show = (i) => {
    cur = (i + list.length) % list.length;
    const g = list[cur], im = g.querySelector('img');
    lbImg.src = g.dataset.src; lbImg.alt = im.alt;
    lbCount.textContent = `${cur + 1} / ${list.length}`;
  };
  gs.forEach((g) => g.addEventListener('click', () => {
    list = gs.filter((x) => !x.classList.contains('is-out'));
    show(list.indexOf(g)); lb.showModal();
  }));
  lb.addEventListener('click', (e) => {
    const a = e.target.dataset.lb;
    if (a === 'close' || e.target === lb) lb.close();
    if (a === 'prev') show(cur - 1);
    if (a === 'next') show(cur + 1);
  });
  lb.addEventListener('keydown', (e) => { if (e.key === 'ArrowLeft') show(cur - 1); if (e.key === 'ArrowRight') show(cur + 1); });
  let sx = 0;
  lb.addEventListener('touchstart', (e) => (sx = e.touches[0].clientX), { passive: true });
  lb.addEventListener('touchend', (e) => { const dx = e.changedTouches[0].clientX - sx; if (Math.abs(dx) > 50) show(cur + (dx < 0 ? 1 : -1)); });

  /* ---------- Estimate quiz ---------- */
  const quiz = $('#quiz'), bar = $('#quizBar'), count = $('#quizCount'), err = $('#quizErr');
  const next = $('#quizNext'), back = $('#quizBack');
  let stepN = 1;
  const stepEl = (n) => quiz.querySelector(`[data-step="${n}"]`);
  function go(n) {
    stepEl(stepN).classList.remove('is-on');
    stepN = n;
    const el = stepEl(n);
    if (n === 4) { el.hidden = false; $('.quiz__nav', quiz).hidden = true; err.textContent = ''; count.textContent = 'Done'; bar.style.width = '100%'; return; }
    el.classList.add('is-on');
    if (quiz.getBoundingClientRect().top < 0) quiz.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    bar.style.width = (n / 3 * 100) + '%';
    count.textContent = `Step ${n} of 3`;
    back.hidden = n === 1;
    next.innerHTML = n === 3 ? 'Request my free estimate' : 'Next <span aria-hidden="true">→</span>';
    err.textContent = '';
  }
  function valid() {
    if (stepN === 1 && !quiz.querySelector('[name=project]:checked')) return 'Pick a project type to continue.';
    if (stepN === 2 && !quiz.querySelector('[name=when]:checked')) return 'Let us know roughly when you would like to start.';
    if (stepN === 3) {
      if (!quiz.elements.fullname.value.trim()) return 'Please add your name.';
      if (quiz.elements.phone.value.replace(/\D/g, '').length < 10) return 'Please add a 10-digit phone number.';
      const em = quiz.elements.email.value.trim();
      if (em && !/^\S+@\S+\.\S+$/.test(em)) return 'That email looks off. Check it or leave it blank.';
    }
    return '';
  }
  next.addEventListener('click', () => { const m = valid(); if (m) { err.textContent = m; buzz(30); return; } buzz(); go(stepN + 1); });
  back.addEventListener('click', () => go(stepN - 1));
  $$('[name=project]', quiz).forEach((r) => r.addEventListener('change', () => setTimeout(() => stepN === 1 && go(2), 260)));
  quiz.addEventListener('submit', (e) => e.preventDefault());

  /* ---------- Mobile menu sheet ---------- */
  const sheet = $('#sheet'), menuBtn = $('#menuBtn');
  const openSheet = (open) => {
    menuBtn.setAttribute('aria-expanded', open);
    if (open) { sheet.hidden = false; setTimeout(() => sheet.classList.add('is-open'), 20); }
    else { sheet.classList.remove('is-open'); setTimeout(() => (sheet.hidden = true), 420); }
  };
  menuBtn.addEventListener('click', () => openSheet(sheet.hidden));
  sheet.addEventListener('click', (e) => { if (e.target.closest('[data-close]')) openSheet(false); });
  addEventListener('keydown', (e) => { if (e.key === 'Escape' && !sheet.hidden) openSheet(false); });

  /* ---------- Header hide/show + dock tuck ---------- */
  const hdr = $('#hdr'), dock = $('.dock'), est = $('#estimate');
  let lastY = scrollY;
  const onScroll = () => {
    const y = scrollY;
    hdr.classList.toggle('is-hidden', y > 300 && y > lastY + 4 && sheet.hidden);
    if (y < lastY - 4 || y < 300) hdr.classList.remove('is-hidden');
    const r = est.getBoundingClientRect();
    dock.classList.toggle('is-tucked', r.top < innerHeight * 0.7 && r.bottom > 0);
    lastY = y;
    fill();
  };
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();
})();
