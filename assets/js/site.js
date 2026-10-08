'use strict';

document.documentElement.classList.add('js-enabled');
const year = document.getElementById('year');
if (year) year.textContent = new Date().getFullYear();

const menu = document.querySelector('.menu-toggle');
const navigation = document.getElementById('navigation');
if (menu && navigation) {
  menu.hidden = false;
  function closeMenu() {
    menu.setAttribute('aria-expanded', 'false');
    navigation.classList.remove('is-open');
  }
  menu.addEventListener('click', () => {
    const open = menu.getAttribute('aria-expanded') !== 'true';
    menu.setAttribute('aria-expanded', String(open));
    navigation.classList.toggle('is-open', open);
  });
  navigation.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
  document.addEventListener('keydown', event => {
    if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') { closeMenu(); menu.focus(); }
  });
}

const filters = document.querySelector('.filters');
if (filters) {
  filters.hidden = false;
  filters.querySelectorAll('[data-filter]').forEach(button => button.addEventListener('click', () => {
    filters.querySelectorAll('[data-filter]').forEach(filter => {
      filter.classList.toggle('active', filter === button);
      filter.setAttribute('aria-pressed', String(filter === button));
    });
    let count = 0;
    document.querySelectorAll('.tour-card').forEach(card => {
      card.hidden = button.dataset.filter !== 'all' && card.dataset.category !== button.dataset.filter;
      if (!card.hidden) count++;
    });
    document.getElementById('filter-status').textContent = `${count} ${count === 1 ? 'journey' : 'journeys'} shown`;
  }));
}

function localDate() {
  const today = new Date();
  return `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
}

const form = document.getElementById('enquiry-form');
if (form) {
  form.hidden = false;
  const arrival = form.elements.arrival;
  const traveller = form.elements.traveller;
  const status = document.getElementById('form-status');
  const storageKey = 'vintage-eyes:last-draft';
  const cooldown = 15000;
  let lastDraft = 0;
  try { lastDraft = Number(localStorage.getItem(storageKey)) || 0; } catch { /* Storage can be disabled; enquiries still work. */ }
  arrival.min = localDate();
  traveller.addEventListener('input', () => traveller.setCustomValidity(''));

  form.addEventListener('submit', event => {
    event.preventDefault();
    arrival.min = localDate();
    const name = traveller.value.trim();
    traveller.setCustomValidity(!name ? 'Please enter your name.' : name.length > 80 ? 'Please keep your name under 80 characters.' : '');
    if (!form.reportValidity()) return;

    // These client-side checks are bypassable; they are not server-verified spam protection.
    if (form.elements.website.value) {
      status.textContent = 'Please use the direct WhatsApp link or call us to continue your enquiry.';
      return;
    }
    const now = Date.now();
    try { lastDraft = Number(localStorage.getItem(storageKey)) || lastDraft; } catch { /* Use the in-memory timestamp. */ }
    const remaining = cooldown - (now - lastDraft);
    if (remaining > 0) {
      let notice = status.querySelector('.cooldown-notice');
      if (!notice) { notice = document.createElement('span'); notice.className = 'cooldown-notice'; status.append(notice); }
      notice.textContent = ` Please wait ${Math.ceil(remaining / 1000)} seconds before creating another draft.`;
      return;
    }
    const guests = Number(form.elements.guests.value);
    if (!Number.isInteger(guests) || guests < 1 || guests > 50 || form.elements.notes.value.length > 1500) {
      status.textContent = 'Please check the traveller count and keep your notes under 1,500 characters.';
      return;
    }
    const message = ['Hello Vintage Eyes!', `My name is ${name}.`, `Journey: ${form.elements.journey.value}`, `Travellers: ${guests}`];
    if (arrival.value) message.push(`Preferred arrival: ${arrival.value}`);
    if (form.elements.notes.value.trim()) message.push(`Notes: ${form.elements.notes.value.trim()}`);
    message.push(`Tour page: ${document.querySelector('link[rel="canonical"]').href}`);
    message.push('Please share availability, the itinerary and a quote.');
    const url = new URL('https://wa.me/916363336467');
    url.searchParams.set('text', message.join('\n'));
    window.open(url.href, '_blank', 'noopener,noreferrer');
    lastDraft = now;
    try { localStorage.setItem(storageKey, String(now)); } catch { /* No personal information is stored. */ }
    status.replaceChildren(document.createTextNode('Your draft is ready. Review it and tap Send in WhatsApp. If it did not open, '));
    const fallback = document.createElement('a');
    fallback.textContent = 'open your WhatsApp draft here';
    fallback.href = url.href;
    fallback.target = '_blank';
    fallback.rel = 'noopener noreferrer';
    status.append(fallback, document.createTextNode('.'));
  });
}
