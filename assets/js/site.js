'use strict';

const tours = {
  swift: { name: 'Swift Hampi', meta: '2 DAYS / 1 NIGHT', price: 'From ₹8,999 per couple', image: 'chariot', select: 'Swift Hampi — 2 days', description: 'A compact Hampi break with a hotel stay, private car and sightseeing.', days: [['Day 1 · Arrive & discover Hampi', 'Hospet pickup, hotel check-in, and temple highlights including Vittala and Virupaksha.'], ['Day 2 · Royal ruins & departure', 'Explore the royal enclosure, Lotus Mahal and Elephant Stables as departure time allows, then return to Hospet.']], included: 'Hotel, air-conditioned cab, driver, parking and Hospet transfers. Sightseeing allowance: 8 hours / 80 km per day. Entry tickets, camera fees and unspecified meals are extra.' },
  heritage: { name: 'Heritage Hampi', meta: '3 DAYS / 2 NIGHTS', price: 'From ₹11,999 per couple', image: 'hampi', select: 'Heritage Hampi — 3 days', description: 'More time for Hampi’s monuments, with a third day around Anegundi.', days: [['Day 1 · Temples & first impressions', 'Hospet pickup, check-in and the temple trail, including Vittala and Virupaksha.'], ['Day 2 · The royal side of Hampi', 'Royal enclosure, Lotus Mahal, Elephant Stables and riverside sights.'], ['Day 3 · Across to Anegundi', 'Discuss stops around Anjanadri, Pampa Sarovar and Sanapur Lake before your Hospet drop-off.']], included: 'Hotel, air-conditioned private cab, driver, parking and Hospet transfers. Sightseeing allowance: 8 hours / 80 km per day. Entry tickets, camera fees, optional activities and unspecified meals are extra.' },
  regal: { name: 'Regal explorations', meta: '4 DAYS / 3 NIGHTS', price: 'From ₹15,999 per couple', image: 'badami', select: 'Regal heritage circuit — 4 days', description: 'A heritage road trip through Hampi, Aihole, Pattadakal and Badami.', days: [['Day 1 · Hampi', 'Arrive in Hospet, check in, and explore Hampi’s monuments.'], ['Day 2 · Aihole', 'Travel via Aihole’s temple sites to Badami for your overnight stay.'], ['Day 3 · Pattadakal', 'Spend the day exploring Pattadakal’s temple complex.'], ['Day 4 · Badami & departure', 'Visit Badami’s caves and other sights before your arranged drop-off.']], included: 'Hotel, air-conditioned private cab, driver, parking and arranged transfers. Confirm the route, departure point and vehicle allowance with your quote. Meals, entry tickets, camera fees and optional activities are extra.' },
  sightseeing: { name: 'Hampi by car', meta: '1 DAY / PRIVATE TOUR', price: 'From ₹2,700 per car · up to 4 guests', image: 'chariot', select: 'Hampi sightseeing by car — 1 day', description: 'A private sightseeing day for travellers who already have their accommodation arranged.', days: [['Your Hampi day', 'Explore highlights such as Vittala Temple, Virupaksha Temple, the royal enclosure, Lotus Mahal and Elephant Stables. The route is planned around your available time.']], included: 'Private car and driver, 8 hours of sightseeing, parking and pickup/drop-off in Hampi or Hospet. No hotel stay. Entry tickets, camera fees and meals are extra. Vehicle-specific prices are confirmed on enquiry.' }
};

document.documentElement.classList.add('js-enabled');
document.getElementById('year').textContent = new Date().getFullYear();

const menu = document.querySelector('.menu-toggle');
const navigation = document.getElementById('navigation');
menu.hidden = false;
function closeMenu() { menu.setAttribute('aria-expanded', 'false'); navigation.classList.remove('is-open'); }
menu.addEventListener('click', () => {
  const open = menu.getAttribute('aria-expanded') !== 'true';
  menu.setAttribute('aria-expanded', String(open));
  navigation.classList.toggle('is-open', open);
});
navigation.addEventListener('click', event => { if (event.target.closest('a')) closeMenu(); });
document.addEventListener('keydown', event => { if (event.key === 'Escape' && menu.getAttribute('aria-expanded') === 'true') { closeMenu(); menu.focus(); } });

document.querySelector('.filters').hidden = false;
document.querySelectorAll('[data-filter]').forEach(button => button.addEventListener('click', () => {
  document.querySelectorAll('[data-filter]').forEach(filter => {
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

const dialog = document.getElementById('tour-dialog');
let activeTour;
let previousFocus;
function element(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text) node.textContent = text;
  return node;
}
document.querySelectorAll('[data-tour]').forEach(link => link.addEventListener('click', event => {
  if (typeof dialog.showModal !== 'function') {
    document.getElementById('journey-select').value = tours[link.dataset.tour].select;
    return;
  }
  event.preventDefault();
  activeTour = tours[link.dataset.tour];
  previousFocus = link;
  const content = document.getElementById('dialog-content');
  content.replaceChildren();
  const image = element('img', 'dialog-image');
  image.src = `assets/images/${activeTour.image}.jpg`;
  image.alt = link.closest('.tour-card').querySelector('img').alt;
  content.append(image, element('p', 'eyebrow', activeTour.meta));
  const title = element('h2', 'dialog-title', activeTour.name);
  title.id = 'dialog-title';
  content.append(title, element('p', 'dialog-price', activeTour.price), element('p', 'dialog-description', activeTour.description));
  const list = element('ol', 'itinerary');
  activeTour.days.forEach(([heading, text]) => {
    const item = element('li');
    item.append(element('strong', '', heading), element('p', '', text));
    list.append(item);
  });
  content.append(list, element('p', 'dialog-inclusions', activeTour.included));
  dialog.showModal();
  document.body.classList.add('modal-open');
}));
document.querySelector('.dialog-close').addEventListener('click', () => dialog.close());
dialog.addEventListener('click', event => {
  const bounds = dialog.getBoundingClientRect();
  if (event.target === dialog && (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom)) dialog.close();
});
dialog.addEventListener('close', () => {
  document.body.classList.remove('modal-open');
  if (previousFocus) previousFocus.focus({ preventScroll: true });
});
document.getElementById('dialog-enquire').addEventListener('click', () => {
  document.getElementById('journey-select').value = activeTour.select;
  dialog.close();
  document.getElementById('plan').scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
  document.querySelector('[name="traveller"]').focus({ preventScroll: true });
});

const arrival = document.getElementById('arrival');
function localDate() {
  const today = new Date();
  return `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, '0')}-${String(today.getDate()).padStart(2, '0')}`;
}
arrival.min = localDate();
const form = document.getElementById('enquiry-form');
form.addEventListener('submit', event => {
  event.preventDefault();
  arrival.min = localDate();
  const name = form.elements.traveller;
  name.setCustomValidity(name.value.trim() ? '' : 'Please enter your name.');
  if (!form.reportValidity()) return;
  const details = new FormData(form);
  const message = ['Hello Vintage Eyes!', `My name is ${details.get('traveller').trim()}.`, `Journey: ${details.get('journey')}`, `Travellers: ${details.get('guests')}`];
  if (details.get('arrival')) message.push(`Preferred arrival: ${details.get('arrival')}`);
  if (details.get('notes').trim()) message.push(`Notes: ${details.get('notes').trim()}`);
  message.push('Please share availability, the itinerary and a quote.');
  const url = new URL('https://wa.me/916363336467');
  url.searchParams.set('text', message.join('\n'));
  window.open(url.href, '_blank', 'noopener,noreferrer');
  const status = document.getElementById('form-status');
  status.replaceChildren(document.createTextNode('Your enquiry draft is ready. If WhatsApp did not open, '));
  const fallback = element('a', '', 'open your draft here');
  fallback.href = url.href;
  fallback.target = '_blank';
  fallback.rel = 'noopener noreferrer';
  status.append(fallback, document.createTextNode('.'));
});
form.elements.traveller.addEventListener('input', event => event.target.setCustomValidity(''));
