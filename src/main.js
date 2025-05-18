import './style.css';
import data from '../resources/_gen/metadata_all.json' with {type: 'json'};

function buildCalendarUrl(filename) {
  const url = new URL(`ical/${filename}`, window.location.href);
  return url.href;
}

const container = document.getElementById('calendar-list');

function createHolidayTag(name) {
  const span = document.createElement('span');
  span.textContent = name;
  span.title = name;
  span.className = 'px-3 py-1 rounded-full bg-gray-100 dark:bg-slate-700 text-gray-800 dark:text-gray-100 shadow-sm transition-all hover:scale-105 hover:shadow-md max-w-[12rem] truncate inline-block';
  return span;
}

function createCalendarCard(calendar) {
    const wrapper = document.createElement('div');
    wrapper.innerHTML = `
    <div class="p-6 bg-gradient-to-br from-white via-slate-50 to-slate-100 dark:from-slate-800 dark:via-slate-900 dark:to-slate-800 border border-gray-200 dark:border-gray-700 rounded-2xl shadow-lg transition-shadow hover:shadow-xl space-y-4">
      <div class="space-y-3">
        <p class="font-bold text-xl text-gray-900 dark:text-white tracking-tight">${calendar.title}</p>
        <div class="bg-white dark:bg-slate-900 border border-gray-100 dark:border-slate-700 rounded-lg p-3 flex items-center gap-2 shadow-inner">
          <input class="flex-1 px-3 py-2 rounded-md font-mono text-sm bg-transparent text-gray-800 dark:text-gray-100 focus:outline-none" readonly id="input-${calendar.file.replace('.ics', '')}" value="${buildCalendarUrl(calendar.file)}">
          <button class="copy-btn px-4 py-2 bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 text-white rounded-md text-sm shadow-md transition-transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-blue-500">Copy</button>
        </div>
        <div class="copy-feedback hidden text-green-600 dark:text-green-400 text-sm">✓ In die Zwischenablage kopiert</div>
      </div>
      <div>
        <div class="holiday-tags flex flex-wrap gap-2 text-sm mt-3"></div>
      </div>
      <div class="text-xs text-gray-400 dark:text-gray-500 pt-3 border-t border-gray-100 dark:border-gray-700 flex flex-wrap gap-4">
        <p><span class="opacity-70">Region:</span> ${calendar.region}</p>
        <p><span class="opacity-70">Zeitraum:</span> ${calendar.start_year} – ${calendar.end_year}</p>
        <p><span class="opacity-70">Kategorien:</span> ${calendar.categories.join(', ')}</p>
        <p><span class="opacity-70">Generiert am:</span> <time title="${new Date(calendar.generated_at).toLocaleString('de-DE')}">${new Date(calendar.generated_at).toLocaleDateString('de-DE')}</time></p>
      </div>
    </div>
  `;

    // Append holiday tags
    const tagsContainer = wrapper.querySelector('.holiday-tags');
    calendar.holidays.forEach(holiday => {
        tagsContainer.appendChild(createHolidayTag(holiday));
    });

    // Copy logic
    const copyBtn = wrapper.querySelector('.copy-btn');
    const input = wrapper.querySelector('input');
    const feedback = wrapper.querySelector('.copy-feedback');
    copyBtn.addEventListener('click', () => {
        navigator.clipboard.writeText(input.value).then(() => {
            feedback.classList.remove('hidden');
            setTimeout(() => feedback.classList.add('hidden'), 1500);
        });
    });

    return wrapper;
}

// Render all calendars
data.forEach(calendar => {
    container.appendChild(createCalendarCard(calendar));
});
