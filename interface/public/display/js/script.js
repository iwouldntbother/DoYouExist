socket = io();

const DD2DMS = (lat, lng) => {
  // 3.51667
  lat_deg = lat.split('.')[0];
  lat_min = Number('0.' + lat.split('.')[1]) * 60;
  lat_sec = Number('0.' + String(lat_min).split('.')[1]) * 60;
  lat_dir = '';

  lng_deg = lng.split('.')[0];
  lng_min = Number('0.' + lng.split('.')[1]) * 60;
  lng_sec = Number('0.' + String(lng_min).split('.')[1]) * 60;
  lng_dir = '';

  if (Number(lat_deg) < 0) {
    lat_dir = 'S';
  } else {
    lat_dir = 'N';
  }

  if (Number(lng_deg) < 0) {
    lng_dir = 'W';
  } else {
    lng_dir = 'E';
  }

  return `${lat_deg || 0}° ██\′ ██″ ${lat_dir} ${
    lng_deg || 0
  }° ██\′ ██″ ${lng_dir}`;
};

// Characters
// ─ │ ┐ ┌ └ ┘ ├ ┤ ┬ ┴ ┼

const displayData = (info) => {
  const displayTextaArea = document.querySelector('#displayTextArea');

  displayTextaArea.innerHTML = '';

  for (let i = 0; i < displayPage.length; i++) {
    displayTextaArea.innerHTML += displayPage[i] + '<br>';
  }

  if (!info) {
    return;
  }

  document.querySelector('#name').innerHTML = `${
    info.name.split(' ')[0]
  } ${info.name
    .split(' ')[1]
    .slice(0, 1)
    .padEnd(info.name.split(' ')[1].length, '█')}`.padEnd(39);
  document.querySelector('#phone').innerHTML = `${info.phone_number.slice(
    0,
    2
  )}${''.padEnd(info.phone_number.length - 4, '█')}${info.phone_number.slice(
    -2
  )}`.padEnd(29);
  document.querySelector('#uuid').innerHTML = `${info.uuid
    .split('-')[0]
    .slice(0, 4)}████-████-████-████-████████${info.uuid
    .split('-')[4]
    .slice(-4)}`.padEnd(39);
  document.querySelector('#dob').innerHTML = (
    info.date_of_birth.slice(0, 6) + '████'
  ).padEnd(29);
  document.querySelector('#bankOne').innerHTML = info.bank_card[0].padEnd(39);
  document.querySelector('#bankTwo').innerHTML = info.bank_card[2]
    .split(' ')[0]
    .slice(-4)
    .padStart(info.bank_card[2].length, '█')
    .padEnd(39);
  document.querySelector('#bankThree').innerHTML = (
    info.bank_card[2].split(' ')[1] + ' CVC: ███'
  ).padEnd(39);
  document.querySelector('#addOne').innerHTML = info.address
    .split('|')[0]
    .split(' ')[0]
    .padEnd(info.address.split('|')[0].length, '█')
    .padEnd(29);
  document.querySelector('#addTwo').innerHTML = info.address
    .split('|')[1]
    .slice(0, 1)
    .padEnd(info.address.split('|')[1].length, '█')
    .padEnd(29);
  document.querySelector('#addThree').innerHTML = (
    info.address.split('|')[2].split(' ')[0] + ' ███'
  ).padEnd(29);
  document.querySelector('#locOne').innerHTML = DD2DMS(
    info.last_location[0],
    info.last_location[1]
  ).padEnd(71);
  document.querySelector('#locTwo').innerHTML = (
    info.last_location[2]
      .slice(0, 1)
      .padEnd(info.last_location[2].length, '█') +
    ', ' +
    info.last_location[3]
  ).padEnd(71);
  document.querySelector('#locThree').innerHTML = info.last_location[4]
    .slice(0, 1)
    .padEnd(info.last_location[4].length, '█')
    .padEnd(71);

  // Photo
  document.querySelector('#square-0').setAttribute('src', info.face_image);
  // fingerprints
  document
    .querySelector('#square-1-0')
    .setAttribute('src', info.fingerprints[0]);
  document
    .querySelector('#square-1-1')
    .setAttribute('src', info.fingerprints[1]);
  document
    .querySelector('#square-1-2')
    .setAttribute('src', info.fingerprints[2]);
  document
    .querySelector('#square-1-3')
    .setAttribute('src', info.fingerprints[3]);
  document
    .querySelector('#square-1-4')
    .setAttribute('src', info.fingerprints[4]);
  document
    .querySelector('#square-1-5')
    .setAttribute('src', info.fingerprints[5]);
  document
    .querySelector('#square-1-6')
    .setAttribute('src', info.fingerprints[6]);
  document
    .querySelector('#square-1-7')
    .setAttribute('src', info.fingerprints[7]);

  document.getElementById('square-0').style.opacity = 1;
  document.getElementById('square-1-0').style.opacity = 1;
  document.getElementById('square-1-1').style.opacity = 1;
  document.getElementById('square-1-2').style.opacity = 1;
  document.getElementById('square-1-3').style.opacity = 1;
  document.getElementById('square-1-4').style.opacity = 1;
  document.getElementById('square-1-5').style.opacity = 1;
  document.getElementById('square-1-6').style.opacity = 1;
  document.getElementById('square-1-7').style.opacity = 1;
  document.getElementById('privacyBar').style.opacity = 1;
};

// displayData(tempData[0]);
// displayData()

const displayTextaArea = document.querySelector('#displayTextArea');
displayTextaArea.innerHTML = '';
for (let i = 0; i < displayPage.length; i++) {
  displayTextaArea.innerHTML += blankDisplayPage[i] + '<br>';
}

socket.on('profileData', (data) => {
  displayData(JSON.parse(data));
  console.log(JSON.parse(data));
});
