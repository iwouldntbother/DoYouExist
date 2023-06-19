const socket = io();

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

  return `${lat_deg || 0}° ${Math.floor(lat_min) || 0}\′ ${
    Math.floor(lat_sec) || 0
  }″ ${lat_dir} ${lng_deg || 0}° ${Math.floor(lng_min) || 0}\′ ${
    Math.floor(lng_sec) || 0
  }″ ${lng_dir}`;
};

let timeoutCounter;

const startTimeoutCounter = () => {
  timeoutCounter = setTimeout(() => {
    socket.emit('stopDetect');
    window.location.reload(true);
  }, 60000);
};

const stopTimeoutCounter = () => {
  clearTimeout(timeoutCounter);
};

let currentPage = '';

const loadInfo = (info) => {
  document.querySelector('#name').innerHTML = info.name.padEnd(36);
  document.querySelector('#phone').innerHTML = info.phone_number.padEnd(21);
  document.querySelector('#uuid').innerHTML = info.uuid.padEnd(36);
  document.querySelector('#dob').innerHTML = info.date_of_birth.padEnd(21);
  document.querySelector('#bankOne').innerHTML = info.bank_card[0].padEnd(36);
  document.querySelector('#bankTwo').innerHTML = info.bank_card[2]
    .split(' ')[0]
    .padEnd(36);
  document.querySelector('#bankThree').innerHTML = (
    info.bank_card[2].split(' ')[1] +
    ' ' +
    info.bank_card[3]
  ).padEnd(36);
  document.querySelector('#AddOne').innerHTML = info.address
    .split('|')[0]
    .padEnd(21);
  document.querySelector('#AddTwo').innerHTML = info.address
    .split('|')[1]
    .padEnd(21);
  document.querySelector('#AddThree').innerHTML = info.address
    .split('|')[2]
    .padEnd(21);
  document.querySelector('#locOne').innerHTML = DD2DMS(
    info.last_location[0],
    info.last_location[1]
  ).padEnd(60);
  document.querySelector('#locTwo').innerHTML = (
    info.last_location[2] +
    ', ' +
    info.last_location[3]
  ).padEnd(60);
  document.querySelector('#locThree').innerHTML =
    info.last_location[4].padEnd(60);

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
};

const loadButtons = (pageName) => {
  switch (pageName) {
    case 'profile':
      document.querySelector('#button-0').style.width = '37.9em';
      document.querySelector('#button-0').style.height = '13em';
      document.querySelector('#button-0').style.top = '41.4em';
      document.querySelector('#button-0').style.left = '0.5em';

      document.querySelector('#button-1').style.width = '39.8em';
      document.querySelector('#button-1').style.height = '13em';
      document.querySelector('#button-1').style.top = '41.4em';
      document.querySelector('#button-1').style.right = '0.5em';
      break;

    case 'welcome':
      document.querySelector('#button-0').style.width = '39em';
      document.querySelector('#button-0').style.height = '40.5em';
      document.querySelector('#button-0').style.top = '14em';
      document.querySelector('#button-0').style.left = '0.5em';

      document.querySelector('#button-1').style.width = '38.7em';
      document.querySelector('#button-1').style.height = '40.5em';
      document.querySelector('#button-1').style.top = '14em';
      document.querySelector('#button-1').style.right = '0.5em';
      break;

    default:
      break;
  }
};

const loadPage = (pageName, info) => {
  currentPage = pageName;
  document.querySelector('#mainTextArea').innerHTML = '';
  switch (pageName) {
    case 'profile':
      for (let i = 0; i < pages[pageName].length; i++) {
        document.querySelector('#mainTextArea').innerHTML +=
          pages[pageName][i] + '<br>';
      }
      loadInfo(info);
      document.querySelector('#square-0').style.display = 'block';
      document.querySelector('#square-1').style.display = 'flex';
      loadButtons(pageName);
      stopTimeoutCounter();
      break;

    case 'welcome':
      for (let i = 0; i < pages[pageName].length; i++) {
        document.querySelector('#mainTextArea').innerHTML +=
          pages[pageName][i] + '<br>';
      }
      document.querySelector('#square-0').style.display = 'none';
      document.querySelector('#square-1').style.display = 'none';
      loadButtons(pageName);
      break;

    case 'check':
      for (let i = 0; i < pages[pageName].length; i++) {
        document.querySelector('#mainTextArea').innerHTML +=
          pages[pageName][i] + '<br>';
      }
      document.querySelector('#square-0').style.display = 'none';
      document.querySelector('#square-1').style.display = 'none';
      startTimeoutCounter();
      break;

    case 'printing':
      for (let i = 0; i < pages[pageName].length; i++) {
        document.querySelector('#mainTextArea').innerHTML +=
          pages[pageName][i] + '<br>';
      }
      document.querySelector('#square-0').style.display = 'none';
      document.querySelector('#square-1').style.display = 'none';
      break;

    case 'thankyou':
      for (let i = 0; i < pages[pageName].length; i++) {
        document.querySelector('#mainTextArea').innerHTML +=
          pages[pageName][i] + '<br>';
      }
      document.querySelector('#square-0').style.display = 'none';
      document.querySelector('#square-1').style.display = 'none';
      typeCommand('');
      loading(false);
      cursor(true);
      setTimeout(() => {
        window.location.reload(true);
      }, 5000);
      break;

    default:
      break;
  }
};

let typeSpeed = 100;

const typeCommand = (commandString) => {
  commandEl = document.querySelector('#typeCommand');
  commandEl.innerHTML = '';
  let idx = 0;
  typing = setInterval(() => {
    if (idx >= commandString.length) {
      clearInterval(typing);
    }
    commandEl.innerHTML += commandString.charAt(idx);
    idx++;
  }, typeSpeed);
};

const spinner = (show) => {
  if (show) {
    document.querySelector('.spinner').style.display = 'inline-block';
  } else {
    document.querySelector('.spinner').style.display = 'none';
  }
};

const cursor = (show) => {
  if (show) {
    document.querySelector('.cursor').style.display = 'inline-block';
  } else {
    document.querySelector('.cursor').style.display = 'none';
  }
};

const loading = (show) => {
  if (show) {
    document.querySelector('.loading').style.display = 'inline-block';
  } else {
    document.querySelector('.loading').style.display = 'none';
  }
};

spinner(false);
loading(false);

// YES button event
document.querySelector('#button-0').addEventListener('click', () => {
  // console.log('button-0 pressed'); // DEV
  // document.querySelector('#button-0').style.opacity = 1; // DEV
  switch (currentPage) {
    case 'profile':
      printProfile(currentJSONString);
      typeCommand('Printing, please wait');
      setTimeout(() => {
        cursor(false);
        loading(true);
      }, 2100);
      break;

    case 'welcome':
      loadPage('check');
      startDetecting();
      typeCommand('Analysing face, please wait');
      setTimeout(() => {
        cursor(false);
        loading(true);
      }, 2700);
      break;

    default:
      break;
  }
});

// NO button event
document.querySelector('#button-1').addEventListener('click', () => {
  // console.log('button-1 pressed'); // DEV
  // document.querySelector('#button-1').style.opacity = 1; // DEV
  switch (currentPage) {
    case 'profile':
      loadPage('thankyou');
      break;

    case 'welcome':
      loadPage('check');
      startDetecting();
      typeCommand('Analysing face, please wait');
      setTimeout(() => {
        cursor(false);
        loading(true);
      }, 2700);
      break;

    default:
      break;
  }
});

// Socket.io //

currentJSONString = '';

socket.on('profileData', (data) => {
  console.log('profile data received');
  console.log(JSON.parse(data));
  profileInfo = JSON.parse(data);
  currentJSONString = JSON.stringify(profileInfo);
  loadPage('profile', profileInfo);
  typeCommand('Presenting profile data');
  setTimeout(() => {
    cursor(false);
    loading(false);
  }, 2700);
});

socket.on('thankyou', () => {
  loadPage('thankyou');
});

let detecting = false;

const startDetecting = () => {
  if (detecting) {
    return;
  }

  detecting = true;

  socket.emit('start');
};

const printProfile = (jsonStringData) => {
  loadPage('printing');
  socket.emit('print', jsonStringData);
};

// DEV //

// welcome, check, profile, thankyou

pageArray = ['welcome', 'check', 'profile', 'thankyou'];
position = 0;

document.body.addEventListener('keydown', (e) => {
  // console.log(e.key);
  if (e.key == 'ArrowRight') {
    if (position < pageArray.length - 1) {
      position++;
      loadPage(
        pageArray[position],
        JSON.parse(JSON.stringify(tempData[0]).replaceAll('\n', '|'))
      );
    } else if (e.key == ' ') {
      startDetecting();
    } else {
      position = 0;
      loadPage(
        pageArray[position],
        JSON.parse(JSON.stringify(tempData[0]).replaceAll('\n', '|'))
      );
    }
    console.log(position, pageArray[position]);
  }
});

loadPage(
  'welcome',
  JSON.parse(JSON.stringify(tempData[0]).replaceAll('\n', '|'))
);
