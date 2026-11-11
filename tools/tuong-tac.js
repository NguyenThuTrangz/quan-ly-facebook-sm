// Dan vao javascript_tool tren trang facebook.com (newsfeed) hoac trang group.
// Dat muc tieu: ST.targets = [5,4,1,5] (lenh "tuong tac 5/4/1/5"), ST.useLove = [false,true,false,true] (xen ke Like/Love).
// Goi lai `await STEP(38000)` nhieu lan (JS timeout 45s) cho den khi left = [].
// Bai dau tien dem = bai dang hien tren man hinh (div[aria-posinset] nho nhat dang co).
const sl = ms => new Promise(r => setTimeout(r, ms));
window.ST = { targets: [5, 4, 1, 5], useLove: [false, true, false, true], valid: 0, done: [],
  next: Math.min(...[...document.querySelectorAll('div[aria-posinset]')].map(x => +x.getAttribute('aria-posinset'))) };
{ let acc = 0; ST.targets = ST.targets.map(x => acc += x); }
window.STEP = async budget => {
  const t0 = Date.now();
  while (Date.now() - t0 < budget && ST.targets.length) {
    const e = document.querySelector(`div[aria-posinset="${ST.next}"]`);
    if (!e) { scrollBy(0, 700); await sl(900); continue; }
    e.scrollIntoView({ block: 'center' }); await sl(1800 + Math.random() * 1500);
    const t = e.innerText;
    const bad = t.length < 40 || /Sponsored|Reels|Suggested for you|People you may know|group suggestions|Suggested groups/i.test(t.slice(0, 400)) || /^Stories/.test(t.trim());
    if (!bad) {
      ST.valid++;
      if (ST.valid >= ST.targets[0]) {
        const like = e.querySelector('[aria-label^="React with Like"]');
        const who = (t.split('\n').map(s => s.trim()).find(x => x.length > 2 && !/Online status|^Active$/.test(x)) || '').slice(0, 30);
        if (like) {
          let kind = 'Like';
          if (ST.useLove[0]) {
            e.querySelector('[aria-label^="React to "]')?.click(); await sl(1500);
            const lv = [...document.querySelectorAll('[aria-label="Love"]')].find(b => b.offsetParent);
            if (lv) { lv.click(); kind = 'Love'; } else like.click();
          } else like.click();
          await sl(1500);
          const ok = !e.querySelector('[aria-label^="React with Like"]');
          ST.done.push(ST.valid + '#' + ST.next + ':' + who + ' ' + kind + (ok ? ' OK' : ' ?'));
          const cnt = ST.targets.shift(); ST.useLove.shift();
        } else { ST.done.push('da react san #' + ST.next + ':' + who); ST.valid--; }
      }
    }
    ST.next++;
  }
  return JSON.stringify({ valid: ST.valid, next: ST.next, left: ST.targets, done: ST.done });
};
'ready';
