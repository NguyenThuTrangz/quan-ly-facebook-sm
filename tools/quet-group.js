// Chay tren trang facebook.com/groups/<id>/about (sau khi load ~3s). Tra ve 1 dong tom tat de cham diem group.
(() => {
  const t = document.body.innerText;
  const num = s => { if (!s) return null; s = s.replace(/,/g, ''); const k = /K$/i.test(s) ? 1000 : /M$/i.test(s) ? 1e6 : 1; return Math.round(parseFloat(s) * k); };
  const m = t.match(/([\d.,]+[KM]?)\s+(?:total\s+)?members/i);
  const day = t.match(/([\d,]+)\s+new posts? today/i);
  const mon = t.match(/([\d,]+)\s+in the last month/i);
  const wk = t.match(/\+\s*([\d,]+)\s+in the last week/i);
  const rules = (t.split(/Group rules from the admins/i)[1] || '').slice(0, 2500);
  const about = (t.split(/About this group/i)[1] || '').split(/\n(Private|Public)\n/)[0].slice(0, 400);
  const all = about + ' ' + rules;
  return JSON.stringify({
    ok: !/isn't available|content isn't available/i.test(t),
    name: (document.title || '').replace(/ \| Facebook$/, '').replace(/^\(\d+\)\s*/, '').slice(0, 45),
    priv: /Private group/i.test(t) ? 'P' : 'O',
    mem: num(m && m[1]), day: day ? +day[1].replace(/,/g, '') : 0, mon: mon ? +mon[1].replace(/,/g, '') : 0, wk: wk ? +wk[1].replace(/,/g, '') : 0,
    noSell: /no (self[- ]?)?promo|no promotion|no advertis|no business|no selling|no sales|not a (buy|sell)|no spam.{0,20}(sell|promo)|selling is not allowed|no shop|no links? to (shop|store)/i.test(all),
    sell: /wholesale|for sale|buy and sell|selling|seller|vendor|retail|boutique|shop/i.test(all),
    resale: /pre-?loved|second ?hand|used clothing|vintage/i.test(all + ' ' + document.title),
    en: /[a-z]{4,}/i.test(about) && !/[ăâđêôơư]/i.test(about)
  });
})()
